from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_of_creation', 'img', 'views_count',)
    list_filter = ('views_count',)
    search_fields = ('title', 'content',)