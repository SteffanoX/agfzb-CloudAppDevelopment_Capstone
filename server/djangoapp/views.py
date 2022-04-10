from time import strptime
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_state_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime, date
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method =='POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exists = False
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            logger.debug(f"{username} is a new user")
        
        if not user_exists:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
    else:
        return render(request, 'onlinecourse/user_registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://e5334bd3.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealerships"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


def get_dealerships_state(request, state):
    if request.method == "GET":
        url = "https://e5334bd3.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealer_by_state_from_cf(url, state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id, dealer_name):
    if request.method == "GET":
        context = {}
        url = "https://e5334bd3.eu-gb.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["dealership_name"] = dealer_name
        context["dealer_id"] = dealer_id
        context["reviews"] = reviews
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id, dealer_name):
    if request.user.is_authenticated:
        if request.method == "POST":
            url = 'https://e5334bd3.eu-gb.apigw.appdomain.cloud/api/review'
            review = {}
            json_payload = {}
            review['id'] = 1000
            review["name"] = request.user.first_name + " " + request.user.last_name
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            review["purchase"] = True if 'purchasecheck' in request.POST else False
            if review["purchase"] == True:
                date_obj = datetime.strptime(request.POST['purchasedate'], '%Y-%m-%d')
                review["purchase_date"] = str(date_obj.strftime('%m/%d/%Y'))
                if request.POST['car'] != 'nil':
                    purchased_car = get_object_or_404(CarModel, pk=request.POST['car'])
                    review["car_make"] = purchased_car.car_make.name
                    review["car_model"] = purchased_car.name
                    review["car_year"] = str(purchased_car.year.strftime('%Y'))
                else:
                    review["car_make"] = 'Not spcified'
                    review["car_model"] = 'Not spcified'
                    review["car_year"] = 'Not spcified'
            else:
                review["purchase_date"] = 'nil'
                review["car_make"] = 'nil'
                review["car_model"] = 'nil'
                review["car_year"] = 'nil'

            json_payload["review"] = review
            response = post_request(url, json_payload, dealerId=dealer_id)
            print(response)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id, dealer_name=dealer_name)
        
        elif request.method == "GET":
            context = {}
            cars = CarModel.objects.filter(dealer_id = dealer_id)
            context["cars"] = cars
            context["dealer_id"] = dealer_id
            context["dealer_name"] = dealer_name
            return render(request, 'djangoapp/add_review.html', context)



