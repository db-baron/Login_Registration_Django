from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
from django.contrib import messages
import bcrypt, re

NAME_REGEX = re.compile (r'^[a-z A-Z]+$')

# For later extending our manager 'objects' to include a new method
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []  # Create an array of error messages
        # postData['name'] comes from the request gotten from views.py registration function
        if len(postData['name']) < 2 or len(postData['alias']) < 2:
            errors.append("Name and Alias must be between 2 and 45 characters.")
        elif not NAME_REGEX.match(postData['name']):
            errors.append("Name can not contain non-letters.")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData['confirm']:
            errors.append("Password does not match Confirmation Password")
        if len(postData["email"]) == 0:
            errors.append("Please enter an email address.")
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$', postData["email"]):
            errors.append("Invalid email address.")
        elif len(User.objects.filter(email=postData["email"])) > 0:
            errors.append("Email address is already registered.")
        try:
            # strptime() parses a string representing a time according to a format and returns a struct_time as returned by gmtime() or localtime(), meaning a tuple of 9 integeres.
            dob = datetime.strptime(postData["dob"], "%m/%d/%Y")
            print "dob"*100, dob
        except ValueError:
            errors.append("Invalid date of birth entered. Use M/D/YYYY format.")
        else:
            if datetime.now() < dob:
                errors.append("Future date of birth entered.")
        if len(errors) == 0:
            # This is where the new user object is created
            user = User.objects.create(name=postData["name"], alias=postData["alias"], \
            pw_hash=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
            return (True, user)
            # if no error, the method returns the tuple (success code, user object)
        else:
            return (False, errors)
            # if at least one error, the method returns the tuple (failure, error list)
    def authenticate(self, postData):
        if "alias" in postData and "password" in postData:
            try:
                user = User.objects.get(alias=postData["alias"])
            except User.DoesNotExist:
                return (False, "Invalid user name/password combination.")
            pw_match = bcrypt.hashpw(postData['password'].encode(),user.pw_hash.encode())
            if pw_match:
                return (True, user)
            else:
                return (False, "Invalid user name/password combination.")
        else:
            return (False, "Please enter login info.")

class AddFriendManager(models.Manager):
    def validfriend(self, user_id, postData):
        print "************ Validation for the new friend **************"
        if len(User.objects.filter(friends=postData["email"])) > 0:
            errors.append("That person is already your friend.")
        try:
            current_user = User.objects.get(id=user_id)
            print "current_user is ", current_user
            friend = Friend.objects.create(user=current_user, )
            print "friend is ", friend
            return (True, friend)
        except:
            return (False, "Could not add this friend")

class Friend(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friendMan = AddFriendManager()

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    dob = models.DateTimeField()
    password = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ForeignKey(Friend)
    objects = UserManager()

class Other(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
