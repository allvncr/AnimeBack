from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db.models.signals import post_save
from anime.models import Episode


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email Address")
        if not username:
            raise ValueError("Users must have an Username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, null=True)
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Channel(models.Model):
    Homme = 'H'
    Femme = 'F'
    Autre = 'A'
    SEXE = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
        ('Autre', 'Autre'),
    ]

    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="channel")
    description = models.TextField(blank=True)
    location = models.CharField(max_length=20, blank=True)
    views = models.PositiveIntegerField(default=0)
    photo = models.URLField(blank=True, default="https://dynamic-assets.mobilius.top/images/default-avatars/23.png")
    sexe = models.CharField(max_length=8, choices=SEXE, default=Homme, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return 'Channel User {}'.format(self.user.username)

    def create_channel(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_channel = Channel(user=user)
            user_channel.save()

    post_save.connect(create_channel, sender=Account)


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="playlists")
    episodes = models.ManyToManyField(Episode, through='PlaylistTrack', related_name='playlists', blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks')
    track = models.ForeignKey(Episode, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        ordering = ('position',)
        unique_together = (('playlist', 'track'),)
