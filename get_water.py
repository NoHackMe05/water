import requests
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
STORE_ENDPOINT = os.getenv('STORE_ENDPOINT')

def add_api_key(row):
    row['api_key'] = API_KEY
    return row

def save_to_database(df):
    """
    Sends the data to a PHP script to be saved in a MySQL database.

    Args:
        df (DataFrame): The data to be saved.
    """
    data = [add_api_key(record) for record in df.to_dict(orient='records')]

    for row in data:
        print(f"Data : {row}")

        # Envoyer la requête
        response = requests.post(STORE_ENDPOINT, data=row)
        if response.status_code == 200:
          result = response.json()
          if 'success' in result:
              print(f"Data successfully recorded : {row}")
          else:
              print(f"Error sending data: {result.get('error')}")
        else:
            print(f"Error sending data: {response.status_code}")

if __name__ == "__main__":
    # Définir la requête Overpass
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:csv(::id, ::lat, ::lon, "name", "amenity")];
    area["name"="France"]->.searchArea;
    (
      node["amenity"="drinking_water"](area.searchArea);
      node["natural"="water"](area.searchArea);
      node["waterway"="riverbank"](area.searchArea);
    );
    out body;
    """

    # Envoyer la requête
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.text

    # Sauvegarder les données dans un fichier CSV
    with open('points_deau.csv', 'w') as f:
        f.write(data)

    # Charger et vérifier les données avec Pandas
    df = pd.read_csv('points_deau.csv', sep='\t', quotechar='"', encoding='utf-8')
    save_to_database(df)
