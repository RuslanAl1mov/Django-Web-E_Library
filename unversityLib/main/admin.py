from django.contrib import admin
from .models import Books
from .models import Author
from .models import Keyword


# Register your models here.

admin.site.register(Author)
admin.site.register(Keyword)

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('book_short_name', 'enter_date')
    exclude = ('enter_date',)

