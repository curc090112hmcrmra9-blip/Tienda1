from django.urls import path
# agregar ulrs de app1
from . import views

urlpatterns = [
    #path('saludar/<str:nombre>/<int:edad>',views.saludar),
     path('infor',views.info, name='info'),
     path('',views.home, name='home'),
     path('stores/',views.stores_view, name='stores'),
     path('products/',views.products_view, name='products'),
     path('create_store/',views.create_store, name='create_store'),
     path('create_product/',views.create_product, name='create_product'),
     path('details/<int:id>',views.details,name='details'),
     path('contact',views.contact,name='contact'),
     path('filtro/',views.ProductosListView.as_view(), name='filtro' ),
     path('filtro-stores/', views.StoresListView.as_view(), name='filtro_stores'),
     
     # Nuevas URLs para productos
     path('update_product/', views.update_product, name='update_product'),
     path('delete_product/', views.delete_product, name='delete_product'),

     # Nuevas URLs para Stores
     path('update_stores/', views.update_Stores, name='update_stores'),
     path('delete_stores/', views.delete_Stores, name='delete_stores'),
     path('filtro/', views.ProductosListView.as_view(), name='filtro'),
     path('filtro-stores/', views.StoresListView.as_view(), name='filtro_stores'),


     
]