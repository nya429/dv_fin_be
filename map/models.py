# from fcntl import LOCK_EX
from django.db import models

# Create your models here.
class Tracker(models.Model):
    tracker_id = models.CharField(max_length=127, null=False, unique=False)

    def __str__(self):
        return f"{self.tracker_id}"


class Location(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    tracker_id = models.CharField(max_length=32, blank=True, null=True)
    loc_x = models.IntegerField(blank=True, null=True) 
    loc_y = models.IntegerField(blank=True, null=True) 
    product_id = models.CharField(max_length=32, blank=True, null=True)
    
    def __str__(self):
        return f"{self.tracker_id} {self.time}"


class Setting(models.Model):
    setting_key = models.CharField(max_length=127, null=False, unique=True)
    setting_value = models.CharField(max_length=127, null=False, unique=False)
    
    def __str__(self):
        return f"{self.setting_key}"