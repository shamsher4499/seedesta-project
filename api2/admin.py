from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'mobile', 'is_verified', 'is_active',)
admin.site.register(User, UserAdmin)

# class ProfileAdmin(admin.ModelAdmin):
#     list_display  = ('username', 'user')
# admin.site.register(UserProfile, ProfileAdmin)

class GoalAdmin(admin.ModelAdmin):
    list_display  = ('user', 'category', 'goal_name', 'start_date', 'amount')
admin.site.register(Goal, GoalAdmin)
