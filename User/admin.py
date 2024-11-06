from django.contrib import admin

from User.models import AdminUser, User

# Register your models here.


admin.site.register(AdminUser)
admin.site.register(User)