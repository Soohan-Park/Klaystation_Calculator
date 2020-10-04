from django.contrib import admin

from .models import Donation, RateData

# Register your models here.
admin.site.register(Donation)
admin.site.register(RateData)