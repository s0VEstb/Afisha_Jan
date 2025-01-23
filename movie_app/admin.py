from django.contrib import admin
from .models import Director, Movie, Review


admin.site.register(Director)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'duration')
    search_fields = ('title', 'director__name')
    list_filter = ('director',)


admin.site.register(Review)
