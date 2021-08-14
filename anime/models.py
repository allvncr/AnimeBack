from django.db.models import *
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Genre(Model):
    name = CharField(max_length=50, unique=True)
    slug = SlugField(unique=True)
    image = URLField()
    description = TextField(blank=True)

    @property
    def genre_count(self):
        return self.animes.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Studio(Model):
    name = CharField(max_length=30, unique=True)
    slug = SlugField(unique=True)

    @property
    def studio_count(self):
        return self.animes.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Studio, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Anime(Model):
    EN_COURS = 'EC'
    TERMINÉ = 'TN'
    PROCHAINEMENT = 'PR'
    CHOICE = [
        (EN_COURS, 'EN COURS'),
        (TERMINÉ, 'TERMINÉ'),
        (PROCHAINEMENT, 'PROCHAINEMENT'),
    ]
    studio = ForeignKey(Studio, on_delete=CASCADE, related_name='animes')
    genres = ManyToManyField(Genre, through='Category', related_name='animes', blank=True)
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True)
    image = URLField()
    date = DateField()
    created = DateField(auto_now_add=True)
    updated = DateField(auto_now=True)
    note = DecimalField(default=0.0, max_digits=2, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    synopsis = TextField(blank=True)
    status = CharField(max_length=20, choices=CHOICE, default=TERMINÉ)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Anime, self).save(*args, **kwargs)

    @property
    def episode_count(self):
        return self.episodes.count()

    @property
    def views(self):
        episodes = self.episodes.all()
        view = 0
        for episode in episodes:
            view = view + episode.views
        return view

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)


class Category(Model):
    anime = ForeignKey(Anime, on_delete=CASCADE, related_name='a_genres')
    genre = ForeignKey(Genre, on_delete=CASCADE, related_name='g_animes')

    class Meta:
        unique_together = (('anime', 'genre',),)


class Episode(Model):
    anime = ForeignKey(Anime, on_delete=CASCADE, related_name='episodes')
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True)
    created = DateField(auto_now_add=True)
    updated = DateField(auto_now=True)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    dislike = PositiveIntegerField(default=0)
    video = URLField()
    download = URLField(blank=True)
    valid = BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
