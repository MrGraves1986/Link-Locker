from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postdata):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postdata['first_name']) < 2: 
            errors['first_name']="First name must be at least 2 characters"

        if len(postdata['last_name']) < 2:
            errors['last_name']="Last name must be at least 2 characters."

        if not email_check.match(postdata['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address.")

        if len(postdata['pw']) < 8:
            errors['pw']="Password must be at least 8 characters."

        if postdata['confirm_pw'] != postdata['pw']:
            errors['confirm_pw']="Passwords do not match, please try again."
        return errors
       

class User(models.Model):
    first_name=models.CharField(max_length=25)
    last_name=models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

class LinkManager(models.Manager): 
    def empty_validator(self, postdata):
        errors=""
        if len(postdata['content']) < 5:
            errors="Link must be atleast 5 characters."
        return errors

class Link(models.Model):
    content=models.TextField()
    poster=models.ForeignKey(User, related_name="links", on_delete=models.CASCADE) 
    objects=LinkManager()



    
