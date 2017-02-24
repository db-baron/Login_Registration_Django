from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
from django.contrib import messages
import bcrypt, re

NAME_REGEX = re.compile (r'^[a-zA-Z]+$')

# For later extending our manager 'objects' to include a new method
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []  # Create an array of error messages
        if postData['name'] == "Name" or len(postData['name']) < 4:
            errors.append("Please enter a valid name.")
        elif len(postData["name"]) < 4:
            errors.append("Name must be between 4 and 45 characters.")
        if postData['user_name'] == "Username" or len(postData['user_name']) < 4:
            errors.append("Please enter a valid username.")
        elif len(postData["user_name"]) < 4:
            errors.append("Username must be between 4 and 45 characters.")
        elif not NAME_REGEX.match(postData['name']):
            errors.append("Name can not contain non-letters.")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData['confirm']:
            errors.append("Password does not match Confirmation Password")
        # If there were no errors
        if len(errors) == 0:
            # Here is where the new user object is actually created
            user = User.objects.create(name=postData["name"], user_name=postData["user_name"], \
            pw_hash=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            return (True, user)
            # if no error, the method returns the tuple (success code, user object)
        else:
            return (False, errors)
            # if at least one error, the method returns the tuple (failure, error list)

    def authenticate(self, postData):
        if "user_name" in postData and "password" in postData:
            try:
                user = User.objects.get(user_name=postData["user_name"])
            except User.DoesNotExist:
                return (False, "Invalid user name/password combination.")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid user name/password combination.")
        else:
            return (False, "Please enter login info.")

class AddPlanManager(models.Manager):
    def validtrip(self, user_id, trip_id):
        this_user = User.objects.get(id=user_id)
        this_trip = Trip.tripMan.get(id=trip_id)
        if this_user in this_trip.user.all() :
            return {'valid': False, 'msg': "You've added this trip already."}
        else:
            this_user.trips.add(this_trip)
            return {'valid': True}


class User(models.Model):
    name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    user = models.ForeignKey(User, related_name="trips")
    destination = models.CharField(max_length=45)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tripMan = AddPlanManager()
