from django.contrib import admin
from .models import User,Moving,Staying,PassPort,Holiday,LimitsOfDate,Pappers

# Register your models here.
admin.site.register(User)
admin.site.register(Moving)
admin.site.register(Staying)
admin.site.register(PassPort)
admin.site.register(Holiday)
admin.site.register(LimitsOfDate)
admin.site.register(Pappers)