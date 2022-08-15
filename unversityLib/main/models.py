from django.db import models
from django import utils
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime


class Author(models.Model):
    name = models.CharField("Автор", max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Keyword(models.Model):
    keyword_name = models.CharField("Ключевое слово", max_length=250)

    def __str__(self):
        return self.keyword_name

    class Meta:
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Books(models.Model):
    book_full_name = models.TextField('Полное Название книги (год издания/автор)')
    book_short_name = models.TextField('Название книги (Заголовок)')

    book_annotation = models.TextField('Аннотация из книги')

    authors = models.ManyToManyField(Author, verbose_name="Авторы")
    pages_number = models.IntegerField(verbose_name='Кол-во страниц')
    year = models.IntegerField(validators=[MinValueValidator(1984), max_value_current_year], verbose_name='Год издания')
    keywords = models.ManyToManyField(Keyword, verbose_name="Ключевые слова")
    file = models.FileField(upload_to='unversityLib/static/books/', verbose_name='Файл (эл.Пособие)')

    enter_date = models.DateField(default=utils.timezone.now, verbose_name='Дата загрузки книги')

    def __str__(self):
        return self.book_short_name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
