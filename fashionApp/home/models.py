import uuid
from django.db import models

# 1. USER
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    display_name = models.CharField(max_length=255, null=False, blank=False)
    profile_picture_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    followers_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)

# 2. STORE
class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    logo_url = models.URLField(blank=True)

# 3A VARIANT 
class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    options = models.JSONField(blank=True, default=list)

# 3. PRODUCT
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3, null=False, blank=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    variants = models.ManyToManyField(Variant)

    # customising save function in order to handle blank fields
    def save(self, *args, **kwargs):
        if self.original_price is None: 
            self.original_price = self.price

        if self.discount_percentage is None:
            if self.original_price < self.price:
                self.discount_percentage = 0
            else:
                self.discount_percentage = (self.original_price - self.price) / self.original_price * 100
        
        super().save(*args, **kwargs)

# 5. MUSIC
class Music(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    artist = models.CharField(max_length=255, blank=True)
    cover_url = models.URLField(blank=True)

# 6. Our Final Product - VIDEO
class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_url = models.URLField(blank=False)
    thumbnail_url = models.URLField(blank=False)
    description = models.TextField(blank=True)
    view_count = models.IntegerField(default=0)
    duration = models.DurationField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='videos', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    is_liked = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, blank=True, null=True)
    hashtags = models.JSONField(blank=True, default=list)