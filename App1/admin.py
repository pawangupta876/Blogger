from django.contrib import admin
from App1.models import UserProfileInfo, User_Post, Friend, Review, Like, User_Message

admin.site.register(UserProfileInfo)
admin.site.register(User_Post)
admin.site.register(Friend)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(User_Message)
# Register your models here.
