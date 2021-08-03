import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Album, Image
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EditForm
import re

# Create your views here.


@login_required
def gallery(request):
    user_id = request.user
    album = request.GET.get('album')
    page = request.GET.get('page', 1)

    if album == None:
        images = Image.objects.filter(client=user_id).order_by('id')
    else:
        images = Image.objects.filter(client=user_id).filter(album__name=album).order_by('id')

    albums = Album.objects.filter(client=user_id)
    paginator = Paginator(images, 9)
    try:
        paged_images = paginator.page(page)
    except PageNotAnInteger:
        paged_images = paginator.page(1)
    except EmptyPage:
        paged_images = paginator.page(paginator.num_pages)

    context = {'albums': albums, 'images': images, 'user_id': user_id, 'paged_images': paged_images}

    return render(request, 'webgallery/gallery.html', context)


@login_required
def viewImage(request, pk):
    user_id = request.user
    is_user_img = check_if_this_user_photo(user_id, pk)
    if is_user_img and user_id:
        image = Image.objects.get(id=pk)
        context = {'image': image, 'user_id': user_id}
        return render(request, 'webgallery/image.html', context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def addImage(request):
    user_id = request.user
    albums = Album.objects.filter(client=user_id)

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['album'] != 'none':
            album = Album.objects.get(id=data['album'])
        elif data['album_new'] != '':
            album, created = Album.objects.get_or_create(
                name=data['album_new'],
                client=request.user
            )
        else:
            album = None

        for image in images:
            image = Image.objects.create(
                album=album,
                description=data['description'],
                image=image,
                client=request.user
            )
        messages.success(request, "Image added Successfuly!")
        return redirect('gallery')

    context = {'albums': albums}
    return render(request, 'webgallery/add.html', context)


@login_required
def editImage(request, pk):
    user_id = request.user
    is_user_img = check_if_this_user_photo(user_id, pk)
    if is_user_img:
        albums = Album.objects.filter(client=user_id)
        image = get_object_or_404(Image, id=pk)
        form = EditForm(request.POST or None, instance=image)
        context = {'albums': albums, "image": image}
        if form.is_valid():
            image = Image.objects.get(id=pk)
            album_id = image.album_id
            if album_id:
                album = Album.objects.get(id=album_id)
                last_image = check_if_last_photo(request.user, album_id)
                if last_image:
                    album.delete()
            form.save()
            messages.success(request, "Image edited Successfuly!")
            return redirect('gallery')
        context["form"] = form
        return render(request, 'webgallery/edit.html', context)
    else:
        messages.warning(request, "You are trying to edit other person's image!")
        return redirect('gallery')


@login_required
def deleteImage(request, pk):
    user_id = request.user
    is_user_img = check_if_this_user_photo(user_id, pk)
    if is_user_img:
        image = Image.objects.get(id=pk)
        album_id = image.album_id
        last_image = False
        if album_id:
            album = Album.objects.get(id=album_id)
            last_image = check_if_last_photo(request.user, album_id)
        if last_image:
            album.delete()
        if len(image.image) > 0:
            os.remove(image.image.path)
        image.delete()
        messages.success(request, "Image Deleted Successfuly")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "You are trying to delete other person's image. Don't do this :)")
        return redirect('gallery')


def check_if_this_user_photo(user_id, pk):
    image = Image.objects.filter(client=user_id).filter(id=pk)
    if not image:
        return False
    return True


def check_if_last_photo(user_id, album_id):
    count_images = Image.objects.filter(client_id=user_id).filter(album_id=album_id).count()
    if count_images == 1:
        return True
    return False


def validate_email(input):
    email_regex = re.compile(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$')
    result = email_regex.search(input)
    if result:
        return True
    return False


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with this email {email} already exists!')
                    return redirect('register')
                elif not validate_email(email):
                    messages.error(request, f'This email {email} is not valid! Please enter a valid email.')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, 'You have successfully registered your account. '
                                              'If you want start uploading images, please log in.')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match !')
            return redirect('register')
    return render(request, 'register.html')


def demo(request):
    return render(request, 'demo.html')
