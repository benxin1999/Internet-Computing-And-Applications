from django.urls import path
from . import views

urlpatterns = [
    path('add/defaultData',views.create_deafault_category),
    path('add',views.add),
    path('list',views.fetch_all),
    path('delete',views.delete),
]