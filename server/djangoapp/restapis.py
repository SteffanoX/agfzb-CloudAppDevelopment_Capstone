import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
         response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
         response = requests.post(url, params=kwargs, json=json_payload)
         results = response.status_code
         print("With status {} ".format(results))
        # If any error occurs
    except:
        print("Network exception occurred")
        results = "Network exception occured"

    return results


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer state from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
            NLU_sentiment = analyze_review_sentiments(review["review"])
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], 
                         review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"], 
                         car_model=review["car_model"], car_year=review["car_year"], sentiment=NLU_sentiment, id=review['id'])
            results.append(review_obj)
    
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text): 
    url = "" 
    api_key = "" 
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    try:
        response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
        label=json.dumps(response, indent=2) 
        label = response['sentiment']['document']['label']
    except:
        label='neutral' 
    return(label) 
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative


