from django.db import models
from django.contrib.auth.models import User


GENDERS = (('m', 'Male'), ('f', 'Female'))


class Profile(User):
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS)
    date_of_birth = models.DateField(null=True)
