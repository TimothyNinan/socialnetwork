from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from .models import User, Posts, Following
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse



def index(request):
    if (request.method == 'POST'):
        user = request.user
        body = request.POST["content"]
        posting = Posts(poster=user, content=body)
        posting.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        page_number = int(request.GET.get('page', '1'))
        posts = Posts.objects.order_by('-time').all()
        paginator = Paginator(posts, 10)
        pageposts = paginator.get_page(page_number)
        totpages = paginator.num_pages
        return render(request, "network/index.html", {
            'posts': pageposts,
            'range_pages': range(1, totpages+1),
            'current_page': page_number
        })


@csrf_exempt
@login_required
def edit(request, post_id):
    # Query for requested email
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def like(request, post_id):
    # Query for requested email
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        initial_likes = post.likes
        if data.get("likes") is not None:
            new_likes = data["likes"]
        if new_likes > initial_likes:
            post.liker.add(request.user)
        else:
            post.liker.remove(request.user)
        post.likes = new_likes
        post.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@login_required
def following(request):
    page_number = int(request.GET.get('page', '1'))
    follow = Following.objects.get(user=request.user)
    followees = follow.followee.all()
    totposts = []
    for followee in followees:
        posts = Posts.objects.order_by('-time').filter(poster=followee)
        for post in posts:
            totposts.append(post)
    paginator = Paginator(totposts, 10)
    pageposts = paginator.get_page(page_number)
    totpages = paginator.num_pages
    return render(request, "network/following.html", {
        'posts': pageposts,
        'range_pages': range(1, totpages+1),
        'current_page': page_number
    })

def profile(request, username):
    if (request.method == 'POST'):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "network/error.html", {
                'message': "Requested User Does Not Exist"
            })

        try:
            yesfollow = request.POST['follow']
        except MultiValueDictKeyError:
            yesfollow = "No"
        try:
            yesunfollow = request.POST['unfollow']
        except MultiValueDictKeyError:
            yesunfollow = "No"
        if yesfollow == 'Follow':
            user.followers += 1
            user.save()
            follow = Following.objects.get(user=request.user)
            follow.followee.add(user)
            follow.save()
        elif yesunfollow == 'Unfollow':
            user.followers -= 1
            user.save()
            follow = Following.objects.get(user=request.user)
            follow.followee.remove(user)
            follow.save()

        return HttpResponseRedirect(f"/{username}")

    else:
        page_number = int(request.GET.get('page', '1'))
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "network/error.html", {
                'message': "Requested User Does Not Exist"
            })
        
        try:
            posts = Posts.objects.order_by('-time').filter(poster=user)
        except Posts.DoesNotExist:
            posts = None

        paginator = Paginator(posts, 10)
        pageposts = paginator.get_page(page_number)
        totpages = paginator.num_pages

        isfollowing = False
        isposter = False

        if request.user.is_authenticated:
            
            follow = Following.objects.get(user=request.user)
            if user in follow.followee.all():
                isfollowing = True
            if request.user == user:
                isposter = True
        else:
            isposter = True
        fallowss = Following.objects.get(user=user)
        follows = fallowss.followee.all()

        return render(request, 'network/profile.html', {
            'user': user,
            'posts': pageposts,
            'isfollowing': isfollowing,
            'follows': follows,
            'isposter': isposter,
            'range_pages': range(1, totpages+1),
            'current_page': page_number
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "User with this email already exists. Please log in."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
