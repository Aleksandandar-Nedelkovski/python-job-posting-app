from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re 

class UserManager(models.Manager):
    def register(self, name, lname, email, password, confirm):
        errors = []
        if len(name) < 2:
            errors.append("Name must be at least 2 characters")
        if len(name) < 1:
            errors.append("Name is required")
        if len(lname) < 2:
            errors.append("Last Name must be at least 2 characters")
        if len(lname) < 1:
            errors.append("Last Name is required")
        if len(email) < 1:
            errors.append("Email is required")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Email not valid")
        if len(password) < 8:
            errors.append("Password must be 8 characters or more")
        if len(password) < 1:
            errors.append("Password is required")
        if len(confirm) < 1:
            errors.append("Confirm password is required")
        if confirm != password:
            errors.append("Confirm password should match your password")

        response= {
            "errors":errors,
            "valid":True,
            "user":None,
            "id": None
        }

        if len(errors) > 0:
            response["valid"] = False
            response['errors'] = errors
        else:
            response['user'] = User.objects.create(
                name=name,
                lname=lname,
                email=email.lower(),
                password=password,
            )
            matchingEmail = User.objects.filter(email=email)
            response['id'] = matchingEmail[0].id
        return response

    def login(self, email, password):
        errors = []
        
        response = {
            "errors": errors,
            "valid": True,
            "user": None,
            "id": None
        }

        matchingEmail = User.objects.filter(email=email)
        if len(matchingEmail) > 0:
            if password == matchingEmail[0].password:
                response['valid'] = True
                response['id'] = matchingEmail[0].id
            else:
                errors.append("Incorrect password")
        else:
            errors.append("Incorrect email")

        if len(errors) > 0:
            response['errors'] = errors
            response['valid'] = False

        return response

    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "4 characters"
        if len(postData['lname']) < 3:
            errors["lname"] = "3 characters"
        return errors


class QuoteManager(models.Manager):
    def basic_validator1(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors["author"] = "Blog name should be at least 5 characters"
        if len(postData['quote']) < 10:
            errors["quote"] = "Blog description should be at least 10 characters"
        return errors

class User(models.Model):
    name = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"Name: {self.name}, Last Name: {self.lname}"


class Quote(models.Model):
    message_body = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="messages")
    author = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()