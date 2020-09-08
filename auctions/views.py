from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Auction, Bid, Comment, Favorite
from .forms import *



def index(request):
    form = FilterByCategories()
    
    return render(request, "auctions/index.html", {
        'auctions': Auction.objects.all().order_by("-id"),
        'form': form,
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



@login_required
def new_auction(request):
    form = NewAuction(request.POST or None)

    # create new auction form control
    if request.method == "POST" and form.is_valid():

        data = form.cleaned_data

        Auction.objects.create(
                    name=str(request.user),
                    title=data["title"],
                    desc=data["desc"],
                    price=data["price"],
                    category=data["category"],
                    image=data["image"],
                )

        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/newauction.html', {
        'form': form
    })



def auction_details(request, auction_id):
    
    # Get auction by id
    auction = Auction.objects.get(id=auction_id)

    result=""
    
    #heart red or heart gray
    try:
        auction.auctionhere.get(fk_user=request.user.id)
        isfav = True
    except:
        isfav = False
    
    # form for new bid
    if request.method == "POST":
        bid = request.POST["bid"]

        # am i the creator of this auction?
        if auction.name == str(request.user):
            result = "You cannot bid on your own auction"

        # am i the last bidder?
        if auction.bidshere.all().exists() and auction.bidshere.all().latest().name == str(request.user):
            result = "You cannot improve your own offer"
        
        else:
            
            # is the bid largest than the initial? then, go to the labyrinth
            if int(bid) > int(auction.price):
                try:
                    
                    # everything is alright? is my bid largest than the previous? then go!
                    if int(bid) > int(auction.bidshere.all().latest().bid):
                        Bid.objects.create(
                            bid=bid,
                            name=str(request.user),
                            fk_auctions=auction
                        )
                        result = "Your offer has been successful!"
                    
                    # else, not go
                    else:
                        result = "The offer must be largest than the last offer"
                
                # if it is the first offer, the conditions fail, and it is assumed that there are no offers 
                # this except takes care of that
                except:
                    Bid.objects.create(
                            bid=bid,
                            name=str(request.user),
                            fk_auctions=auction
                        )
                    result = "Your offer has been successful!"
            
            # your bid is lowest than the inital
            else:
                result = "Your bid must be largest than the initial bid"

    return render(request, "auctions/auctiondetails.html", {
        "auction": auction,
        "result": result,
        "isfav": isfav,
    })



@login_required
def fun_new_comment(request):

    comment = request.POST["comment"]
    id = request.POST["id"]

    # get the object by id
    auctioner = Auction.objects.get(id=id)
    auction_id = auctioner.id

    # create new comment
    Comment.objects.create(
            name = str(request.user),
            comment = comment,
            fk_auctions = auctioner,
        )

    return HttpResponseRedirect(reverse("auctiondetails", args=(auction_id,)))



@login_required
def favorites(request):

    # render favs page
    return render(request, "auctions/favorites.html", {
        "favs": Favorite.objects.filter(fk_user=request.user).order_by("-id"),
    })



@login_required
def fun_favorites(request):

    # add the auction to favorites
    if request.method == 'POST':
        id = Auction.objects.get(id=request.POST["id"])
        if Favorite.objects.filter(fk_user=request.user, fk_auction=id).exists():
            Favorite.objects.filter(fk_user=request.user, fk_auction=id).delete()
        else:
            Favorite.objects.create(fk_user=request.user,fk_auction=id)
        
        return HttpResponseRedirect(reverse("auctiondetails", args=(id.id,)))

    return HttpResponseRedirect(reverse('index'))



@login_required
def fun_close_auction(request):

    # if "close auction" button pressed, change is_active to false
    if request.method == "POST":

        auction = Auction.objects.get(id=request.POST["id"])
        auction.is_active = False
        auction.save()

        return HttpResponseRedirect(reverse("auctiondetails", args=(auction.id,)))
        
    return HttpResponseRedirect(reverse('index'))



def filter(request):

    form = FilterByCategories(request.POST)

    # filter control
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        auctions = Auction.objects.filter(category=data['categories']).order_by('-id')

        # render the filtered results
        return render(request, 'auctions/filter.html', {
            'auctions':auctions,
        })

    return HttpResponseRedirect(reverse('index'))