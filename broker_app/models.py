from django.db import models


# Create your models here.
class Survey(models.Model):
    building_name = models.CharField(max_length=255)
    building_address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.building_name
