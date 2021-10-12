from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model
class CarMake(models.Model)
    name = models.CharField(null=False, max_length=30, default='Car Make')
    description = models.CharField(max_length=1000)
   

    def __str__(self):
        return "Car Model: " + self.name + "," + \
               "Description: " + self.description



class CarModel(models.Model):
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
