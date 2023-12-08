from django.db import models
import re 

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # title validation
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters"
        return errors
       
    

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        # name validation
        if len(postData['name']) < 2:
            errors["name"] = "Name should be at least 2 characters"
        # alias validation
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be at least 2 characters"
        # email validation
        if len(postData['email']) < 8:
            errors["email"] = "Email should be at least 8 characters"
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors['email'] = ("Invalid email address!")
        # password validation
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        # confirm password validation
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        # email validation
        if len(postData['email']) < 8:
            errors["email"] = "Email should be at least 8 characters"
        # password validation
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        return errors


    # Create your models here.
# create user name alias email password with validations max_length 255 min_length 2 , email regex
class User (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


    # validations for name
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    author = models.CharField(max_length=50, default="unknown")
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ManyToManyField(User, related_name="books_reviewed")
    objects = BookManager()


class Review(models.Model):
    rate = models.IntegerField(default=0)
    review = models.CharField(max_length=50)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

