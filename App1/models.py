from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete = models.CASCADE)

    address = models.CharField(max_length=100, blank=True)
    contact_number = models.IntegerField(default='0')
    qualification = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='propfile_pics', default='propfile_pics\download_1.jpg')
    gender = models.CharField(max_length=6, blank=False)

    def __str__(self):
        return self.user.username 

class User_Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    
    post = models.CharField(max_length=500, blank=True)
    time = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to= 'profile_pic', blank=True)
   
    def __str__(self):
        return str(self.post)+str(self.image)

class Friend(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    friends = models.ForeignKey(User, related_name="dost",on_delete = models.CASCADE) 
 

    def __str__(self):
        return self.friends.username

class Review(models.Model):
    user_post = models.ForeignKey(User_Post, related_name="review",on_delete = models.CASCADE)
    comments = models.CharField(max_length=100, blank=True)
    time = models.DateTimeField(auto_now_add = True)
    user = models.CharField(max_length=20, blank=True)
   
    def __str__(self):
        return self.comments

class Like(models.Model):
    user_post = models.ForeignKey(User_Post,on_delete = models.CASCADE)
    liked_by = models.ForeignKey(User,on_delete = models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
         return str(self.likes)

class User_Message(models.Model):
    friend_model = models.ForeignKey(Friend,on_delete = models.CASCADE)
    message = models.CharField(max_length = 200)
    sender = models.CharField(max_length=10)

    def __str__(self):
        return self.message
