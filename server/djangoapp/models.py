from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
# - Name
    name = models.CharField(null=False, max_length=30)
# - Description
    description = models.CharField(null=True, max_length=500)
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
    def __str__(self):
        return "name: " + self.name + ", " + \
               "description: " + self.description


class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
# - Name
    name = models.CharField(null=False, max_length=30)
# - Dealer id, used to refer a dealer created in cloudant database
    dealer_id = models.IntegerField()
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    SEDAN, SUV, WAGON, COUPE = 'Sedan', 'SUV', 'Wagon', 'Coupe'
    car_type_options = [
        (SEDAN, 'Sedan'), (SUV, 'SUV'), 
        (WAGON, 'Wagon'), (COUPE, 'Coupe')
        ]
    car_type = models.CharField(null=False, max_length=20, choices=car_type_options, default=SEDAN)
# - Year (DateField)
    year = models.DateField(null=True)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
    def __str__(self):
        return "Model Name: " + self.name + "," + \
               "Dealer ID: " + str(self.dealer_id) + "," + \
               "Car Type: " + self.car_type + "," + \
               "year: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
