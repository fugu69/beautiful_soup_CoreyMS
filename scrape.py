import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


BASE_URL = "https://ru.wikipedia.org"

url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%3Cb%3E%D0%90%3C%2Fb%3E"


def get_links_from_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    links_div = soup.find('div', class_='mw-category mw-category-columns')
    next_link_div = soup.find('div', class_='mw-category-generated')

    links = []
    next_absolute_url = None

    if links_div:
        a_tags = links_div.find_all('a')
        links = [a.get('href') for a in a_tags if a.get('href')]

    if next_link_div:
        next_link_tag = next_link_div.find('a', string=lambda text: text and 'Следующая страница' in text)
        if next_link_tag:
            next_relative_path = next_link_tag.get('href')
            next_absolute_url = urljoin(BASE_URL, next_relative_path)
            print(f"➡️ Next page found: {next_absolute_url}")
        else:
            print("⛔ No next page link found.")
    else:
        print("⛔ No <div class='mw-pages'> found on the page.")

    return links, next_absolute_url

def get_all_links(start_url):
    current_url = start_url
    all_links = []
    page_count = 0

    while current_url:
        print(f"🔄 Parsing page {page_count + 1}: {current_url}")
        links, next_url = get_links_from_page(current_url)
        all_links.extend(links)
        current_url = next_url
        page_count += 1

    print(f"✅ Finished! Parsed {page_count} pages.")
    
    letter_count = {}
    for link in all_links:
        name = link.split('/')[-1]
        if name:
            name = requests.utils.unquote(name)
            first_letter = name[0].upper()
            if first_letter.isalpha():
                letter_count[first_letter] = letter_count.get(first_letter, 0) + 1

    return letter_count


def save_counts_to_csv(counts_dict, filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Letter', 'Count'])  # header
        for letter, count in sorted(counts_dict.items()):
            writer.writerow([letter, count])

letter_counts = get_all_links(url)
save_counts_to_csv(letter_counts)
print(f"\n✅ Done! Letter frequency saved to beasts.csv")
