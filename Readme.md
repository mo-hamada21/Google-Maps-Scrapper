# 🗺️ Google Maps Review Scraper & Analyzer

This project allows you to **scrape, clean, and analyze reviews** from **Google Maps** automatically.  
It includes both a **command-line scraper** and a **desktop GUI interface** for collecting and analyzing reviews using **Selenium**, **Tkinter**, and **CAMeL Tools**.

---

## 🚀 Features

- ✅ Scrape reviews directly from any **Google Maps place URL**
- 🧭 Automatically sorts reviews by **newest first**
- 🧹 **Cleans and normalizes text** in both Arabic and English
- 🧠 Detects **languages and Arabic dialects** using [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools)
- ✍️ **Auto-corrects English text** using [TextBlob](https://textblob.readthedocs.io)
- 📊 Built-in **GUI interface** for scraping and analysis:
  - Filter by keywords, language, and time period  
  - Export filtered results to CSV  
  - Load and analyze previously saved reviews
- 💾 Save both **original** and **processed** reviews as `.csv` files

---

## 📁 Project Structure

```
📦 google-maps-review-analyzer
├── google_maps_scraper.py      # CLI-based scraper with text preprocessing
├── review_analyzer_gui.py      # Tkinter GUI for scraping and analysis
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

---

## 🧩 Requirements

- **Python 3.8+**
- **Google Chrome** (latest version)
- **ChromeDriver** that matches your Chrome version

### Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` file yet, install these manually:

```bash
pip install selenium textblob langdetect camel-tools pandas
```

> 📝 Note: `tkinter` usually comes pre-installed with Python on most systems.

---

## ⚙️ ChromeDriver Setup

1. Open Chrome and check your version:  
   - Go to `chrome://settings/help`
2. Download the matching **ChromeDriver**:  
   👉 https://chromedriver.chromium.org/downloads  
3. Add it to your system PATH or place it in the same folder as this project.

---

## 🧾 Command-Line Scraper Usage

Run the scraper directly from your terminal or command prompt:

```bash
python google_maps_scraper.py
```

You’ll be prompted to:
- Enter the Google Maps place URL  
- Choose the number of reviews to scrape  
- Optionally run preprocessing tests  
- Save the results to a CSV file

Example session:

```
Enter the Google Maps place URL: https://www.google.com/maps/place/Mall+of+Riyadh
Enter the number of reviews to scrape: 100
```

### Output Files
- `processed_reviews.csv` — cleaned, normalized, and language-processed data  
- `original_reviews.csv` — raw scraped data (optional)

---

## 💻 GUI Application

You can also use the graphical interface for scraping and analysis:

```bash
python review_analyzer_gui.py
```

### GUI Tabs

#### 🕵️ Scrape Reviews Tab
- Paste a Google Maps URL  
- Choose number of reviews  
- Click **Start Scraping**  
- Save or use the reviews for analysis  

#### 📈 Analyze Reviews Tab
- Load an existing `.csv` file or use scraped data  
- Filter by:
  - Keywords
  - Language (English, Arabic, or Mixed)
  - Time period (e.g., last 30 days)
- Export filtered results to a new `.csv` file

---

## 🌐 Language & Text Processing

The text processor in `google_maps_scraper.py` includes:

- **Arabic normalization**:
  - Removes diacritics
  - Normalizes different forms of Alef and Teh Marbuta
  - Identifies Arabic dialects using CAMeL Tools
- **English correction**:
  - Uses TextBlob for grammar and spelling correction
  - Includes confidence checks to avoid false corrections
- **Mixed text handling**:
  - Detects and processes both Arabic and English content
  - Avoids errors on common terms like:
    - “mall”, “brands”, “halal”, “nice”, etc.

---

## 🧠 Example Workflow

1. Run the GUI:
   ```bash
   python review_analyzer_gui.py
   ```
2. Paste the Google Maps place link and scrape 100 reviews  
3. Save results to `reviews.csv`  
4. Switch to the **Analyze Reviews** tab  
5. Apply filters such as:
   - Keyword: `service, price`
   - Language: `English only`
   - Time Period: `Last 30 days`
6. Export filtered insights to a new CSV file

---

## 🧰 Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|-----------|
| `selenium.common.exceptions.WebDriverException` | ChromeDriver mismatch | Ensure ChromeDriver matches your Chrome version |
| `ModuleNotFoundError` | Missing library | Run `pip install -r requirements.txt` |
| Arabic text unreadable | Encoding issue | Open CSV with UTF-8 encoding (script uses `utf-8-sig`) |
| GUI not opening | Tkinter not installed | Ensure `tkinter` is available for your Python build |
| CAMeL Tools warning | Missing optional dependency | Run `pip install camel-tools` |

---

## 🧑‍💻 Author

**Your Name**  
📧 *[youremail@example.com]*  
💻 Built with ❤️ using Python, Selenium, and Tkinter.

---

## 📜 License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it for personal or commercial purposes.

---

## ⭐ Acknowledgements

- [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) — Arabic NLP toolkit  
- [TextBlob](https://textblob.readthedocs.io) — English text processing  
- [Selenium](https://www.selenium.dev) — Web automation and scraping  
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI library for Python  
- [Google Maps](https://maps.google.com) — Review data source  

---

## 🧾 Example Output (CSV)

| name           | date         | rating   | text                                                                  |
|----------------|--------------|----------|-----------------------------------------------------------------------|
| Sarah Smith    | 2 days ago   | 5 stars  | Excellent mall with great food options.                               |
| محمد الأحمد    | 3 weeks ago  | 4 stars  | المول زين بس الأسعار شوي غالية.                                     |
| John Doe       | 1 month ago  | 3 stars  | Good location but crowded on weekends.                                |

---

## 🏁 Quick Start Summary

```bash
# Clone this repository
git clone https://github.com/yourusername/google-maps-review-analyzer.git
cd google-maps-review-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the command-line scraper
python google_maps_scraper.py

# OR launch the GUI
python review_analyzer_gui.py
```

---

✨ **Enjoy scraping, cleaning, and analyzing Google Maps reviews with ease!**
