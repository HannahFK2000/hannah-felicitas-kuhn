import os
import re
from bs4 import BeautifulSoup, NavigableString

BASE_DIR = r"C:\\Users\\Hannah\\Documents\\PortfolioWebsite"

PAGES = ["index", "about", "experience", "projects", "skills", "sports", "writing", "contact"]

def load_translations(lang):
    file_name = f"translation_{'german' if lang=='de' else 'french'}.md"
    path = os.path.join(BASE_DIR, "translations", file_name)
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    mapping = {}
    current_key = None
    buffer = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if stripped.startswith("KEY:"):
            if current_key and buffer:
                mapping[current_key] = "\n".join(buffer).strip()
            current_key = stripped.split("KEY:", 1)[1].strip()
            buffer = []
        elif stripped.startswith("ELEMENT:"):
            continue
        elif current_key:
            if stripped.startswith(f"{lang.upper()}:"):
                buffer.append(stripped.split(f"{lang.upper()}:", 1)[1].strip())
            else:
                if stripped != "" or buffer:
                    buffer.append(line.rstrip('\n')) 
    if current_key and buffer:
        mapping[current_key] = "\n".join(buffer).strip()
        
    return mapping

de_map = load_translations("de")
fr_map = load_translations("fr")

def replace_html_with_bs(html_content, lang_map, page_name, lang):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Update title
    title_tag = soup.find('title')
    if title_tag and f"{page_name}_title" in lang_map:
        title_tag.string = lang_map[f"{page_name}_title"]
        
    if page_name == "index":
        if "index_hero_heading" in lang_map:
            h1 = soup.select_one('.hero-content h1')
            if h1: h1.string = lang_map["index_hero_heading"]
        if "index_hero_subheading" in lang_map:
            p_lead = soup.select_one('.hero-content p.lead')
            if p_lead: p_lead.string = lang_map["index_hero_subheading"]
        if "index_hero_body" in lang_map:
            ps = soup.select('.hero-content p:not(.lead)')
            if len(ps) > 0: ps[0].string = lang_map["index_hero_body"]
        if "index_hero_closing" in lang_map:
            ps = soup.select('.hero-content p:not(.lead)')
            if len(ps) > 1: ps[1].string = lang_map["index_hero_closing"]
        if "index_hero_cta" in lang_map:
            cta = soup.select_one('.hero-content a.btn')
            if cta: cta.string = lang_map["index_hero_cta"]
            
    if page_name == "about":
        if "about_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["about_heading"]
        if "about_lead" in lang_map:
            p_lead = soup.select_one('p.lead')
            if p_lead: p_lead.string = lang_map["about_lead"]
        ps = soup.select('.section p:not(.lead)')
        for i, k in enumerate(["about_para_1", "about_para_2", "about_para_3", "about_para_4", "about_para_5"]):
            if k in lang_map and i < len(ps):
                ps[i].string = lang_map[k]
        if "about_funding_heading" in lang_map:
            h3s = soup.select('h3')
            if h3s: h3s[0].string = lang_map["about_funding_heading"]
        if "about_funding_para" in lang_map:
            h3s = soup.select('h3')
            if h3s:
                p = h3s[0].find_next_sibling('p')
                if p: p.string = lang_map["about_funding_para"]
        if "about_download_cv" in lang_map:
            a = soup.select_one('a.btn[download]')
            if a:
                svg = a.find('svg')
                a.clear()
                if svg: a.append(svg)
                a.append(NavigableString(" " + lang_map["about_download_cv"]))
                
    if page_name == "experience":
        if "experience_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["experience_heading"]
        if "experience_lead" in lang_map:
            p = soup.select_one('p.lead')
            if p: p.string = lang_map["experience_lead"]
        
        cards = soup.select('.card')
        for i, prefix in enumerate(["exp_davis", "exp_rwanda", "exp_universum", "exp_bachelor"]):
            if i < len(cards):
                c = cards[i]
                if f"{prefix}_title" in lang_map:
                    h3 = c.select_one('h3')
                    if h3: h3.string = lang_map[f"{prefix}_title"]
                if f"{prefix}_meta" in lang_map:
                    meta = c.select_one('p.meta')
                    if meta: meta.string = lang_map[f"{prefix}_meta"]
                if f"{prefix}_body" in lang_map:
                    body = c.select_one('p:not(.meta)')
                    if body: body.string = lang_map[f"{prefix}_body"]
        if "exp_download_cv" in lang_map:
            a = soup.select_one('a.btn[download]')
            if a:
                svg = a.find('svg')
                a.clear()
                if svg: a.append(svg)
                a.append(NavigableString(" " + lang_map["exp_download_cv"]))

    if page_name == "projects":
        if "projects_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["projects_heading"]
        if "projects_lead" in lang_map:
            p = soup.select_one('p.lead')
            if p: p.string = lang_map["projects_lead"]
        
        cards = soup.select('.card')
        for i, prefix in enumerate(["proj_thesis", "proj_inclusive"]):
            if i < len(cards):
                c = cards[i]
                if f"{prefix}_title" in lang_map:
                    h3 = c.select_one('h3')
                    if h3: h3.string = lang_map[f"{prefix}_title"]
                if f"{prefix}_meta" in lang_map:
                    meta = c.select_one('p.meta')
                    if meta: meta.string = lang_map[f"{prefix}_meta"]
                if f"{prefix}_body" in lang_map:
                    body = c.select_one('p:not(.meta)')
                    if body: body.string = lang_map[f"{prefix}_body"]
        
        if "proj_thesis_methodology" in lang_map:
            h4 = soup.select_one('h4')
            if h4: h4.string = lang_map["proj_thesis_methodology"]
        
        bullets = [lang_map.get(f"proj_thesis_bullet_{i}") for i in range(1,4)]
        lis = soup.select('main ul > li')
        for i, b in enumerate(bullets):
            if b and i < len(lis):
                lis[i].string = b.lstrip('- ')

    if page_name == "skills":
        if "skills_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["skills_heading"]
        if "skills_lead" in lang_map:
            p = soup.select_one('p.lead')
            if p: p.string = lang_map["skills_lead"]
        
        cats = soup.select('.skill-category')
        for i, prefix in enumerate(["skills_lab", "skills_software", "skills_field"]):
            if i < len(cats):
                c = cats[i]
                if f"{prefix}_heading" in lang_map:
                    h3 = c.select_one('h3')
                    if h3: h3.string = lang_map[f"{prefix}_heading"]
                if f"{prefix}_items" in lang_map:
                    items_str = lang_map[f"{prefix}_items"]
                    items = [x.lstrip('- ').strip() for x in items_str.split('\n') if x.strip() and x.strip().startswith('-')]
                    lis = c.select('li')
                    for j, item in enumerate(items):
                        if j < len(lis): lis[j].string = item

    if page_name == "sports":
        if "sports_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["sports_heading"]
        if "sports_lead" in lang_map:
            p = soup.select_one('p.lead')
            if p: p.string = lang_map["sports_lead"]
            
        cards = soup.select('.card')
        for i, prefix in enumerate(["sports_hockey", "sports_martial", "sports_hiking"]):
            if i < len(cards):
                c = cards[i]
                if f"{prefix}_heading" in lang_map:
                    h3 = c.select_one('h3')
                    if h3: h3.string = lang_map[f"{prefix}_heading"]
                if f"{prefix}_body" in lang_map:
                    body = c.select_one('p')
                    if body: body.string = lang_map[f"{prefix}_body"]

    if page_name == "writing":
        if "writing_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["writing_heading"]
        if "writing_lead" in lang_map:
            p = soup.select_one('p.lead')
            if p: p.string = lang_map["writing_lead"]
        if "writing_body" in lang_map:
            ps = soup.select('.section p:not(.lead)')
            if ps: ps[0].string = lang_map["writing_body"]
        if "writing_selected_heading" in lang_map:
            h3 = soup.select_one('h3')
            if h3: h3.string = lang_map["writing_selected_heading"]
        if "writing_platforms_intro" in lang_map:
            ps = soup.select('.section p:not(.lead)')
            if len(ps) > 1: ps[1].string = lang_map["writing_platforms_intro"]

    if page_name == "contact":
        if "contact_heading" in lang_map:
            h1 = soup.select_one('h1')
            if h1: h1.string = lang_map["contact_heading"]
        if "contact_lead" in lang_map:
            p = soup.select_one('p.lead')
            if p: p.string = lang_map["contact_lead"]
            
        h3s = soup.select('h3')
        if "contact_email_heading" in lang_map and len(h3s) > 0: h3s[0].string = lang_map["contact_email_heading"]
        if "contact_network_heading" in lang_map and len(h3s) > 1: h3s[1].string = lang_map["contact_network_heading"]
        if "contact_resume_heading" in lang_map and len(h3s) > 2: h3s[2].string = lang_map["contact_resume_heading"]
        
        if "contact_linkedin_button" in lang_map:
            a = soup.select_one('a.btn[target="_blank"]')
            if a:
                svg = a.find('svg')
                a.clear()
                if svg: a.append(svg)
                a.append(NavigableString(" " + lang_map["contact_linkedin_button"]))
                
        if "contact_download_button" in lang_map:
            a = soup.select_one('a.btn-outline[download]')
            if a:
                svg = a.find('svg')
                a.clear()
                if svg: a.append(svg)
                a.append(NavigableString(" " + lang_map["contact_download_button"]))


    # Global Elements: Navbar & Footer
    nav_map = {
        'index.html': 'nav_home',
        'about.html': 'nav_about',
        'experience.html': 'nav_experience',
        'projects.html': 'nav_projects',
        'skills.html': 'nav_skills',
        'sports.html': 'nav_sports',
        'writing.html': 'nav_writing',
        'contact.html': 'nav_contact'
    }
    
    # Update navigation links and all other a tags ending in .html
    for a in soup.select('a'):
        href = a.get('href', '')
        if href.endswith('.html'):
            base_href = re.sub(r'-(de|fr)\.html', '.html', href)
            # update href for language
            if lang != "en":
                new_href = base_href.replace('.html', f'-{lang}.html')
                a['href'] = new_href

            # Update nav link text
            if a.parent and (a.parent.name == 'li' and (a.parent.parent.has_attr('class') and ('nav-links' in a.parent.parent['class'] or 'mobile-nav-links' in a.parent.parent['class']))):
                if base_href in nav_map:
                    key = nav_map[base_href]
                    if key in lang_map:
                        a.string = lang_map[key]
                        
    # Ensure active class is correctly applied based on the page_name
    for a in soup.select('.nav-links a, .mobile-nav-links a'):
        href = a.get('href', '')
        if href == f"{page_name}-{lang}.html":
            a['class'] = a.get('class', []) + ['active']
        else:
            if 'active' in a.get('class', []):
                a['class'].remove('active')

    # Footer translations
    if "footer_copyright" in lang_map:
        f_p = soup.select_one('.footer-info p')
        if f_p: f_p.string = lang_map["footer_copyright"]
    
    if "footer_download" in lang_map:
        f_a = soup.select_one('.footer-links a[download]')
        if f_a:
            svg = f_a.find('svg')
            f_a.clear()
            if svg: f_a.append(svg)
            f_a.append(NavigableString(" " + lang_map["footer_download"]))
            
    return str(soup)

