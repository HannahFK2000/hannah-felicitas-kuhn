# generate_multilingual.py
import os, re, sys

BASE_DIR = r"C:\\Users\\Hannah\\Documents\\PortfolioWebsite"
TRANSLATIONS = {
    "de": {},
    "fr": {}
}

def load_translation(lang):
    path = os.path.join(BASE_DIR, "translations", f"translation_{'german' if lang=='de' else 'french'}.md")
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    mapping = {}
    key = None
    for line in lines:
        line = line.strip()
        if line.startswith('KEY:'):
            key = line.split('KEY:')[1].strip()
        elif lang == 'de' and line.startswith('DE:') and key:
            mapping[key] = line.split('DE:')[1].strip()
            key = None
        elif lang == 'fr' and line.startswith('FR:') and key:
            mapping[key] = line.split('FR:')[1].strip()
            key = None
    return mapping

TRANSLATIONS['de'] = load_translation('de')
TRANSLATIONS['fr'] = load_translation('fr')

pages = ["index", "about", "experience", "projects", "skills", "sports", "writing", "contact"]

def replace_content(html, lang_map, page_name):
    title_key = f"{page_name}_title"
    if title_key in lang_map:
        html = re.sub(r'<title>.*?</title>', f'<title>{lang_map[title_key]}</title>', html, flags=re.I|re.S)
    hero_heading_key = f"{page_name}_hero_heading"
    if hero_heading_key in lang_map:
        html = re.sub(r'(<h1[^>]*>)(.*?)(</h1>)', rf"\1{lang_map[hero_heading_key]}\3", html, flags=re.I|re.S)
    hero_sub_key = f"{page_name}_hero_subheading"
    if hero_sub_key in lang_map:
        html = re.sub(r'(<p class=\"lead\">)(.*?)(</p>)', rf"\1{lang_map[hero_sub_key]}\3", html, flags=re.I|re.S)
    hero_body_key = f"{page_name}_hero_body"
    if hero_body_key in lang_map:
        html = re.sub(r'(<p class=\"lead\">.*?</p>\s*)(<p>)(.*?)(</p>)', rf"\1\2{lang_map[hero_body_key]}\4", html, flags=re.I|re.S)
    cta_key = f"{page_name}_hero_cta"
    if cta_key in lang_map:
        html = re.sub(r'(<a href="about\.html"[^>]*>)(.*?)(</a>)', rf"\1{lang_map[cta_key]}\3", html, flags=re.I|re.S)
    nav_map = {
        'nav_home': 'Home',
        'nav_about': 'About',
        'nav_experience': 'Experience',
        'nav_projects': 'Projects',
        'nav_skills': 'Skills',
        'nav_sports': 'Sports & Outdoors',
        'nav_writing': 'Travels & Writing',
        'nav_contact': 'Contact'
    }
    for key, en_text in nav_map.items():
        translated = lang_map.get(key, en_text)
        html = re.sub(rf'(<a href="[^"]*">){re.escape(en_text)}(</a>)', rf"\1{translated}\2", html)
    return html

def insert_lang_switcher(html, page_name, current_lang):
    en_file = f"{page_name}.html"
    de_file = f"{page_name}-de.html"
    fr_file = f"{page_name}-fr.html"
    en_class = 'lang-active' if current_lang == 'en' else ''
    de_class = 'lang-active' if current_lang == 'de' else ''
    fr_class = 'lang-active' if current_lang == 'fr' else ''
    switcher = f'''<div class="lang-switcher">
  <a href="{en_file}" class="{en_class}">EN</a>
  <span class="lang-sep">/</span>
  <a href="{de_file}" class="{de_class}">DE</a>
  <span class="lang-sep">/</span>
  <a href="{fr_file}" class="{fr_class}">FR</a>
</div>'''
    html = re.sub(r'(</li>\s*</ul>)', f'</li>\n{switcher}\n\1', html, count=1)
    html = re.sub(r'(<ul class="mobile-nav-links">)(.*?)(</ul>)', rf"\1\2{switcher}</ul>", html, flags=re.S)
    return html

css_path = os.path.join(BASE_DIR, 'css', 'styles.css')
with open(css_path, 'a', encoding='utf-8') as f:
    f.write('\n/* Language Switcher Styles */\n')
    f.write('.lang-switcher {\n  margin-left: 1rem;\n  padding-left: 1rem;\n  display: flex;\n  align-items: center;\n  gap: 0.25rem;\n  font-size: 0.85rem;\n  border-left: 1px solid var(--border-color);\n}\n.lang-switcher a { color: var(--text-color); font-weight: 400; text-decoration: none; }\n.lang-switcher a.lang-active { color: var(--accent-color); font-weight: 600; }\n.lang-switcher .lang-sep { color: var(--border-color); }\n\n/* Mobile tweaks */\n.mobile-lang-switcher .lang-switcher { border-left: none; padding-left: 0; margin-left: 0; justify-content: center; font-size: 1rem; }\n')

for page in pages:
    en_path = os.path.join(BASE_DIR, f"{page}.html")
    with open(en_path, encoding='utf-8') as f:
        en_html = f.read()
    # DE
    de_html = re.sub(r'href="([^"]+?)\.html"', r'href="\1-de.html"', en_html)
    de_html = replace_content(de_html, TRANSLATIONS['de'], page)
    de_html = insert_lang_switcher(de_html, page, 'de')
    with open(os.path.join(BASE_DIR, f"{page}-de.html"), 'w', encoding='utf-8') as f:
        f.write(de_html)
    # FR
    fr_html = re.sub(r'href="([^"]+?)\.html"', r'href="\1-fr.html"', en_html)
    fr_html = replace_content(fr_html, TRANSLATIONS['fr'], page)
    fr_html = insert_lang_switcher(fr_html, page, 'fr')
    with open(os.path.join(BASE_DIR, f"{page}-fr.html"), 'w', encoding='utf-8') as f:
        f.write(fr_html)

print('Multilingual pages generated.')
