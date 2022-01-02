from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarMake, CarModel
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

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
            get_dealerships({'method': 'GET'})
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    context = {}
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
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
            logger.debug("{} does not exist".format(username))
        # If it is a new user
        if not user_exist:
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://4a9f7d39.us-south.apigw.appdomain.cloud/api/dealership"

        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealer_id):
    context={}
    url = "https://4a9f7d39.us-south.apigw.appdomain.cloud/api/review"
    dealer_details = get_dealer_reviews_from_cf(url,dealer_id)
    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    context = {}
    url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/8250ba8602120a229d380bfa5ca46392fb0731b5f751bb87a2a87530555b43ad/djangoapp/api/review"
    context["dealer_id"] = dealer_id

    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            review = {}
            review["id"] = 0
            review["name"] = request.POST["name"]
            review["dealership"] = dealer_id
            review["review"] = request.POST["review"]

            review["purchase"] = request.POST["purchase"]
            review['purchase_date'] = request.POST['purchase_date'] or "Nil"
            review["car_model"] = request.POST["car_model"] or "Nil"
            review["car_make"] = request.POST["car_make"] or "Nil"
            review["car_year"] = request.POST["car_year"] or "Nil"
            json_payload = {"review": review}
            send_review_to_cf(url, json_payload)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)