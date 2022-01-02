import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("Get from {} ".format(url))
    try:
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("network exception error")
    status_code = response.status_code
    print("With Status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city = dealer_doc["city"], full_name = dealer_doc["full_name"], id = dealer_doc["id"],lat=dealer_doc["lat"], long=dealer_doc["long"], short_name= dealer_doc["short_name"], st=dealer_doc["st"], zip= dealer_doc["zip"])
            result.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results =[]
    json_result = get_request(url, dealerId = dealerId)
    if json_result:
        if 'entries' in json_result:
            reviews = json_result['entries']
            results = [DealerReview(id=review['id'], car_make=(review['car_make'] if 'car_make' in review else None), car_model=(review['car_model'] if 'car_model' in review else None), car_year=(review['car_year'] if 'car_year' in review else None), dealership=review['dealership'], name=review['name'], purchase=(review['purchase'] if 'purchase' in review else None), purchase_date=(review['purchase_date'] if 'purchase_date' in review else None), review=review['review'], sentiment=analyze_review_sentiments(review['review'])) for review in reviews]
    return results
        

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    result = "Not checked"
    print(text)
    try:
        json_result = get_request(url="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/48b966aa-b98c-44f7-a78f-78e8e01e8b88/v1/analyze",
                        api_key="rw0nKSLh7V9Wvlff_jYmMTmzgS1rjzVIL-OkJj1BrDpC",
                        version="2021-03-25",
                        features="sentiment",
                        language="en",
                        text=text)
        result = json_result["sentiment"]["document"]["label"]
        print(result)
    finally:
        return result


