from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Authentication)
admin.site.register(Novidpart)
admin.site.register(Vidpart)
admin.site.register(Notifications)
admin.site.register(Interestnovidpart)
admin.site.register(Interestvidpart)