from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('search/', include('search_book.urls'), name='search-book'),
    path('book-info/<int:book_id>/', views.show_book, name='book-info')
]
