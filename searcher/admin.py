from django.contrib import admin

from searcher.models import Actor, Movie

# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ["name", "actors_count"]


admin.site.register(Movie, MovieAdmin)


class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "movies_count"]


admin.site.register(Actor, ActorAdmin)
