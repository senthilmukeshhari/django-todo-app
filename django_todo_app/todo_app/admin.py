from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = [ 'username', 'email', 'is_staff', 'profile_img' ]

class TodoListAdmin(admin.ModelAdmin):
    list_display = [ 'username', 'title', 'description', 'is_completed' ]

admin.site.register(User, UserAdmin)
admin.site.register(TodoList, TodoListAdmin)