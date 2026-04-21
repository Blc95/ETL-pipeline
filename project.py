from requests import Session
import psycopg2
import os
import sys
import logging


from dotenv import load_dotenv
load_dotenv()

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


### EXTRACT ###
def fetch_crypto_data(start, limit):
  api_key = os.getenv("CMC_API_KEY")
  
  if not api_key:
    raise ValueError("Error: CMC_API_KEY is not set in the environment.")

  url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
  parameters = {
      "start": start,
      "limit": limit,
      "convert": "USD"
  }
  headers = {
      "Accepts": "application/json",
      "X-CMC_PRO_API_KEY": api_key,
  }
  
  session = Session()
  session.headers.update(headers)

  response = session.get(url, params=parameters)
  response.raise_for_status()
  data = response.json()
      
  return data

### TRANSFORM ###
def transform_crypto_data(data):
  
  list_of_dicts = []

  fetched_at = data["status"]["timestamp"]

  for coin in data["data"]:
      row = {
          "fetched_at": fetched_at,
          "coin_id": coin["id"],
          "name": coin["name"],
          "symbol": coin["symbol"],
          "date_added": coin["date_added"],
          "max_supply": coin["max_supply"],
          "price_in_usd": coin["quote"]["USD"]["price"],
          "volume_24h": coin["quote"]["USD"]["volume_24h"],
          "market_cap": coin["quote"]["USD"]["market_cap"],
          "market_cap_dominance": coin["quote"]["USD"]["market_cap_dominance"],
      }
      list_of_dicts.append(row)
  return list_of_dicts



### LOAD ###
def load_crypto_data_to_psql(list_of_dicts):
  connection = None
  cursor = None
  
  user = os.getenv("DB_USER")
  password = os.getenv("DB_PASSWORD")
  host = os.getenv("DB_HOST")
  port = os.getenv("DB_PORT")
  database = os.getenv("DB_NAME")
  


  try:
    connection = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO crypto_prices (
        fetched_at,
        coin_id,
        name,
        symbol,
        date_added,
        max_supply,
        price_in_usd,
        volume_24h,
        market_cap,
        market_cap_dominance
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (coin_id, fetched_at) DO NOTHING
    """

    for row in list_of_dicts:
        values = (
            row["fetched_at"],
            row["coin_id"],
            row["name"],
            row["symbol"],
            row["date_added"],
            row["max_supply"],
            row["price_in_usd"],
            row["volume_24h"],
            row["market_cap"],
            row["market_cap_dominance"],
        )
        cursor.execute(insert_query, values)

    connection.commit()
    logging.info("Rows inserted successfully.")
    
  finally:
    if cursor is not None:
        cursor.close()
    if connection is not None:
        connection.close()
        logging.info("PostgreSQL connection is closed")

def main():
    try:
        logging.info("Starting extract")
        data = fetch_crypto_data(1, 10)

        logging.info("Starting transform")
        list_of_dicts = transform_crypto_data(data)

        logging.info("Starting load")
        load_crypto_data_to_psql(list_of_dicts)

        logging.info("Pipeline completed successfully")

    except Exception as e:
        logging.exception(f"Pipeline failed: {e}")
        sys.exit(1)

    
            

if __name__ == "__main__":
  main()