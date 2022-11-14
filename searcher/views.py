from django.db.models import Q
from django.utils.text import slugify
from django.views.generic import DetailView, TemplateView

from searcher.models import Actor, Movie


class IndexPageView(TemplateView):
    template_name = "index.html"


class SearchView(TemplateView):
    template_name = "search.html"
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        search_query = self.request.GET.get("search")
        search_query_normalized = search_query.split(" ")

        filter_query = Q()
        for item in search_query_normalized:
            filter_query |= Q(name__contains=item)

        context = super().get_context_data(**kwargs)

        context["query"] = search_query
        context["movies"] = Movie.objects.filter(filter_query)
        context["actors"] = Actor.objects.filter(filter_query)

        return context


class MovieDetailView(DetailView):
    template_name = "movie_detail.html"
    model = Movie


class ActorDetailView(DetailView):
    template_name = "actor_detail.html"
    model = Actor
