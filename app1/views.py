from django.shortcuts import render,redirect
from .models import User, Book  , Review
import bcrypt
from django.contrib import messages
# Create your views here.

def register(request):
    return render(request, 'register-login.html')



def register_form(request):
    erros = User.objects.basic_validator(request.POST)
    if len(erros) > 0:
        for key, value in erros.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == 'POST':
            # create new user 
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create 
            new_user = User.objects.create(
                name = request.POST['name'],
                alias = request.POST['alias'],
                email = request.POST['email'],
                password = pw_hash,
            )
            # set the new user to session
            request.session['user_id'] = new_user.id
            # redirect to books page
            return redirect('/books')
def login_form(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
    # see if the username provided exists in the database
        user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
        print(user)
        if user: # note that we take advantage of truthiness here: an empty list will return false
            user = user[0] 
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/books')
            else:
                print("failed password")
        # if we didn't find anything in the database by searching by username or if the passwords don't match, 
        # redirect back to a safe route
        return redirect("/")


def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'reviews': Review.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    
    return render(request, 'books.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


def add_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'add-book.html')


def add_book_form(request):
    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/books/add')
    else:
        if request.method == 'POST':
            # create new book 
            author = request.POST['author']
            if request.POST['author'] == "":
                author = request.POST['author-select']
            new_book = Book.objects.create(
                title = request.POST['title'],
                author = author,
                uploaded_by = User.objects.get(id=request.session['user_id'])
            )
            # make rating and review
            
    
            Review.objects.create(
                review = request.POST['review'],
                rate = request.POST['rating'],
                book = new_book,
                user = User.objects.get(id=request.session['user_id'])

            )
            
            return redirect('/books')
def book_info(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    Reviews = Review.objects.filter(book=book_id)
    context = {
        'book': Book.objects.get(id=book_id),
        'user': User.objects.get(id=request.session['user_id']),
        'reviews': Reviews,
    }
    return render(request, 'book-info.html', context)