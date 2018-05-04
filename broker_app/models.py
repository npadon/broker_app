from django.contrib.auth.models import User
from django.core.validators import int_list_validator, MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse


class MediaUpload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()


class Requirement(models.Model):
    furniture_choices = (('Y', 'Y'), ('N', 'N'))
    lease_or_purchase_choices = (('Lease', 'Lease'), ('Purchase', 'Purchase'))

    name_of_tenant = models.CharField(max_length=255)
    type_of_tenant = models.CharField(max_length=255)
    commencement_date = models.DateField()
    term_length_YRS = models.FloatField(default=0)

    submarket_A = models.NullBooleanField()
    submarket_B = models.NullBooleanField()
    submarket_C = models.NullBooleanField()
    submarket_D = models.NullBooleanField()

    building_class_A = models.NullBooleanField()
    building_class_B = models.NullBooleanField()
    building_class_C = models.NullBooleanField()

    minimum_rsf = models.FloatField(default=0)
    maximum_rsf = models.FloatField(null=True, blank=True)
    lease_or_purchase = models.CharField(max_length=10, choices=lease_or_purchase_choices, default='Lease')
    desired_percentage_offices_PCT = models.FloatField(validators=[MaxValueValidator(1.1), MinValueValidator(-.1)],
                                                       default=0)
    needs_furniture = models.CharField(max_length=2, choices=furniture_choices, default='N')
    notes = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name_of_tenant

    def get_absolute_url(self):
        return reverse('index')


class Survey(models.Model):
    gross_net_bases = (('Gross', 'Gross'), ('Net', 'Net'))

    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)

    building_name = models.CharField(max_length=255, null=False, default='default_building')
    building_address = models.CharField(max_length=255, null=False, default='default_address')
    zipcode = models.CharField(max_length=10, null=False, default='77019')
    building_size_RSF = models.IntegerField(null=False, default=0)
    building_number_of_floors = models.IntegerField(null=False, default=0)
    building_avg_floor_size = models.IntegerField(null=False, default=0)
    subject_space_floors = models.CharField(max_length=50, null=False, validators=[int_list_validator()], default='0')
    subject_space_size_RSF = models.IntegerField(null=False, default=0)
    quoted_net_rental_rate_USD_per_RSF = models.FloatField(null=False, default=0)
    estimated_yearly_operating_expenses_USD = models.FloatField(null=False, default=0)
    annual_increase_in_net_rental_rate_USD = models.IntegerField(null=False, default=0)
    quoted_improvement_allowance_USD = models.IntegerField(null=False, default=0)
    quoted_free_rent_months_CNT = models.IntegerField(null=False, default=0)
    quoted_free_rent_basis = models.CharField(max_length=10, choices=gross_net_bases, default='Gross', null=False)
    building_reserved_parking_ratio = models.FloatField(null=False,
                                                        validators=[MaxValueValidator(2), MinValueValidator(-1)],
                                                        default=0)
    building_reserved_parking_rates_USD_per_DAY = models.FloatField(null=False, default=0)
    building_unreserved_parking_ratio = models.FloatField(null=False,
                                                          validators=[MaxValueValidator(2), MinValueValidator(-1)],
                                                          default=0)
    building_unreserved_parking_rates_USD_per_DAY = models.FloatField(null=False, default=0)
    supplemental_garage_reserved_parking_ratio = models.FloatField(null=True, blank=True,
                                                                   validators=[MaxValueValidator(2),
                                                                               MinValueValidator(-1)],
                                                                   default=0)
    supplemental_garage_reserved_parking_rates_USD_per_DAY = models.FloatField(null=True, blank=True, default=0)
    supplemental_garage_unreserved_parking_ratio = models.FloatField(null=True, blank=True,
                                                                     validators=[MaxValueValidator(2),
                                                                                 MinValueValidator(-1)],
                                                                     default=0)
    supplemental_garage_unreserved_parking_rates_USD_per_DAY = models.FloatField(null=True, blank=True, default=0)
    subject_space_former_use = models.TextField(null=True, blank=True)
    subject_space_existing_condition = models.TextField(null=True, blank=True)
    building_capital_improvements = models.TextField(null=True, blank=True)
    other_notes = models.TextField(null=True, blank=True)

    # "Upload building floor plan*"
    # "Upload building photo*"
    # "Upload other documents"
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.building_name

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