def insert_switcher(html_content, page_name, current_lang):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    en_file = f"{page_name}.html"
    de_file = f"{page_name}-de.html"
    fr_file = f"{page_name}-fr.html"
    
    en_class = 'lang-active' if current_lang == 'en' else ''
    de_class = 'lang-active' if current_lang == 'de' else ''
    fr_class = 'lang-active' if current_lang == 'fr' else ''

    switcher_html = f'''<div class="lang-switcher">
  <a href="{en_file}" class="{en_class}">EN</a>
  <span class="lang-sep">/</span>
  <a href="{de_file}" class="{de_class}">DE</a>
  <span class="lang-sep">/</span>
  <a href="{fr_file}" class="{fr_class}">FR</a>
</div>'''

    # Remove any existing switchers to prevent duplicates
    for sw in soup.select('.lang-switcher'):
        sw.decompose()
        
    for ml in soup.select('.mobile-lang-switcher'):
        ml.decompose()

    switcher_soup_desktop = BeautifulSoup(switcher_html, 'html.parser')
    
    # Desktop: insert after Contact link
    ul_desktop = soup.select_one('ul.nav-links')
    if ul_desktop:
        ul_desktop.append(switcher_soup_desktop)
        
    # Mobile overlay: insert inside mobile-lang-switcher container
    mobile_switcher_html = f'<div class="mobile-lang-switcher">{switcher_html}</div>'
    switcher_soup_mobile = BeautifulSoup(mobile_switcher_html, 'html.parser')
    
    ul_mobile = soup.select_one('ul.mobile-nav-links')
    if ul_mobile:
        ul_mobile.parent.append(switcher_soup_mobile)
        
    # Pretty print the switcher area slightly or just let BS format
    # BS4 encode with formatter minimal
    return str(soup)


