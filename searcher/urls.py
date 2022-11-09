from django.urls import path

from .views import ActorDetailView, IndexPageView, MovieDetailView, SearchView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("search/", SearchView.as_view(), name="search"),
    path("movie/<slug:slug>", MovieDetailView.as_view(), name="movie-detail"),
    path("actor/<slug:slug>", ActorDetailView.as_view(), name="actor-detail"),
]
