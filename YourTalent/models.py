from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
class User(AbstractUser):
    pass
class Authentication(models.Model):
    user_authentication = models.ForeignKey(User,on_delete=models.CASCADE)
    boolean_authenticate = models.BooleanField()
    authentication_code = models.IntegerField()
    role = models.TextField()
class Novidpart(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField(unique=True)
    description = models.TextField()
    category = models.TextField()
    file = models.FileField(upload_to = 'YourTalent/Novidpart/')
    date = models.DateTimeField(auto_now_add=True)
    
    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)
class Vidpart(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField(unique=True)
    description = models.TextField()
    category = models.TextField()
    videoid = models.TextField()
    thumbnail = models.FileField(upload_to = 'YourTalent/thumbnail/')
    date = models.DateTimeField(auto_now_add=True)
    
    def delete(self,*args,**kwargs):
        self.thumbnail.delete()
        super().delete(*args,**kwargs)
class Notifications(models.Model):
    notif_recruiter = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notif_recruiter")
    notif_contencreator = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notif_contencreator")
    notif_thecontent_title = models.TextField()
    category = models.TextField()
    content_id = models.BigIntegerField()
    seen = models.BooleanField()
class Interestnovidpart(models.Model):
    interest_recruiter = models.ForeignKey(User,on_delete=models.CASCADE)
    interest_file = models.ForeignKey(Novidpart,on_delete=models.CASCADE)
    category = models.TextField()
    def serialize(self):
        return{
            "content_id":self.interest_file.id
        }
class Interestvidpart(models.Model):
    interest_recruiter = models.ForeignKey(User,on_delete=models.CASCADE)
    interest_vid = models.ForeignKey(Vidpart,on_delete=models.CASCADE)
    category = models.TextField()