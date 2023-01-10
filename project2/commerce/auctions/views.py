from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing


def index(request):
    # get all the data from model Listing
    L = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "auctions" : L 
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    '''
    create new Listing
    '''
    if request.method == 'POST':
       title = request.POST["title"]
       des = request.POST["description"]
       bid = int(request.POST["bid"])
       url = request.POST["url"]
       category = request.POST["category"]
       u = request.POST["user"]
       user = User.objects.filter(username=u).first()

       # add listing to data!
       L = Listing(owner=user, title=title, des=des, bid=bid, url=url, category=category)
       L.save()

       return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/create.html')

def product(request, name):
    if request.method == 'POST':
        # get bids 
        bid = int(request.POST["bid"])
        last_bid = int(request.POST["last_bid"])
        # if curent bid bigger than the last bid
        if bid > last_bid:
            o = (request.POST["owner"])
            # get user
            user = User.objects.filter(username=o).first()
            # change bid 
            Listing.objects.filter(title=name, owner=user).update(bid=bid, last_bid='moshe4631') # צריך להוסיף שינוי של מי שקנה אחרון (צריך את בעל החשבון)
            return HttpResponse("You offered the highest price")
        else:
            return HttpResponse("your bid is smaller or equal the curent bid")
    else:
        # לחשוב איך להשיג את השם של בעל החשבון בשביל לדעת מי נכנס למוצר 
        owner = ''
        buyer = ''
        # get the product that blong to the user 
        t_o = name.split(".")
        user = User.objects.filter(username=t_o[1]).first()
        product = Listing.objects.filter(title=t_o[0], owner=user)
        '''
        get the owner of the product
        for i in product:
           owner = i.owner
        '''
        # check if someone buy, if so buyer = True
        for i in product:
            if i.last_bid != "No one offered":
                buyer = True

        return render(request, 'auctions/Listing.html', {
            "product" : product, "owner" : owner, "buyer" : buyer
        })


