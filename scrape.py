from bs4 import BeautifulSoup as bs
import requests
import csv
import requests.compat

"""
def get_links_from_page(url):
    source = requests.get(url).text

    soup = bs(source, "lxml")

    animals_links_div = soup.find("div", class_="mw-category-generated")
    links_on_page = [a.get("href") for a in animals_links_div.find_all('a')]

    next_link_tag = animals_links_div.find("a", string="Следующая страница")
    next_link = next_link_tag.get("href") if next_link_tag else None

    return links_on_page, next_link

def get_all_links(start_url):
    current_url = start_url
    all_links = []

    while current_url:
        print(f"Parsing: {current_url}")
        links, next_link = get_links_from_page(current_url)
        all_links.extend(links)

        if next_link:
            current_url = requests.compat.urljoin(current_url, next_link)
        else:
            current_url = None

    return all_links


# print(animals_table.prettify())
"""
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
"""

import requests
from bs4 import BeautifulSoup

def get_links_from_page(url):
    res = requests.get(url)
    res.raise_for_status()  # raise error if not 200 OK

    soup = BeautifulSoup(res.text, 'html.parser')

    # Find div with class 'links'
    links_div = soup.find('div', class_='links')
    if not links_div:
        return [], None

    # Extract all <a> tags inside this div
    links = [a.get('href') for a in links_div.find_all('a')]

    # Find the "Next" link inside this div (or somewhere else if needed)
    next_link_tag = links_div.find('a', string='Next')
    next_link = next_link_tag.get('href') if next_link_tag else None

    return links, next_link


def get_all_links(start_url):
    current_url = start_url
    all_links = []

    while current_url:
        print(f"Parsing: {current_url}")
        links, next_link = get_links_from_page(current_url)
        all_links.extend(links)

        if next_link:
            # If next_link is relative, build absolute URL
            current_url = requests.compat.urljoin(current_url, next_link)
        else:
            current_url = None

    return all_links


# Example usage:
start_url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%3Cb%3E%D0%90%3C%2Fb%3E"
all_parsed_links = get_all_links(start_url)
print("All links:", all_parsed_links)

"""

import requests
from bs4 import BeautifulSoup

url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%3Cb%3E%D0%90%3C%2Fb%3E"  # Replace with your actual URL

response = requests.get(url)
response.raise_for_status()  # check if request succeeded

soup = BeautifulSoup(response.text, 'html.parser')

# Find the div with class 'links'
links_div = soup.find('div', class_='mw-category-generated')

if links_div:
    # Find all <a> tags inside that div
    a_tags = links_div.find_all('a')

    # Extract href attributes from all found <a> tags
    links = [a.get('href') for a in a_tags if a.get('href')]

    print("Links found inside <div class='links'>:")
    for link in links:
        print(link)

    # Check if a "Next page" link exists
    # Let's check for an <a> tag with text containing 'Next' (case-insensitive)
    next_link_tag = links_div.find('a', string=lambda text: text and 'Следующая страница' in text)
    
    if next_link_tag:
        next_link = next_link_tag.get('href')
        print(f"Next page link found: {next_link}")
    else:
        print("No next page link found.")
else:
    print("No <div class='links'> found on the page.")