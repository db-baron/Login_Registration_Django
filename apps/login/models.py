from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
from django.contrib import messages
import bcrypt, re

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile (r'^[a-zA-Z]+$')

# For later extending our manager 'objects' to include a new method
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []  # Create an array of error messages
        if postData['first_name'] == "First Name" or len(postData['first_name']) < 1:
            errors.append("Please enter a first name.")
        elif len(postData["first_name"]) < 2:
            errors.append("First name must be between 2 and 45 characters.")
        if postData['last_name'] == "Last Name" or len(postData['last_name']) < 1:
            errors.append("Please enter a last name.")
        elif len(postData["last_name"]) < 2:
            errors.append("Last name must be between 2 and 45 characters.")
        elif not NAME_REGEX.match(postData['first_name'] or postData['last_name']):
            errors.append("Names can not contain non-letters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email must be a valid address.")
        if len(User.objects.filter(email = postData['email'])) > 0:
			errors.append("Email address has already been registered.")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData['confirm']: # check that password matches the password confirmation
            errors.append("Password does not match Confirmation Password")
        try:
            # method strptime breaks date into elements of a tuple as so:
            # time.strptime("30 Nov 00", "%d %b %y") would return (2000, 11, 30, 0, 0, 0, 3, 335, -1)
            dob = datetime.strptime(postData["dob"], "%m/%d/%Y")  # dob is a datetime object
        except ValueError:
            errors.append("Invalid date of birth entered. Use M/D/YYYY format.")
        else:
            if datetime.now() < dob:
                errors.append("Future date of birth entered.")
        # If there were no errors
        if len(errors) == 0:
            # Here is where the new user object is actually created
            user = User.objects.create(first_name=postData["first_name"], last_name=postData["last_name"], email=postData["email"],\
            dob=dob,pw_hash=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            return (True, user)
            # if no error, the method returns the tuple (success code, user object)
        else:
            return (False, errors)
            # if at least one error, the method returns the tuple (failure, error list)


    def authenticate(self, postData):
        if "email" in postData and "password" in postData:
            try:
                user = User.objects.get(email=postData["email"])
            except User.DoesNotExist:
                return (False, "Invalid email/password combination.")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid email/password combination.")
        else:
            return (False, "Please enter login info.")


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    dob = models.DateTimeField()
    pw_hash = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
