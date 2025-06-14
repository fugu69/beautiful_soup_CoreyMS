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


BASE_URL = "https://ru.wikipedia.org"

url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%3Cb%3E%D0%90%3C%2Fb%3E"

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
        next_relative_path = next_link_tag.get('href')
        print(f"Next page link found: {next_relative_path}")
        next_absolute_url = urljoin(BASE_URL, next_relative_path)
        print(f"Next page absolute link : {next_absolute_url}")

    else:
        print("No next page link found.")
else:
    print("No <div class='links'> found on the page.")