from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import Books
from main.models import Keyword
from main.models import Author

import os
import fitz
from PIL import Image


def keywords_for_menu_dropdown():
    keywords_from_db = Keyword.objects.all()

    cache_counter, amount_counter = 0, 0
    keywords_block, cache_list = [], []
    for keyword in keywords_from_db:
        cache_list.append(keyword)
        cache_counter += 1
        amount_counter += 1
        if cache_counter == 17:
            keywords_block.append(cache_list.copy())
            cache_list.clear()
            cache_counter = 0
        elif amount_counter == len(keywords_from_db):
            keywords_block.append(cache_list.copy())

    return keywords_block


def authors_for_menu_dropdown():
    authors_from_db = Author.objects.all()

    cache_counter, amount_counter = 0, 0
    authors_block, cache_list = [], []
    for author in authors_from_db:
        cache_list.append(author)
        cache_counter += 1
        amount_counter += 1
        if cache_counter == 17:
            authors_block.append(cache_list.copy())
            cache_list.clear()
            cache_counter = 0
        elif amount_counter == len(authors_from_db):
            authors_block.append(cache_list.copy())

    return authors_block


def books_pack(book):
    IMAGES_PATH = f'unversityLib\\static\\img\\books_covers_imgs\\'
    CSS_BOOK_COVER_PATH = "img/books_covers_imgs/"

    book_name = book.file.name.split('/')[-1]
    book_format = book_name.split('.')[-1]
    file_size = os.path.getsize(book.file.name) / (1024 * 1024)
    file_size = float(f'{file_size:.2f}')

    try:
        image_name = book_name.replace('.pdf', '') + '.png'
        if image_name not in os.listdir(IMAGES_PATH):
            doc = fitz.open(book.file.name)
            pix = doc.get_page_pixmap(0)
            pix.save(IMAGES_PATH + image_name)

            image = Image.open(IMAGES_PATH + image_name)
            resized_image = image.resize((245, 330))
            resized_image.save(IMAGES_PATH + image_name)

    except Exception as e:
        print("Ошибка загрузки обложки книги!  -->  " + repr(e))
        image_name = 'UnknownBookCover.png'

    image_name = CSS_BOOK_COVER_PATH + image_name

    return {'book_object': book, 'book_cover_path': image_name,
            'book_name': book_name, 'file_format': book_format, 'file_size': file_size}


def simple_search(search_info, order_by_settings):
    db_books_list = Books.objects.all()
    if len(db_books_list) != 0:
        if order_by_settings is not None:
            db_books_list.order_by(order_by_settings)
        else:
            db_books_list.order_by("book_short_name")

        searched_books_list = []

        for book in db_books_list:
            book_name = str(book.book_full_name).replace(".", "").replace(",", "").replace(":", "").replace("?", "").replace("!", "")

            for author in book.authors.all():
                book_name = book_name + " " + author.name

            for keyword in book.keywords.all():
                book_name = book_name + " " + keyword.keyword_name

            if search_info.lower() in book_name.lower():
                searched_books_list.append(books_pack(book))

        return searched_books_list, len(searched_books_list), len(db_books_list)


@csrf_exempt
def index(request):

    searched = ''
    order_by_settings = None

    try:
        order_by_settings = request.POST.get('sort_by')
        print(order_by_settings)
    except Exception as e:
        print(repr(e))

    if order_by_settings is None:
        order_by_settings = 'book_short_name'

    try:
        searched = request.POST['searched'].replace(',', '')
        print(searched)
    except Exception as e:
        print(repr(e))

    db_books_list = Books.objects.all()
    if len(db_books_list) != 0:  # Если БД книг не пустая

        if searched != '':
            searched_books_list, search_books_amount, all_books_amount = simple_search(searched, order_by_settings)

            return render(request, 'search_page/search.html', {'books_list': searched_books_list,
                                                               'keywords_block': keywords_for_menu_dropdown(),
                                                               'authors_block': authors_for_menu_dropdown(),
                                                               'books_amount': all_books_amount,
                                                               'search_value': searched,
                                                               'search_title': "Найдено по запросу Книг: " + str(search_books_amount) + " шт.",
                                                               'sorted_by': order_by_settings})

        elif searched == '':
            if order_by_settings is not None:
                db_books_list = Books.objects.all().order_by(order_by_settings)
            else:
                db_books_list = Books.objects.all().order_by("book_short_name")

            all_books_amount = len(db_books_list)

            searched_books_list = []
            for book in db_books_list:
                searched_books_list.append(books_pack(book))

            return render(request, 'search_page/search.html', {'books_list': searched_books_list,
                                                               'keywords_block': keywords_for_menu_dropdown(),
                                                               'authors_block': authors_for_menu_dropdown(),
                                                               'books_amount': all_books_amount,
                                                               'search_value': searched,
                                                               'search_title': "Каталог книг",
                                                               'sorted_by': order_by_settings})
    else:
        return render(request, 'search_page/search.html', {'books_list': [],
                                                           'keywords_block': keywords_for_menu_dropdown(),
                                                           'authors_block': authors_for_menu_dropdown(),
                                                           'books_amount': 0,
                                                           'search_value': searched,
                                                           'search_title': "База книг пуста!",
                                                           'sorted_by': order_by_settings})