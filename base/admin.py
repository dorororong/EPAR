from django.contrib import admin
from .models import UserInfo, SchoolInfo, SemesterInfo
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(SchoolInfo)
admin.site.register(SemesterInfo)
