from django.contrib import admin
from accounts.models import UserDepartment, UserProfile, Department

admin.site.register(UserDepartment)
admin.site.register(Department)
admin.site.register(UserProfile)

