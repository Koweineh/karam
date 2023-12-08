from django.urls import path 
from . import views


urlpatterns = [
    path('',views.register),
    path('register-form',views.register_form),
    path('login-form',views.login_form),
    path('books',views.books),
    path('logout',views.logout),
    path('add-book',views.add_book),
    path('add-book-form',views.add_book_form),
    path('books/<int:book_id>',views.book_info),
    

]
