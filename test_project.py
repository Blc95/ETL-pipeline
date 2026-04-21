from project import fetch_crypto_data, transform_crypto_data, load_crypto_data_to_psql

def test_fetch_crypto_data():
    data = fetch_crypto_data()
    assert data is not None

