import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
url = "https://pokemondb.net/pokedex/all"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing Pokémon data
table = soup.find('table', class_='data-table')

# Initialize lists to store data
pokemon_data = []

# Extract data from each row in the table
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    pokemon_info = {
        'Pokedex Number': cols[0].text.strip(),
        'Name': cols[1].text.strip(),
        'Type': cols[2].find_all('a')[0].text.strip(),
        'Total': cols[3].text.strip(),
        'HP': cols[4].text.strip(),
        'Attack': cols[5].text.strip(),
        'Defense': cols[6].text.strip(),
        'Sp. Atk': cols[7].text.strip(),
        'Sp. Def': cols[8].text.strip(),
        'Speed': cols[9].text.strip(),
    }
    pokemon_data.append(pokemon_info)

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(pokemon_data)

# Save DataFrame to CSV
df.to_csv('pokemon_data.csv', index=False)

# Display the first few rows of the DataFrame
print(df.head())
