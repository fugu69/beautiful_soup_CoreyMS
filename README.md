# 🐾 Wikipedia Animal Parser

A Python web scraper that collects links to animal pages from Russian Wikipedia, grouped by the first letter of each animal's name.

## 📌 Features

- Crawls through all "Animals by Alphabet" pages on [ru.wikipedia.org](https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту)
- Follows pagination automatically via "Следующая страница" links
- Extracts animal names and groups them by their first letter
- Saves the frequency of animals per starting letter to a CSV file (`beast_counts.csv`)

---

## 🧰 Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `csv`
- `lxml`

Install dependencies:

```bash
pip install requests beautifulsoup4 csv lxml
```

---

🚀 How to Run

```bash
python scrape.py
```

This will:

- Start from the A-section of animals.
- Parse every page until no more "Next" links exist.
- Count how many animal names start with each letter.
- Save the result to beast_counts.csv.

---

📊 Output Format (CSV)
The output file contains two columns:
| Letter | Count |
| ------ | ----- |
| А      | 122   |
| Б      | 98    |
| ...    | ...   |

---

💡 Future Ideas
- Visualize results with bar charts
- Add command-line options (e.g., limit pages, output format)

---

📎 Notes
Wikipedia uses UTF-8 URL encoding (e.g. %D0%90 → А). This script decodes it automatically.

Only animal names starting with a letter are counted (non-alphabet characters are ignored).

---

🐍 Author - Maximus Brutalis
Made with Python, curiosity, and coffee ☕

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
Feel free to use, modify, and distribute it as you like, with attribution.