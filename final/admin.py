from django.contrib import admin

# Register your models here.
from .models import User, Topics, Cards, UserChoice
# Register your models here.

admin.site.register(User)
admin.site.register(Topics)
admin.site.register(Cards)
admin.site.register(UserChoice)

