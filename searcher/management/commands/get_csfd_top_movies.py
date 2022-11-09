import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from searcher.models import Actor, Movie

# We need to set user agent so CSFD site lets us scrape (else we get 429)
HEADERS = {
    "User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
}

# Number of top entries changed once, this provides a quick way to set it to a different number, ditto for range step
MAX_RANGE_LIMIT = 1000
RANGE_STEP = 100


class Command(BaseCommand):
    help = "Scrapes info about top 1000 movies from CSFD and populates the database."

    def handle(self, *args, **kwargs):
        start_url = "https://www.csfd.cz/zebricky/filmy/nejlepsi/?showMore=1"
        movie_detail_url_base = "https://www.csfd.cz"
        next_url_base = "https://www.csfd.cz/zebricky/filmy/nejlepsi/?from={}"
        next_url_params = [step for step in range(100, MAX_RANGE_LIMIT, RANGE_STEP)]
        next_urls = [next_url_base.format(param) for param in next_url_params]

        urls = [start_url, *next_urls]

        for url in urls:
            # Print this just to get a sense of progress
            print(f"Scraping {url}")
            resp = requests.get(url, headers=HEADERS)

            # Don't bother with anything if we don't get the all clear signal.
            if resp.status_code != 200:
                raise Exception("Response is not valid for scraping!")

            soup = BeautifulSoup(resp.content, "html.parser")

            # We want links without any class. Also some keyword blacklisting.
            movies = soup.find_all(
                "a",
                {"class": None},
                href=lambda href: href
                and "film" in href
                and "zebricky" not in href
                and "pridat" not in href,
            )

            for movie in movies:
                # To see progress again
                print(f"Scraping info about movie {movie['title']}")

                # I wanted to use plain .create() as I assume TOP 1000 list should have 1000 unique items.
                # But, in the words of Quellcrist Falconer: 'Assume nothing. Only then can you truly see what you’re dealing with.'
                movie_obj, created = Movie.objects.get_or_create(name=movie["title"])

                if not created:
                    print(
                        f"Movie {movie['title']} already exists in the database. Skipping."
                    )
                    continue

                movie_resp = requests.get(
                    f'{movie_detail_url_base}{movie["href"]}', headers=HEADERS
                )
                movie_soup = BeautifulSoup(movie_resp.text, "html.parser")

                # Find the Hrají string and get the parent div, so we can get the array of actors.
                try:
                    actors_tag = movie_soup.find("h4", text="Hrají: ")
                    actors_parent_div = actors_tag.find_parent()
                    actors = actors_parent_div.find_all("a", {"class": None})

                    for actor in actors:
                        # get_or_create(), because actor might already exist from previous movies
                        actor_obj, created = Actor.objects.get_or_create(
                            name=actor.contents[0]
                        )

                        if not created:
                            print(
                                f"Actor {actor.contents[0]} already exists in the database! "
                                f"Adding movie {movie['title']} to his filmography."
                            )

                        movie_obj.actors.add(actor_obj)
                except AttributeError:
                    # Movie detail has no actors listed
                    print(
                        f"Movie {movie['title']} does not seem to have actors listed on the detail page!"
                    )
                    continue
