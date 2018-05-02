from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.core.validators import int_list_validator, MaxValueValidator, MinValueValidator


# Create your models here.
class Survey(models.Model):
    gross_net_bases = (('Gross', 'Gross'), ('Net', 'Net'))

    building_name = models.CharField(max_length=255, null=False)
    building_address = models.CharField(max_length=255, null=False)
    zipcode = models.CharField(max_length=10, null=False)
    building_size = models.IntegerField(null=False)
    building_number_of_floors = models.IntegerField(null=False)
    building_avg_floor_size = models.IntegerField(null=False)
    subject_space_floors = models.CharField(max_length=50, null=False, validators=[int_list_validator()])
    subject_space_size_RSF = models.IntegerField(null=False)
    quoted_net_rental_rate_USD_per_RSF = models.FloatField(null=False)
    estimated_yearly_operating_expenses_USD = models.FloatField(null=False)
    annual_increase_in_net_rental_rate_USD = models.IntegerField(null=False)
    quoted_improvement_allowance_USD = models.IntegerField(null=False)
    quoted_free_rent_months_CNT = models.IntegerField(null=False)
    quoted_free_rent_basis = models.CharField(max_length=10, choices=gross_net_bases, default='Gross', null=False)
    building_reserved_parking_ratio = models.FloatField(null=False,
                                                        validators=[MaxValueValidator(1), MinValueValidator(0)])
    building_reserved_parking_rates_USD_per_DAY = models.FloatField(null=False)
    building_unreserved_parking_ratio = models.FloatField(null=False,
                                                          validators=[MaxValueValidator(1), MinValueValidator(0)])
    building_unreserved_parking_rates_USD_per_DAY = models.FloatField(null=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    supplemental_garage_reserved_parking_ratio = models.FloatField(null=True, blank=True,
                                                                   validators=[MaxValueValidator(1),
                                                                               MinValueValidator(0)])
    supplemental_garage_reserved_parking_rates_USD_per_DAY = models.FloatField(null=True, blank=True)
    supplemental_garage_unreserved_parking_ratio = models.FloatField(null=True, blank=True,
                                                                     validators=[MaxValueValidator(1),
                                                                                 MinValueValidator(0)])
    supplemental_garage_unreserved_parking_rates_USD_per_DAY = models.FloatField(null=True, blank=True)
    subject_space_former_use = models.TextField(null=True, blank=True)
    subject_space_existing_condition = models.TextField(null=True, blank=True)
    building_capital_improvements = models.TextField(null=True, blank=True)
    other_notes = models.TextField(null=True, blank=True)

    # "Upload building floor plan*"
    # "Upload building photo*"
    # "Upload other documents"
    
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
    surveys = models.ManyToManyField(Survey)

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
