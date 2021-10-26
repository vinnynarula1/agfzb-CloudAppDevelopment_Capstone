from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model

class CarMake(models.Model):
    name = models.CharField(null=False,max_length=1000)
    description = models.CharField(max_length=3000)
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description


class CarModel(models.Model):

    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False,max_length=1000)
    dealer_id = models.IntegerField()
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    type_choices = [(SEDAN, 'Sedan'),(SUV, 'SUV'),(WAGON, 'Wagon'),(HATCHBACK, 'Hatchback')]
    car_type = models.CharField(null=False,choices=type_choices,max_length=1000)
    year = models.DateField()
    def __str__(self):
        return "Name: " + self.name + ", " + "Type: " + self.car_type + ', ' + 'Year: ' + str(self.year)
    

# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        #Dealer address
        self.address= address
        #Dealer City
        self.city = city
        #Dealer full name
        self.full_name = full_name
        #Dealer id
        self.id = id
        #Dealer lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer Name: " +self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, name, purchase, purchase_date, review, sentiment):
        self.car_make= car_make
        #Dealer car model
        self.car_model = car_model
        #Dealer car year
        self.car_year = car_year
        #Dealer name
        self.dealership = dealership
        #Dealer name
        self.name = name
        # Location purchase
        self.purchase = purchase
        # Dealer purchase_date
        self.purchase_date = purchase_date
        # Dealer review
        self.review = review
        # Dealer zip
        self.sentiment  = sentiment
    def __str__(self):
        return "Dealership: " + self.dealership
