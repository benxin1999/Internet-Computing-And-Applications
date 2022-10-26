from django.urls import path
from . import views

urlpatterns =[
    path('add',views.add),
    path('delete',views.delete),
    path('detail',views.fetch_one),
    path('list',views.get_bill_lists),
    path('update',views.update),
]
