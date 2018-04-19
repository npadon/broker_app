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


class Requirement(models.Model):
    name_of_tenant = models.CharField(max_length=255)
    type_of_tenant = models.CharField(max_length=255)

    building_size_choices = (('A', 'Class A'),
                             ('B', 'Class B'),
                             ('C', 'Class C'),
                             ('Any', 'Any'))
    building_class = models.CharField(
        max_length=3,
        choices=building_size_choices,
        default='Any',
    )
    minimum_rsf = models.FloatField()
    maximum_rsf = models.FloatField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name_of_tenant

    def get_absolute_url(self):
        return reverse('index')


class TourBook(models.Model):
    tour_title = models.CharField(max_length=255)
    tour_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.tour_title

    def get_absolute_url(self):
        return reverse('index')


class ExecutiveSummary(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('index')
