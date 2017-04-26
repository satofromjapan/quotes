from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, data):
        errors= []
        # print info['email']
        users = User.objects.filter(email=data['email'])

        # print users
        if not users:
            errors.append("Invalid Email")
        else:
            userpass=User.objects.filter(email=data['email'])
            users1 = User.objects.filter(email=data['email'], password=bcrypt.hashpw(data['password'].encode(), userpass[0].password.encode()))
            # print users1
            if not users1:
                errors.append("Login Invalid")

        return errors

    def register(self, data):
        errors=[]
        email_check = User.objects.filter(email=data['email'])

        #Validate First Name
        if len(data['first_name']) < 2 or not data['first_name'].isalpha():
            errors.append('First name is not valid')
        #Validate Last Name
        if len(data['last_name']) < 2 or not data['last_name'].isalpha():
            errors.append('Last name is not valid')
        #Validate Email
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Email is not valid')
        #Checking for existing email
        if email_check:
            erros.append('Email already exists')
        #Validate password
        if len(data['password']) < 8:
            errors.append('Password must be more than 8 characters')
        #Validate password against confirm_password
        if data['password'] != data['confirm_password']:
            errors.append('Password must match confirm password')

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    birthday = models.DateField()
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User, related_name="quotes")
    favorite = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
