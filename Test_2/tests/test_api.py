
import pytest
import requests
import random
import string

BASE_URL = "https://qa-internship.avito.com"

def random_seller_id():
    return random.randint(111111, 999999)

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

@pytest.fixture
def new_ad():
    data = {
        "sellerID": random_seller_id(),
        "name": random_string(),
        "price": 1000,
        "statistics": {
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=data)
    response.raise_for_status()
    return response.json()

def test_create_ad_success():
    data = {
        "sellerID": random_seller_id(),
        "name": random_string(),
        "price": 1000,
        "statistics": {
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=data)
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["name"] == data["name"]
    assert resp_json["price"] == data["price"]

def test_create_ad_missing_name():
    data = {
        "sellerID": random_seller_id(),
        "price": 1000,
        "statistics": {
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=data)
    assert response.status_code == 400

def test_get_ad_by_id(new_ad):
    ad_id = new_ad["id"]
    response = requests.get(f"{BASE_URL}/api/1/item/{ad_id}")
    assert response.status_code == 200
    resp_json = response.json()
    assert any(ad["id"] == ad_id for ad in resp_json)

def test_get_ad_invalid_id():
    response = requests.get(f"{BASE_URL}/api/1/item/invalid_id")
    assert response.status_code == 404

def test_get_ads_by_seller(new_ad):
    seller_id = new_ad["sellerId"]
    response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
    assert response.status_code == 200
    resp_json = response.json()
    assert all(ad["sellerId"] == seller_id for ad in resp_json)

def test_get_statistic_success(new_ad):
    ad_id = new_ad["id"]
    response = requests.get(f"{BASE_URL}/api/2/statistic/{ad_id}")
    assert response.status_code == 200
    stats = response.json()
    assert isinstance(stats, list)
    assert "likes" in stats[0]

def test_get_statistic_invalid_id():
    response = requests.get(f"{BASE_URL}/api/2/statistic/invalid_id")
    assert response.status_code == 404

def test_delete_ad_success(new_ad):
    ad_id = new_ad["id"]
    response = requests.delete(f"{BASE_URL}/api/2/item/{ad_id}")
    assert response.status_code == 200

def test_delete_ad_invalid_id():
    response = requests.delete(f"{BASE_URL}/api/2/item/invalid_id")
    assert response.status_code == 404
