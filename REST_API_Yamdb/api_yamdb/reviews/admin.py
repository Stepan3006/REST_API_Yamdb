from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import (User, Review, Comment, Title,
                     Categories, Genre_title)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'confirm',
        'first_name',
        'last_name',
    )

    search_fields = ('username',)
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Categories)
admin.site.register(Genre_title)
