from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .manager import UserManager


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    username = models.CharField(
        'имя пользователя', max_length=150, unique=True)
    email = models.EmailField('адрес электронной почты', unique=True,
                              db_index=True)
    role = models.CharField('права пользователя',
                            max_length=9, choices=ROLE_CHOICES, default='user')
    bio = models.TextField('коротко о себе', max_length=500, blank=True)
    confirm = models.CharField('код подтверждения', max_length=200, blank=True)
    first_name = models.CharField('имя', max_length=150, blank=True)
    last_name = models.CharField('фамилия', max_length=150, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        ordering = ['pk']
        verbose_name = "пользователь"

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
        help_text="Здесь будет название произведения",
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="Это слаг, для категории",
        help_text="К нему потом можно будет обращаться",
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название жанра",
        help_text="Здесь будет название жанра",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Это слаг, для жанра",
        help_text="К нему потом можно будет обращаться",
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        verbose_name="Название произведения",
        help_text="Здесь будет название произведения",
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        help_text="Год выпуска произвдения",
    )
    description = models.TextField(
        verbose_name="Описание произвеения",
        help_text="Здесь будет описание произведения",
        max_length=1000,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="category",
        verbose_name="Категория произведения",
        help_text="Категория произведения",
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='genres',
        through="Genre_title",
        verbose_name="Жанр произведения",
        help_text="Жанр произведения",
    )

    def __str__(self):
        return self.name


class Genre_title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True)
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        'рейтинг',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                name='unique author-title review',
                fields=('author', 'title')
            ),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
