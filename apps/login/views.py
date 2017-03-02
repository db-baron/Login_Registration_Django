from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Friend, Other

# Create your views here.
def index(request):
    if "user_id" in request.session:   # request is an object and session is a dictonary type attribute of request
        return redirect('/profile')
    return render(request, 'login/index.html')

def registration(request):
    print "@"*50, request.POST['dob']

    # Protect against a user entering in a url manually to access someone's page. Require an actual post request
    if request.method != 'POST':
        print "Registration is POST only"
        return redirect('/')
    else:
        # Set reg_validate equal to what's returned by the validate method in models.py
        # You use request.POST because just 'request' alone would send potentially compromising information, like the user's ip address.
        reg_validate = User.objects.validate(request.POST)   # Send all request.POST data to validate method in models.py
        if reg_validate[0] == True:
            # reg_validate is a tuple where reg_validate[0] is either a true or false and reg_validate[1] is an array of error messages
            request.session["user_id"] = reg_validate[1].id  # Ask for the id message associated with the array
            print "reg_validate[1].id = ", reg_validate[1].id
            return redirect('/profile')
        else:
            # Iterate through each error message in the array stored in the second element of the reg_validate tuple
            for msg in reg_validate[1]:
                messages.add_message(request, messages.INFO, msg)
            return redirect('/')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        login_authenticate = User.objects.authenticate(request.POST)
        if login_authenticate[0] == True:
            print "login_authenticate[1].id = ", login_authenticate[1].id
            request.session["user_id"] = login_authenticate[1].id
            return redirect('/profile')
        else:
            messages.add_message(request, messages.INFO, login_authenticate[1])
            return redirect('/')

def profile(request):
    # Checking for id prevents people from just entering the profile url
    if "user_id" not in request.session:
        return redirect('/')
    # Try to grab the friend object from database
    try:
        userid = User.objects.get(id=request.session["user_id"])
        friends = Friend.friendMan.filter(friends=userid)
        print "#"*50, friends
        others = Friend.objects.exclude(friends=userid)
        print "*"*50, others
        context = {
            'friends':friends,
            'others': others
        }
        return render(request, 'login/profile.html', context)
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, "Error: User not found.")
        return redirect('/')

def addFriend(request):
    if request.method != 'POST':
        print "Method must be a POST"
        return redirect('/')
    else:
        friend_valid = Friend.friendMan.validfriend(request.session['user_id'], request.POST)
        if friend_valid[0] == False:
            return False, "validfriend returned False"
        print "friend_valid = ", friend_valid
        if friend_valid[0] == True:
            request.session["user_id"] = reg_validate[1].id  # Ask for the id message associated with the array
            print "reg_validate[1].id = ", reg_validate[1].id
            return redirect('/profile')
        return redirect('/profile', context)

def logout(request):
    if "user_id" in request.session:
        request.session.pop("user_id")
    return redirect('/')
