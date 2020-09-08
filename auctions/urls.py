from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("newauction/", views.new_auction, name="newauction"),
    path("auctiondetails/<int:auction_id>/", views.auction_details, name="auctiondetails"),
    path("favorites/", views.favorites, name="favorites"),
    path("favs/", views.fun_favorites, name="favs"),
    path("newcomment/", views.fun_new_comment, name="newcomment"),
    path("closeauction/", views.fun_close_auction, name="closeauction"),
    path("filter/", views.filter, name="filter"),
]
