# Generated by Django 4.0.5 on 2022-08-10 06:25

import django.core.validators
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_name', models.CharField(max_length=250, verbose_name='Ключевое слово')),
            ],
            options={
                'verbose_name': 'Ключевое слово',
                'verbose_name_plural': 'Ключевые слова',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_full_name', models.TextField(verbose_name='Полное Название книги (год издания/автор)')),
                ('book_short_name', models.TextField(verbose_name='Название книги (Заголовок)')),
                ('book_annotation', models.TextField(verbose_name='Аннотация из книги')),
                ('pages_number', models.IntegerField(verbose_name='Кол-во страниц')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1984), main.models.max_value_current_year], verbose_name='Год издания')),
                ('file', models.FileField(upload_to='unversityLib/static/books/', verbose_name='Файл (эл.Пособие)')),
                ('authors', models.ManyToManyField(to='main.author', verbose_name='Авторы')),
                ('keywords', models.ManyToManyField(to='main.keyword', verbose_name='Ключевые слова')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
    ]
