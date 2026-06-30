import os
from bs4 import BeautifulSoup

BASE_DIR = r"C:\\Users\\Hannah\\Documents\\PortfolioWebsite"
PAGES = ["index", "about", "experience", "projects", "skills", "sports", "writing", "contact"]
LANGS = ["en", "de", "fr"]

NAV_LABELS = {
    "en": {
        "index": "HOME", "about": "ABOUT", "experience": "EXPERIENCE", 
        "projects": "PROJECTS", "skills": "SKILLS", "sports": "SPORTS", 
        "writing": "WRITING", "contact": "CONTACT"
    },
    "de": {
        "index": "STARTSEITE", "about": "ÜBER MICH", "experience": "ERFAHRUNG", 
        "projects": "PROJEKTE", "skills": "FÄHIGKEITEN", "sports": "SPORT", 
        "writing": "SCHREIBEN", "contact": "KONTAKT"
    },
    "fr": {
        "index": "ACCUEIL", "about": "À PROPOS", "experience": "EXPÉRIENCE", 
        "projects": "PROJETS", "skills": "COMPÉTENCES", "sports": "SPORT", 
        "writing": "ÉCRITURE", "contact": "CONTACT"
    }
}

for lang in LANGS:
    for page in PAGES:
        # Determine filename
        filename = f"{page}.html" if lang == "en" else f"{page}-{lang}.html"
        filepath = os.path.join(BASE_DIR, filename)
        
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Update Navigation Labels
        # Desktop
        desktop_nav_ul = soup.select_one('ul.nav-links')
        if desktop_nav_ul:
            for a in desktop_nav_ul.find_all('a'):
                href = a.get('href', '')
                for base_p in PAGES:
                    if href.startswith(base_p):
                        a.string = NAV_LABELS[lang][base_p]
                        break
        
        # Mobile overlay
        mobile_nav_ul = soup.select_one('ul.mobile-nav-links')
        if mobile_nav_ul:
            for a in mobile_nav_ul.find_all('a'):
                href = a.get('href', '')
                for base_p in PAGES:
                    if href.startswith(base_p):
                        a.string = NAV_LABELS[lang][base_p]
                        break

        # 2. Extract lang-switcher and move it outside <nav>
        # First, remove it from mobile overlay completely
        for ml in soup.select('.mobile-lang-switcher'):
            ml.decompose()
            
        # Find existing desktop lang-switcher
        desktop_switcher = soup.select_one('ul.nav-links .lang-switcher')
        if desktop_switcher:
            switcher_html = str(desktop_switcher)
            desktop_switcher.decompose()
        else:
            # Maybe it's already outside?
            existing_switcher = soup.select_one('.navbar > .right-controls .lang-switcher') or soup.select_one('.navbar > .lang-switcher')
            if existing_switcher:
                switcher_html = str(existing_switcher)
                existing_switcher.decompose()
            else:
                # Should not happen, but fallback
                en_file = f"{page}.html"
                de_file = f"{page}-de.html"
                fr_file = f"{page}-fr.html"
                switcher_html = f'''<div class="lang-switcher">
  <a href="{en_file}" class="{'lang-active' if lang=='en' else ''}">EN</a>
  <span class="lang-sep">/</span>
  <a href="{de_file}" class="{'lang-active' if lang=='de' else ''}">DE</a>
  <span class="lang-sep">/</span>
  <a href="{fr_file}" class="{'lang-active' if lang=='fr' else ''}">FR</a>
</div>'''

        # We want structure: 
        # <div class="navbar">
        #   <a class="nav-brand">...</a>
        #   <nav>...</nav>
        #   <div class="right-controls">
        #       <div class="lang-switcher">...</div>
        #       <button class="menu-toggle">...</button>
        #   </div>
        # </div>
        
        navbar = soup.select_one('.navbar')
        if navbar:
            menu_toggle = navbar.select_one('.menu-toggle')
            # Check if right-controls already exists
            right_controls = navbar.select_one('.right-controls')
            if not right_controls:
                right_controls = soup.new_tag('div', attrs={'class': 'right-controls'})
                # Move menu_toggle inside right_controls
                if menu_toggle:
                    toggle_copy = menu_toggle.extract()
                    # Add switcher then toggle
                    switcher_soup = BeautifulSoup(switcher_html, 'html.parser')
                    right_controls.append(switcher_soup)
                    right_controls.append(toggle_copy)
                navbar.append(right_controls)
            else:
                # Make sure switcher is inside right_controls before toggle
                for sw in right_controls.select('.lang-switcher'):
                    sw.decompose()
                switcher_soup = BeautifulSoup(switcher_html, 'html.parser')
                right_controls.insert(0, switcher_soup.div)

        # Write file back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))

print("HTML structure updated.")
