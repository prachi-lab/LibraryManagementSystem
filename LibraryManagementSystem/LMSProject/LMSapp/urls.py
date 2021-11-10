from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
     path('list_books/', views.list_books, name='list_books'),
     path('add_books/', views.add_books, name='add_books'),
     path('update_books/<str:pk>/', views.update_books, name="update_books"),
     path('delete_books/<str:pk>/', views.delete_books, name="delete_books"),
     path('book_detail/<str:pk>/', views.book_detail, name="book_detail"),
     path('issue_books/<str:pk>/', views.issue_books, name="issue_books"),
     path('receive_books/<str:pk>/', views.receive_books, name="receive_books"),
     path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
     path('book_history/', views.book_history, name='book_history')]