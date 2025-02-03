from django.db import models

class Gender(models.TextChoices):
    FEMALE = 'female', 'Female'
    MALE = 'male', 'Male'
    UNDEFINED = 'undefined', 'Undefined'
    