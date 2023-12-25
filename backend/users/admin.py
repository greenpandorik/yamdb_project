from django.contrib import admin

from .models import User, Subscription


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'username')
    search_fields = ('username', 'email')


admin.site.register(User, UsersAdmin)
admin.site.register(Subscription)
