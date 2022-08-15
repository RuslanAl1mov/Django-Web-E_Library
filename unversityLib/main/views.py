from django.shortcuts import render
from .models import Books
from .models import Keyword
from .models import Author

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


def index(request):
    books_list = Books.objects.all()[::-1]
    IMAGES_PATH = f'unversityLib\\static\\img\\books_covers_imgs\\'

    books_info_list = []

    if len(books_list) != 0:
        book_number = 0
        for book in books_list:
            book_number += 1
            if book_number <= 9:
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
                    print(e)
                    image_name = 'UnknownBookCover.png'

                books_info_list.append({'book_object': book, 'book_cover_name': image_name, 'file_format': book_format,
                                        'file_size': file_size})

    return render(request, 'main/index.html', {'books_list': books_info_list,
                                               'keywords_block': keywords_for_menu_dropdown(),
                                               'authors_block': authors_for_menu_dropdown(),
                                               'books_amount': len(books_list)})


def show_book(request, book_id):
    CSS_BOOK_COVER_PATH = "img/books_covers_imgs/"

    book = Books.objects.get(pk=book_id)
    book_file_name = book.file.name.split('/')[-1]
    print(book_file_name)
    book_format = book_file_name.split('.')[-1]
    file_size = os.path.getsize(book.file.name) / (1024 * 1024)
    file_size = float(f'{file_size:.2f}')

    image_name = book_file_name.replace('.pdf', '') + '.png'
    book_cover = CSS_BOOK_COVER_PATH + image_name

    return render(request, 'book_info_page/book_info.html', {'book_obj': book,
                                                             'book_file_name': book_file_name,
                                                             'keywords_block': keywords_for_menu_dropdown(),
                                                             'authors_block': authors_for_menu_dropdown(),
                                                             'book_format': book_format,
                                                             'file_size': file_size,
                                                             'book_cover_path': book_cover})
