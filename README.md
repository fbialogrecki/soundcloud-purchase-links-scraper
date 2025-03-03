# SoundCloud Purchase Links Scraper

This repository contains a Python tool that automates the process of extracting purchase links from public SoundCloud playlists. The script dynamically loads the entire playlist using Selenium, then parses the page to extract individual track URLs. For each track, it retrieves the track page and searches for a purchase link based on keywords (such as "buy", "purchase", or "kup").

## Features

- **Dynamic Loading:** Automatically scrolls through a SoundCloud playlist to load all tracks.
- **Track Extraction:** Uses BeautifulSoup with a regex filter to accurately extract track URLs.
- **Purchase Link Detection:** Fetches each track's page via requests and scans for purchase links by analyzing link text.
- **Output Files:**
  - `purchase_links.txt` – Contains the track title and its corresponding purchase link (if found).
  - `not_found_purchase_links.txt` – Contains the track title and URL for tracks without a purchase link.

## Requirements

- Python 3.x
- [Selenium](https://www.selenium.dev/) (with a compatible WebDriver such as ChromeDriver)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests](https://docs.python-requests.org/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/soundcloud-purchase-links-scraper.git
   cd soundcloud-purchase-links-scraper

   ```

2. Install the required dependencies using pip:

   ```bash
   pip install selenium beautifulsoup4 requests

   ```

3. Ensure your WebDriver (e.g., ChromeDriver) is installed and properly set up in your PATH.

## Usage

Run the script using Python:

```bash
python soundcloud_purchase_scripts_link.py
```

or run it as bash script (if you work on linux operating system)

```bash
./soundcloud_purchase_scripts_link.py
```

When prompted, enter the URL of the public SoundCloud playlist. The script will process the playlist and create two output files:

- purchase_links.txt
- not_found_purchase_links.txt

## License

This project is licensed under the Apache License. See the LICENSE file for details.
