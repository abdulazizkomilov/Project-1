from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Post, User, Comment
from django.views.decorators.csrf import csrf_exempt
from .forms import SignupForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'home.html', context)


def blogs(request):
    categories = Category.objects.all()
    
    if request.user.is_authenticated:
        exclude = [i.slug for i in request.user.exclude_posts.all()] 
        posts = Post.objects.exclude(slug__in=exclude)
    else:
        posts = Post.objects.all()
    context = {
        'categories': categories,
        'posts': posts,
    }
    return render(request, 'blogs.html', context)



@csrf_exempt
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('blog:home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'registration/login.html')

@csrf_exempt
def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@csrf_exempt
def registerPage(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
    else:
        form = SignupForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registration/sign_up.html', context)


@login_required
def favourite_list(request):
    posts_list = Post.objects.filter(favourites=request.user)
    return render(request,
                  'components/favourites.html',
                  {'posts_list': posts_list})


@login_required
@csrf_exempt
def favourite_add(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@csrf_exempt
def post_remove_add(request, id):
    user = request.user
    post = get_object_or_404(Post, id=id)
    user.exclude_posts.add(post)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@csrf_exempt
def post_remove(request, id):
    user = request.user
    post = user.exclude_posts.get(id=id)
    user.exclude_posts.remove(post)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@csrf_exempt
def removed_list(request):
    posts_list = request.user.exclude_posts.all()
    context = {'posts_list': posts_list}
    return render(request, 'components/removed.html', context)


def single(request, name, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comment_set.all().order_by('-created')
    comments_count = comments.count()
    
    if post:
        post.views = post.views + 1
        post.save()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            try:
                parent = comment_form.cleaned_data['parent']
            except:
                parent=None

        new_comment = Comment(body=body, user=request.user, post=post, parent=parent)
        new_comment.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
        'comments_count': comments_count,
    }

    return render(request, 'single.html', context)


@login_required
@csrf_exempt
def like_dislike(request, id):
    post = get_object_or_404(Post, id=id)
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



@login_required
@csrf_exempt
def follow(request, id):
    user = request.user
    category = get_object_or_404(Category, id=id)
    user.follow.add(category)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@csrf_exempt
def unfollow(request, id):
    user = request.user
    if user.follow.filter(id=id).exists():
        category = user.follow.get(id=id)
    user.follow.remove(category)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    