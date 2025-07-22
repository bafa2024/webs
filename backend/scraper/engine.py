import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Minimal scraping engine

def scrape_page(url, save_dir, options=None):
    options = options or {}
    os.makedirs(save_dir, exist_ok=True)
    # Setup Selenium
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Save HTML
    html_path = os.path.join(save_dir, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    # Download assets
    asset_tags = {
        'img': 'src',
        'link': 'href',
        'script': 'src',
    }
    assets_downloaded = 0
    for tag, attr in asset_tags.items():
        for el in soup.find_all(tag):
            src = el.get(attr)
            if not src:
                continue
            asset_url = urljoin(url, src)
            parsed = urlparse(asset_url)
            ext = os.path.splitext(parsed.path)[1]
            if tag == 'img':
                subdir = 'images'
            elif tag == 'link' and ext in ['.css']:
                subdir = 'css'
            elif tag == 'script' and ext in ['.js']:
                subdir = 'js'
            else:
                subdir = 'other'
            asset_dir = os.path.join(save_dir, 'assets', subdir)
            os.makedirs(asset_dir, exist_ok=True)
            filename = os.path.basename(parsed.path) or f'asset{assets_downloaded}{ext}'
            asset_path = os.path.join(asset_dir, filename)
            try:
                r = requests.get(asset_url, timeout=10)
                with open(asset_path, 'wb') as af:
                    af.write(r.content)
                assets_downloaded += 1
            except Exception:
                continue
    driver.quit()
    return {
        'html_path': html_path,
        'assets_downloaded': assets_downloaded,
        'status': 'completed',
    } 