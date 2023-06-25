from django.contrib import admin
from .models import ReferenceScore, ReferenceSubsubject, Reference_Grade_Subject
# Register your models here.

admin.site.register(Reference_Grade_Subject)
admin.site.register(ReferenceSubsubject)
admin.site.register(ReferenceScore)

