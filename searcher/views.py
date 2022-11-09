from django.views.generic import DetailView, TemplateView

from searcher.models import Actor, Movie


class IndexPageView(TemplateView):
    template_name = "index.html"


class SearchView(TemplateView):
    template_name = "search.html"
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        search_query = self.request.GET.get("search")

        context = super().get_context_data(**kwargs)
        context["query"] = search_query
        context["movies"] = Movie.objects.filter(name__icontains=search_query)
        context["actors"] = Actor.objects.filter(name__icontains=search_query)

        return context


class MovieDetailView(DetailView):
    template_name = "movie_detail.html"
    model = Movie


class ActorDetailView(DetailView):
    template_name = "actor_detail.html"
    model = Actor