for page in PAGES:
    en_path = os.path.join(BASE_DIR, f"{page}.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        en_html = f.read()
        
    # We should make sure en_html doesn't already have switchers applied if we run this multiple times.
    # The insert_switcher removes old switchers anyway.
    
    # 1. Update English version (just add switcher)
    new_en_html = insert_switcher(en_html, page, 'en')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(new_en_html)
        
    # 2. Update German version
    de_html = replace_html_with_bs(en_html, de_map, page, 'de')
    de_html = insert_switcher(de_html, page, 'de')
    with open(os.path.join(BASE_DIR, f"{page}-de.html"), 'w', encoding='utf-8') as f:
        f.write(de_html)
        
    # 3. Update French version
    fr_html = replace_html_with_bs(en_html, fr_map, page, 'fr')
    fr_html = insert_switcher(fr_html, page, 'fr')
    with open(os.path.join(BASE_DIR, f"{page}-fr.html"), 'w', encoding='utf-8') as f:
        f.write(fr_html)

print("HTML generation complete.")

# CSS Update
css_path = os.path.join(BASE_DIR, 'css', 'styles.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Remove previous switcher styles
css_content = re.sub(r'/\* Language Switcher Styles \*/.*?\.mobile-lang-switcher \.lang-switcher \{.*?\}', '', css_content, flags=re.S)

new_css = '''
/* Language Switcher Styles */
.lang-switcher {
  margin-left: 1rem;
  padding-left: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  border-left: 1px solid var(--border-color);
  flex-wrap: nowrap;
  white-space: nowrap;
}
.lang-switcher a { color: var(--text-color); font-weight: 400; text-decoration: none; }
.lang-switcher a.lang-active { color: var(--accent-color); font-weight: 600; }
.lang-switcher .lang-sep { color: var(--border-color); }

.mobile-lang-switcher {
  border-top: 1px solid var(--border-color); 
  padding-top: 1rem; 
  margin-top: 1rem;
  width: 100%;
  display: flex;
  justify-content: center;
}

/* Mobile tweaks */
.mobile-lang-switcher .lang-switcher { 
  border-left: none; 
  padding-left: 0; 
  margin-left: 0; 
  justify-content: center; 
  font-size: 1rem; 
}
'''

if '/* Language Switcher Styles */' not in css_content:
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_content.strip() + '\n' + new_css)
        
print("CSS updated.")
