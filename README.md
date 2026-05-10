# 📡 Telegram Scraping & Traffic Analysis

> A research toolkit for monitoring, scraping, and simulating Telegram channel traffic — built for network traffic analysis and covert communication research.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green?logo=selenium&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-HTML%20Parsing-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🔍 Overview

This project provides a suite of Python tools to **scrape messages from public Telegram channels** via `web.telegram.org` and **simulate realistic message traffic** for research purposes. It was developed as part of a study on network behavior and traffic fingerprinting in encrypted messaging platforms.

The toolkit includes:
- Two scraping approaches (static HTML parsing and dynamic browser automation)
- A realistic message sender that simulates human-like behavior with mixed media types
- A Jupyter notebook for traffic modeling and analysis

---

## 📁 Project Structure

```
Telegram_scraping/
│
├── beautifulsoup.py              # Static scraper using requests + BeautifulSoup
├── selen_scrape.py               # Dynamic scraper using Selenium WebDriver
├── selen_scroll.py               # Selenium helper for auto-scrolling through chat history
├── telegram_txt_sender.py        # Automated message sender with mixed media simulation
├── telegram_text_only_sender.py  # Text-only version of the message sender
├── model 7.ipynb                 # Jupyter notebook: traffic analysis & modeling
└── README.pdf                    # Original documentation
```

---

## ⚙️ Features

### 🕷️ Message Scraping

| Module | Method | Dynamic? | Notes |
|---|---|---|---|
| `beautifulsoup.py` | HTTP + HTML parsing | ❌ | Lightweight; limited by Telegram's JS rendering |
| `selen_scrape.py` | Chrome WebDriver | ✅ | Handles dynamic content; extracts message ID, sender, timestamp, reply context |
| `selen_scroll.py` | Chrome WebDriver | ✅ | Auto-scrolls to load full chat history |

**What gets extracted:**
- Message ID
- Sender name
- Timestamp (Unix epoch)
- Message text
- Reply context (detects if a message is a reply and extracts the quoted content)

---

### 📤 Traffic Simulation

`telegram_txt_sender.py` simulates realistic Telegram traffic by sending randomized messages of varying types at randomized intervals. All activity is logged to a timestamped CSV file.

**Message types & probabilities:**

| Type | Probability | Details |
|---|---|---|
| Text | ~35.6% | Random alphanumeric strings, exponential length distribution |
| Image | ~58.1% | Random noise images (PNG), size between 2.4 KB – 378 KB |
| Voice | ~6.1% | gTTS-generated audio from random text |

**Timing:** Messages are sent at random intervals drawn from an exponential distribution (mean ~60s, capped at 600s), mimicking realistic human usage patterns.

**Output:** A CSV file (`telegram_messages<timestamp>.csv`) with columns:
```
time, size, message_type
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install requests beautifulsoup4 selenium gtts moviepy opencv-python numpy
```

You'll also need:
- [Google Chrome](https://www.google.com/chrome/) installed
- [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version, added to your system PATH

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/GiladFisher/Telegram_scraping.git
   cd Telegram_scraping
   ```

2. **Log in to Telegram Web** in your Chrome browser before running any Selenium-based scripts. The scripts open `web.telegram.org` and require an active session.

3. **Configure the target channel** by editing the `url` variable in the script you want to run:
   ```python
   url = 'https://web.telegram.org/k/#@your_channel_name'
   ```

---

## 🧪 Usage

### Scrape messages with Selenium

```bash
python selen_scrape.py
```

Launches Chrome, navigates to the target channel, waits for content to load, then extracts and prints all visible messages.

### Scrape messages with BeautifulSoup

```bash
python beautifulsoup.py
```

Attempts a static HTTP request to the Telegram Web page. Note: due to JavaScript rendering, this approach has limited effectiveness on modern Telegram Web.

### Simulate message traffic

```bash
python telegram_txt_sender.py
```

Opens a Chrome browser pointed at a target Telegram group, then continuously sends randomized messages (text, images, voice) at randomized intervals. Logs all sent messages to a CSV file.

---

## 📊 Analysis Notebook

`model 7.ipynb` contains the traffic analysis and modeling work, including:
- Statistical analysis of message size distributions
- Traffic pattern modeling
- Visualization of scraped data

Open it with Jupyter:
```bash
jupyter notebook "model 7.ipynb"
```

---

## ⚠️ Disclaimer

This project was developed for **academic and research purposes only**. Please ensure you:
- Only scrape **public** Telegram channels you have permission to access
- Comply with [Telegram's Terms of Service](https://telegram.org/tos)
- Do not use this tool to harass, spam, or violate the privacy of any individual

---

## 🛠️ Tech Stack

- **Python 3.8+**
- [Selenium](https://www.selenium.dev/) — browser automation
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [gTTS](https://gtts.readthedocs.io/) — text-to-speech for voice message simulation
- [OpenCV](https://opencv.org/) — image generation
- [MoviePy](https://zulko.github.io/moviepy/) — video processing
- [NumPy](https://numpy.org/) — numerical distributions for realistic traffic modeling
- [Jupyter Notebook](https://jupyter.org/) — data analysis

---

## 👤 Author

**Gilad Fisher** — [GitHub](https://github.com/GiladFisher)

---

*Feel free to open an issue or pull request if you'd like to contribute or report a bug.*
