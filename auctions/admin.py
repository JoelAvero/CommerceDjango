from django.contrib import admin

from auctions.models import Auction, Bid, Comment, User
# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    search_fields = ("id", "title", "name")
    list_filter = ("name", "title")


class CommentAdmin(admin.ModelAdmin):
    search_fields = ("name", "comment", "fk_auctions__id", "fk_auctions__title")
    list_filter = ("name", "fk_auctions__title")


class BidAdmin(admin.ModelAdmin):
    search_fields = ("name", "fk_auctions__id", "fk_auctions__title", "bid")
    list_filter = ("name", "fk_auctions__title")


admin.site.register(User)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)