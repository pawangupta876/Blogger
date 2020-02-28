from django.shortcuts import render, HttpResponse, redirect
from App1.forms import UserProfileForm, UserForm, User_Post_Form
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo, User_Post,  Friend, Review, Like, User_Message
from django.contrib.auth.models import User


def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user = User.objects.get(username=username)
        if user:
            return redirect('App1:user_login')
        
        else:    
            user1,created = User.objects.get_or_create(username=username,first_name=first_name, last_name=last_name, email=email)
            if created:
                user1.set_password(password)
                user1.save()
                return redirect('App1:user_login')
            else:
               return redirect('App1:register')
    else:

        form1 = UserForm()
        
        args = {'form1':form1}
        return render(request, 'App1/register.html',args)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('App1:home_page')
            else:
                return redirect('App1:register')
        else:
            return redirect('App1:register')
    else:
        return render(request, 'App1/login.html')


@login_required
def home_page(request):
    if request.method == 'POST':
        post = request.POST.get('data')
        image=request.FILES.get('file1')
        if post or image:
            post = User_Post.objects.create(post = post ,user = request.user, image=image)
            post.save()
            
    
    people = User.objects.exclude(id=request.user.id).order_by('username')
    user=request.user
    friend_list = Friend.objects.filter(user = user).order_by('friends')
    posts = User_Post.objects.filter(user = user).order_by('-time')
    pic = User_Post_Form()
    args = {'user':request.user, 'friends':people, 'posts':posts, 'pic':pic, 'list':friend_list}
    return render(request, 'App1/user.html',args)


@login_required
def user_logout(request):
    logout(request)
    return redirect('App1:register')


@login_required
def profile(request):
    userprofile,created = UserProfileInfo.objects.get_or_create(user = request.user)
   
    if request.method == 'POST':
      
        user_profile = UserProfileForm(request.POST, request.FILES,instance = userprofile)
        if user_profile.is_valid():
            user_profile.save()
            return redirect('App1:home_page')
    
        else:
            return redirect('App1:profile')

    else:
        profile_form = UserProfileForm(instance = userprofile)
        return render(request, 'App1/profile.html', {'profile_form':profile_form, 'user':request.user})


    
@login_required
def profile_view(request, pk):
    
    user1 = User.objects.get(pk=pk)
    user2 = request.user
    if request.method == 'POST':
        Friend.objects.get_or_create(user=user2, friends=user1)
        Friend.objects.get_or_create(user=user1, friends=user2)
        return redirect('App1:home_page')

    posts = User_Post.objects.all().filter(user = user1).order_by('-time')
    args = {'user':user1, 'posts':posts, 'user1':request.user} 
    return render(request, 'App1/profile_view.html', args)


@login_required
def comments(request, pk):
    if request.method == 'POST':
        message = request.POST.get('message')
        value = request.POST.get('value')
        if message:
            friend = Friend.objects.get(pk=pk)
            user1 = User.objects.get(username = friend.friends)
            user2 = User.objects.get(username = request.user)
            friend_ob1 = Friend.objects.get(user = user2, friends = user1)
            friend_ob2 = Friend.objects.get(user = user1, friends = user2)
            User_Message.objects.create(friend_model = friend_ob1, message = message, sender = user2)
            User_Message.objects.create(friend_model = friend_ob2, message = message, sender = user2)
        if value:

            friend = Friend.objects.get(pk=pk)
            user1 = User.objects.get(username = friend.friends)
            user2 = User.objects.get(username = request.user)
            Friend.objects.get(user = user2, friends = user1).delete()
            Friend.objects.get(user = user1, friends = user2).delete()
            return redirect('App1:home_page')

    friend = Friend.objects.get(pk=pk)
    mess1 = User_Message.objects.filter(friend_model = friend)
    user1 = User.objects.get(username = friend.friends)
    posts = User_Post.objects.all().filter(user = user1).order_by('-time')
    args = {'user':user1, 'posts':posts,'pk':pk, 'message':mess1, 'user1':request.user}
    return render(request, 'App1/comments.html', args)

   
@login_required
def comment_done(request, pk):

    if request.method == 'POST':
        comment = request.POST.get('comment')
        comment1 = request.POST.get('comment1')
        if comment:
            user_post = User_Post.objects.get(pk = pk)
            Review.objects.create(user_post = user_post, comments = comment, user=request.user)
        if comment1:
            user_post = User_Post.objects.get(pk = pk)
            likes, created = Like.objects.get_or_create(liked_by = request.user, user_post = user_post)
            if not created:
                Like.objects.get(liked_by = request.user, user_post = user_post).delete()
            user = user_post.user
            user = Friend.objects.get(user = request.user, friends = user)
            pk1 = user.pk
            return redirect('App1:comments', pk1)
    
    user_post = User_Post.objects.get(pk = pk)
    likes = Like.objects.filter(user_post = user_post).count()
    user = user_post.user
    comments = Review.objects.filter(user_post = user_post).order_by('-time')
    friends = Friend.objects.filter(user = user).order_by('friends')
    args = {'comments':comments, 'user_post':user_post, 'user':user, 'friends':friends, 'likes':likes, 'user1':request.user}
    return render(request, 'App1/all_comments.html', args)

@login_required
def returned(request, pk):
    user = Friend.objects.get(pk = pk)
    user = User.objects.get(username = user.friends)
    x = user.pk
    return redirect('App1:profile_view', x)