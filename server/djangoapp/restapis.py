import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    print("API Key {} ".format(api_key))
    try:
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        #print("HELLO {}".format(url))
        # Get the row list in JSON as dealers
        #dealers = json_result["rows"]
        dealers = json_result["docs"]
        #print(dealers)
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as reviews
        try:
            reviews = json_result["docs"]
            # For each review object
            for review in reviews:
                # Get its content in `doc` object
                review_doc = review
                print(review_doc["purchase"])
                if review_doc["purchase"]:
                    # Create a Carreview object with values in `doc` object
                    print("true proc")
                    review_obj = DealerReview(dealership=review_doc["dealership"],name=review_doc["name"], purchase=review_doc["purchase"],
                                        review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                        car_model=review_doc["car_model"], car_year=review_doc["car_year"],
                                        id=review_doc["id"])
                else:
                    print("false proc")
                    review_obj = DealerReview(dealership=review_doc["dealership"],name=review_doc["name"], purchase=review_doc["purchase"],
                                        review=review_doc["review"],purchase_date=None, car_make=None,
                                        car_model=None, car_year=None,
                                        id=review_doc["id"])
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)

                results.append(review_obj)
        except:
            print("No reviews")

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    result = "Not checked"
    print(text)
    try:
        json_result = get_request(url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/33ff96b2-e89e-4491-87c8-fa17d7a0d035",
                        api_key="ZGY4CrSXyOfZxvw7I7KddddyKFlyru8XkKxc3yFL4Oat",
                        version="2021-03-25",
                        features="sentiment",
                        language="en",
                        text=text)
        result = json_result["sentiment"]["document"]["label"]
        print(result)
    finally:
        return result

