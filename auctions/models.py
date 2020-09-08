from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Auction(models.Model):
    CLOTHES = "CL"
    ELECTRONICS = "EL"
    SPORTS = "SP"
    TOYS = "TO"
    CATEGORIES = [
        (CLOTHES, 'Clothes'),
        (ELECTRONICS, 'Electronics'),
        (SPORTS, 'Sports'),
        (TOYS, 'Toys'),
    ]
    
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50, default="Null")
    desc = models.TextField()
    image = models.CharField(max_length=200, default="No image", blank=True)
    price = models.IntegerField()
    category = models.CharField(max_length=2, choices=CATEGORIES)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return f"ID: {self.id} - - - -Item: {self.title} - - - -Posted by: {self.name}"



class Bid(models.Model):
    bid = models.IntegerField()
    name = models.CharField(max_length=50, default="No bids yet.")
    fk_auctions = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bidshere", null=True)

    def __str__(self):
        return f"Auction ID: {self.fk_auctions.id} --- Bid: {self.bid} --- Auction title: {self.fk_auctions.title} --- Bidder: {self.name}"

    class Meta:
        get_latest_by = 'id'



class Comment(models.Model):
    comment = models.TextField()
    name = models.CharField(max_length=50)
    fk_auctions = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="commentshere", null=True)

    def __str__(self):
        return f"Auction ID: {self.fk_auctions.id} --- Auction title: {self.fk_auctions.title} --- Commented by: {self.name}"



class Favorite(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userhere", null=True)
    fk_auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auctionhere", null=True)

