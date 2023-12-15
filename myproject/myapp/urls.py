from django.urls import path
from . import views
from myapp.views_old import signup, login_view, custom_logout


urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', custom_logout, name='logout'),
    path('items/', views.item_list, name='item_list'),
    path('add/', views.item_add, name='item_add'),
    path('edit/<int:pk>/', views.item_edit, name='item_edit'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    path('summary/', views.item_summary, name='item_summary'),
]
