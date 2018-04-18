from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse


# Create your models here.
class Survey(models.Model):
    building_name = models.CharField(max_length=255)
    building_address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.building_name

    def get_absolute_url(self):
        return reverse('index')
