from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    dealership_list = []
    if request.method == "GET":
        url = "https://4a9f7d39.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context["dealership_list"] = dealerships
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://4a9f7d39.us-south.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        dealer_details = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        # Concat all dealer's short name
        #dealer_details_reviews = ' '.join([dealer_detail.sentiment for dealer_detail in dealer_details])
        context["review_list"] = dealer_details
        context["dealer_id"] = dealer_id
        # Return a list of dealer short name
        #return HttpResponse(dealer_details_reviews)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        print("GET add_review")
        context["dealer_id"] = dealer_id
        context["cars"] = CarModel.objects.all()
        print(CarModel.objects.all())
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        sessionid = request.COOKIES.get('sessionid')
        if sessionid is None:
            return HttpResponseForbidden("Not Authorized: please login to post reviews")
        print("POST add_review")
        form = request.POST
        user = User.objects.get(username=request.user)
        # prepare json_payload to post
        review = dict()
        review['id'] = user.pk
        review['name'] = user.first_name + " " + user.last_name
        review['dealership'] = dealer_id
        review['review'] = form["content"]
        review['purchase'] = bool(form.get("purchasecheck"))
        review['id'] = 99
        #review['review'] = request.POST['review']
        
        if form.get("purchasecheck"):
            review["purchase_date"] = datetime.strptime(form.get("purchase_date"), "%m/%d/%Y").isoformat()
            # payload if uer purchased a car
            review['purchase'] = True
            if review['purchase_date'] == "":
                # check a date has been selected
                print('Review not posted: please insert purchase date')
                messages.add_message(request, messages.WARNING, \
                    'Review not posted: please insert purchase date')
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            try:
                # dealer must sell cars in order to leave a review for a purchase
                #car_id = request.POST['carInformation']
                #print('car_id:{}'.format(car_id))
                
                purchased_car = CarModel.objects.get(pk=form["car"])
                #purchased_car = CarModel.objects.get(pk=car_id)             
                review['car_make'] = purchased_car.maker.name
                review['car_model'] = purchased_car.name
                review['car_year'] = purchased_car.year.strftime("%Y")
            except:
                print('Review not posted: dealer sells no car')
                messages.add_message(request, messages.WARNING, \
                    'Review not posted: dealer sells no car, cannot post \
                    reviews for purchases')
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            # payload if user did not purchase a car
            review['purchase'] = False
        
        review_json = dict()
        review_json['review']= review
        print(review_json)

        url="https://4a9f7d39.us-south.apigw.appdomain.cloud/api/review"

        json_result = post_request(url, review_json, dealer_id=dealer_id)
        print("---json_result---")
        print(json_result)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)