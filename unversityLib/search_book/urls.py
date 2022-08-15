from django.urls import path
from . import views

def ret_req(request):
    print(request)
    return request.POST['searched']

urlpatterns = [
    path('', views.index, name='search-book'),
]
