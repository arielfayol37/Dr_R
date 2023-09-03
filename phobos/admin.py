from django.contrib import admin

# Register your models here.
from .models import Course, Professor
admin.site.register(Course)
admin.site.register(Professor)