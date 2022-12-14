# Generated by Django 2.2.16 on 2022-06-08 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True, verbose_name='имя пользователя')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='адрес электронной почты')),
                ('role', models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=9, verbose_name='права пользователя')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='коротко о себе')),
                ('confirm', models.CharField(blank=True, max_length=200, verbose_name='код подтверждения')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='имя')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='фамилия')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователь',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Здесь будет название произведения', max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(help_text='К нему потом можно будет обращаться', unique=True, verbose_name='Это слаг, для категории')),
            ],
        ),
        migrations.CreateModel(
            name='Genre_title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Здесь будет название жанра', max_length=200, verbose_name='Название жанра')),
                ('slug', models.SlugField(help_text='К нему потом можно будет обращаться', unique=True, verbose_name='Это слаг, для жанра')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Здесь будет название произведения', verbose_name='Название произведения')),
                ('year', models.IntegerField(help_text='Год выпуска произвдения', verbose_name='Год выпуска')),
                ('description', models.TextField(help_text='Здесь будет описание произведения', max_length=1000, verbose_name='Описание произвеения')),
                ('category', models.ForeignKey(blank=True, help_text='Категория произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='reviews.Categories', verbose_name='Категория произведения')),
                ('genre', models.ManyToManyField(help_text='Жанр произведения', related_name='genres', through='reviews.Genre_title', to='reviews.Genres', verbose_name='Жанр произведения')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('score', models.IntegerField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title')),
            ],
        ),
        migrations.AddField(
            model_name='genre_title',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Genres'),
        ),
        migrations.AddField(
            model_name='genre_title',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Title'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review')),
            ],
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique author-title review'),
        ),
    ]
