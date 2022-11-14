from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    name = models.CharField(db_index=True, max_length=256)
    slug = models.SlugField(db_index=True)
    csfd_id = models.IntegerField(db_index=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(BaseModel):
    pass

    @property
    def actors_count(self):
        return self.actors.count()


class Actor(BaseModel):
    movies = models.ManyToManyField(Movie, related_name="actors")

    @property
    def movies_count(self):
        return self.movies.count()
