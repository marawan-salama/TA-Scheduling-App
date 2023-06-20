from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from project_app.models import User, Course, Section, Notification


admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Notification)
