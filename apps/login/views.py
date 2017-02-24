from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    if "user_id" in request.session:
        return redirect('/success')
    return render(request, 'login/index.html')

def registration(request):
    # Protect against a user entering in a url manually to access someone's page. Require an actual post request
    if request.method != 'POST':
        return redirect('/')
    else:
        # Set user_valid equal to what's returned by the validate method in models.py
        # You use request.POST because just 'request' alone would send potentially compromising information, like the user's ip address.
        user_valid = User.objects.validate(request.POST)   # Send all request.POST data to validate method in models.py
        if user_valid[0] == True:
            # user_valid is a tuple where the first element is true or false and the second element is an array of error messages
            request.session["user_id"] = user_valid[1].id  # Ask for the id message associated with the array
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
            request.session["user_id"] = user[1].id
            return redirect('/success')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect('/')

def success(request):
    # Check if user is registered
    if "user_id" not in request.session:   # checking for id prevents people from just entering the success url
        return redirect('/')
    try:
        # Try to grab the user object from database
        user = User.objects.get(id=request.session["user_id"])
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, "User not found.")
        return redirect('/')
    # If the "try" found the user object, then pass the entire object to the success page as a context (the context is the {"user":user} part, you can define the function inside the render)
    return render(request, 'login/success.html', {"user":user})

def showDestination(request, id):
    destination = Trip.tripMan.filter(id=id)
    context ={
        'destination':destination[0].trips.all()
    }
    return render(request, 'login/destination.html', context)

def addTrip(request):
    if request.method == 'GET':
        print "Method must be a POST"
        return redirect('/')
    trip = Trip.tripMan.validtrip(user_id, trip_id)
    if not trip['valid']:
        messages.error(request, trip['msg'])
    return redirect('/home')

def showTrip(request, id):
    user = User.objects.filter(id=id)
    context = {
        'profile' : user[0].destinations.all()
    }
    return render(request, 'login/addplan.html', context)

def home(request):
    return render(request, 'login/home.html')

def logout(request):
    if "user_id" in request.session:
        request.session.pop("user_id")
    return redirect('/')
