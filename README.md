# Django ČSFD TOP 1000 Searcher

This is a portfolio project showcasing building a simple **Django** app with a search capability, and a simple scraper using **Requests** library.

Frontend is styled with **Tailwind CSS** using CDN.

The code has been formated using **black**, imports sorted with **isort**.

## You exposed the secret key in your repo!

Yes. I included the whole settings file. This is a showcase project. It does not matter.

## Requirements

Included in the file requirements.txt. There is a lot of them since I used **Jupyter notebook** to develop the scraper.

I chose to leave it as it is to show what was used during the development. Production requirements would be a lot less cluttered.

What is truly needed: **Django**, **Requests** and **BeautifulSoup4**.

## How to set it up?

The repo has database already included. Nothing much is needed to run it.

## Running the scraper

The scraper is a management script **get_csfd_top_movies**, so just pwd into the Django root dir, activate virtual env and run it as you would any other management script:

> python manage.py get_csfd_top_movies

## Tests

Since we are not doing much "behind the scenes", there is only one test to make sure model instanes get slug generated upon creation. This is a custom logic in the model's save method (or the base model's, to be precise).

## Django Admin features

Login/pass: admin/admin

Models have a property showing how many actors a movie has and vice versa, which shows in Django Admin list display. I thought it was cool.
