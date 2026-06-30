import os
import glob
from bs4 import BeautifulSoup

BASE_DIR = r"C:\\Users\\Hannah\\Documents\\PortfolioWebsite"
html_files = glob.glob(os.path.join(BASE_DIR, "*.html"))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Fix German START label
    if filepath.endswith('-de.html'):
        for nav_container in soup.select('ul.nav-links, ul.mobile-nav-links'):
            for a in nav_container.find_all('a'):
                if a.string and "STARTSEITE" in a.string:
                    a.string = a.string.replace("STARTSEITE", "START")
                    
    # 2. Fix lang-switcher labels
    switchers = soup.select('.lang-switcher')
    for switcher in switchers:
        links = switcher.find_all('a')
        if len(links) == 3:
            links[0].string = "EN"
            links[1].string = "DE"
            links[2].string = "FR"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print("Text fixes applied.")
