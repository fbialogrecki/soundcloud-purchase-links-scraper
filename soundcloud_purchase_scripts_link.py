#!/usr/bin/env python3

import time
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def load_full_playlist(driver, playlist_url, pause_time=2):
    """
    Opens the playlist page and scrolls to the bottom to load all dynamic content.
    """
    driver.get(playlist_url)
    time.sleep(3)  # Initial wait for the page to load

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_track_links_from_driver(driver):
    """
    Retrieves the full HTML of the playlist page and extracts track links.
    We match URLs with the structure: https://soundcloud.com/<user>/<slug>
    where the slug is not in the reserved names list.
    """
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    track_links = set()

    # Regular expression matching a track URL:
    pattern = re.compile(r"^https://soundcloud\.com/([^/]+)/([^/?#]+)(?:[/?#]|$)")
    # List of names that are not tracks (e.g., menu items or links to other sections)
    reserved = {
        'sets', 'albums', 'tracks', 'followers', 'library', 'pages',
        'charts', 'explore', 'search', 'you', 'creators.soundcloud.com', 'blog.soundcloud.com'
    }

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith("/"):
            href = "https://soundcloud.com" + href
        match = pattern.match(href)
        if match:
            slug = match.group(2).lower()
            if slug not in reserved:
                track_links.add(href)
    return list(track_links)

def get_track_info(track_url):
    """
    Retrieves the track page and returns a tuple (title, purchase link).
    The title is extracted from the <title> tag (removing any " | SoundCloud" suffix),
    and the purchase link is searched for in <a> elements containing the phrases "buy" or "purchase".
    """
    try:
        response = requests.get(track_url)
        if response.status_code != 200:
            print(f"Could not retrieve track page: {track_url}")
            return ("Unknown title", None)
    except Exception as e:
        print(f"Error while retrieving {track_url}: {e}")
        return ("Unknown title", None)

    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract title from the <title> tag
    title = "Unknown title"
    if soup.title:
        title = soup.title.get_text().strip()
        if " | SoundCloud" in title:
            title = title.split(" | SoundCloud")[0].strip()

    purchase_link = None
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if text and any(keyword in text.lower() for keyword in ['buy', 'purchase']):
            purchase_link = a['href']
            if purchase_link.startswith('/'):
                purchase_link = 'https://soundcloud.com' + purchase_link
            break
    return (title, purchase_link)

def main():
    playlist_url = input("Enter the URL of a public SoundCloud playlist: ").strip()

    # Selenium configuration – headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    print("Loading full playlist. This may take a moment...")
    load_full_playlist(driver, playlist_url)

    print("Extracting track links from the playlist...")
    track_links = get_track_links_from_driver(driver)
    driver.quit()

    if not track_links:
        print("No track links found.")
        return

    print("\nFound tracks:")
    for track in track_links:
        print(track)

    # Open files for writing results
    with open("purchase_links.txt", "w", encoding="utf-8") as purchase_file, \
         open("not_found_purchase_links.txt", "w", encoding="utf-8") as not_found_file:
        print("\nAttempting to retrieve purchase links for tracks:")
        for track in track_links:
            title, purchase_link = get_track_info(track)
            if purchase_link:
                purchase_file.write(f"{title}: {purchase_link}\n\n")
                print(f"{track} -> {purchase_link}")
            else:
                not_found_file.write(f"{title}\n{track}\n\n")
                print(f"{track} -> No purchase link found.")

if __name__ == '__main__':
    main()