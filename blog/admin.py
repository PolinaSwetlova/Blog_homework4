from django.contrib import admin

from .models import Category, Location, Post, Tag

admin.site.empty_value_display = 'Не задано'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
        'slug'
    )
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    search_fields = ('name',)
    list_editable = ('is_published',)
    list_filter = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'author',
        'pub_date',
        'location',
        'category'
    )
    search_fields = ('title',)
    list_editable = ('is_published',)
    list_filter = (
        'title',
        'author',
        'pub_date',
        'location',
        'category'
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
