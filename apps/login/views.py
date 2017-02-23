from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    if "id" in request.session:
        return redirect('/success')
    return render(request, 'login/index.html')

def register(request):
    # Protect against a user entering in a url manually to access someone's page. Require an actual post request
    if request.method != 'POST':
        return redirect('/')
    else:
        # Set user_valid equal to what's returned by the models.py method validRegistration
        # You use request.POST instead of request because request would send potentially compromising information, like the user's ip address.
        user_valid = User.objects.validate(request.POST)   # Again, we're sending all request.POST data to our validate method in models.py
        if user_valid[0] == True:
            # user_valid is a tuple where the first element is true or false and the second element is an array of error messages
            request.session["id"] = user_valid[1].id  # Ask for the id message associated with the array
            return redirect('/success')
        else:
            # Iterate through each error message in the array stored in the second element of the user_valid tuple
            for msg in user_valid[1]:
                messages.add_message(request, messages.INFO, msg)
            return redirect('/')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        user = User.objects.authenticate(request.POST)
        if user[0] == True:
            print "%"*50, user[1].id
            request.session["id"] = user[1].id
            return redirect('/success')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect('/')

def success(request):
    # Check if user is registered
    if "id" not in request.session:   # checking for id prevents people from just entering the success url
        return redirect('/')
    try:
        # Try to grab the user object from database
        user = User.objects.get(id=request.session["id"])
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, "User not found.")
        return redirect('/')
    # If the "try" found the user object, then pass the entire object to the success page as a context (the context is the {"user":user} part, you can define the function inside the render)
    return render(request, 'login/success.html', {"user":user})

def logout(request):
    if "id" in request.session:
        request.session.pop("id")
    return redirect('/')
