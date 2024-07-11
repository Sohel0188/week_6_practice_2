from django.db import models

# Create your models here.

class BankInfo(models.Model):
    name = models.CharField(max_length=20)
    is_bankrupt = models.BooleanField(default=False)
