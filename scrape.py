"""
получить доступ к ссылке
посмотреть текст ссылки = имя животного
добавить первую букву имени в словарь, если ещё нет
прибавить 1 к значению имени в словаре
повторить для всех ссылок на странице
перейти по ссылке "Следующая", если есть 
повторить процесс
сохранить результат
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


BASE_URL = "https://ru.wikipedia.org"

url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%3Cb%3E%D0%90%3C%2Fb%3E"

def get_links_from_page(url):
    response = requests.get(url)
    response.raise_for_status()  # check if request succeeded
    soup = BeautifulSoup(response.text, 'html.parser')

    links_div = soup.find('div', class_='mw-category-generated')
    links = []

    if links_div:
        a_tags = links_div.find_all('a')
        links = [a.get('href') for a in a_tags if a.get('href')]

        next_link_tag = links_div.find('a', string=lambda text: text and 'Следующая страница' in text)
        
        if next_link_tag:
            next_relative_path = next_link_tag.get('href')
            print(f"Next page link found: {next_relative_path}")
            next_absolute_url = urljoin(BASE_URL, next_relative_path)
            print(f"Next page absolute link : {next_absolute_url}")

        else:
            print("No next page link found.")
    else:
        print("No <div class='links'> found on the page.")
    
    return links, next_absolute_url

"""
def get_all_links(start_url):
    current_url = start_url
    all_links = []

    while current_url:
        print(f"Parsing: {current_url}")
        links, next_url = get_links_from_page(current_url)
        all_links.extend(links)
        current_url = next_url

    return all_links
"""

def get_all_links(start_url, max_pages=10):
    current_url = start_url
    all_links = []
    page_count = 0

    while current_url and page_count < max_pages:
        print(f"Parsing page {page_count + 1}: {current_url}")
        links, next_url = get_links_from_page(current_url)
        all_links.extend(links)
        current_url = next_url
        page_count += 1

    return all_links

# 📝 Save results to CSV
def save_links_to_csv(links, filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Animal Page URL'])  # header
        for link in links:
            full_url = urljoin(BASE_URL, link)
            writer.writerow([full_url])

# Run it
all_found_links = get_all_links(url)

save_links_to_csv(all_found_links)

print(f"\n✅ Done! {len(all_found_links)} links saved to beasts.csv")