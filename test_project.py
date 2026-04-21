from project import fetch_crypto_data, transform_crypto_data, load_crypto_data_to_psql


def test_fetch_crypto_data():
    data = fetch_crypto_data(1, 10)
    assert data is not None
def test_transform_crypto_data():
    fake_data = {
        "status": {"timestamp": "2026-01-01T00:00:00Z"},
        "data": [
            {
                "id": 1,
                "name": "Bitcoin",
                "symbol": "BTC",
                "date_added": "2010-01-01",
                "max_supply": 21000000,
                "quote": {
                    "USD": {
                        "price": 50000,
                        "volume_24h": 1000,
                        "market_cap": 900000000,
                        "market_cap_dominance": 50
                    }
                }
            }
        ]
    }

    result = transform_crypto_data(fake_data)

    assert isinstance(result, list)
    assert result[0]["symbol"] == "BTC"
    

def test_transform_returns_correct_keys():
    fake_data = {
        "status": {"timestamp": "2026-01-01T00:00:00Z"},
        "data": [{
            "id": 1,
            "name": "Bitcoin",
            "symbol": "BTC",
            "date_added": "2010-01-01",
            "max_supply": 21000000,
            "quote": {
                "USD": {
                    "price": 1,
                    "volume_24h": 1,
                    "market_cap": 1,
                    "market_cap_dominance": 1
                }
            }
        }]
    }

    result = transform_crypto_data(fake_data)

    expected_keys = {
        "fetched_at", "coin_id", "name", "symbol",
        "date_added", "max_supply", "price_in_usd",
        "volume_24h", "market_cap", "market_cap_dominance"
    }

    assert set(result[0].keys()) == expected_keys