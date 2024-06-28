from bs4 import BeautifulSoup
import requests
import pandas as pd


quotes = []
authors = []


for pages in range(1, 10 + 1):
    quotes_url = f"http://quotes.toscrape.com/page/{pages}/"
    response = requests.get(quotes_url)
    quotes_web_page = response.text
    soup = BeautifulSoup(quotes_web_page, "html.parser")
    quote_all = soup.find_all(name='span', class_='text')
    for quote in quote_all:
        x = quote.getText()
        quotes.append(x)
    author_all = soup.find_all('small', class_='author')
    for author in author_all:
        y = author.getText()
        authors.append(y)


data = {
    'author': authors,
    'quotes': quotes
}

df = pd.DataFrame(data)

df.to_csv("quote_list.csv", index=False)

