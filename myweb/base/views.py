from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Course
from .models import User
from .models import Level
from .models import Group
from .models import Comment
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, CourseForm, UserForm
# from .seeder import seeder_func
from django.contrib import messages

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # seeder_func()
    courses = Course.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(group__name__icontains=q) | Q(level__level__icontains=q))
    courses = list(dict.fromkeys(courses))
    # courses = Course.objects.all()
    heading = "Tech Courses"
    levels = Level.objects.all()
    context = {"courses": courses, "heading": heading, 'levels': levels}
    return render(request, 'base/home.html', context)



def about(request):
    return render(request, 'base/about.html')

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    # courses = user.courses.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    courses = user.courses.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(group__name__icontains=q) | Q(level__level__icontains=q))
    courses = list(dict.fromkeys(courses))
    heading = "My Courses"
    levels = Level.objects.all()
    context = {"courses": courses, "heading": heading, 'levels': levels}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def adding(request, id):
    user = request.user
    course = Course.objects.get(id=id)
    user.courses.add(course)
    return redirect('profile', user.id)

@login_required(login_url='login')
def delete(request, id):
    obj = Course.objects.get(id=id)

    if request.method == 'POST':
        request.user.courses.remove(obj)
        return redirect('profile', request.user.id)


    return render(request, 'base/delete.html', {'obj': obj})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', request.user.id)
        else:
            messages.error(request, 'User or Password is not correct!')

    return render(request, 'base/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = MyUserCreationForm

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)

        else:
            messages.error(request, 'Your Password is not valid. Create Another Password')

    context = {'form': form}
    return render(request, 'base/register.html', context)


# def add_course(request):
#     groups = Group.objects.all()
#     levels = Level.objects.all()
#     form = CourseForm()
#
#     if request.method == 'POST':
#         course_group = request.POST.get('group')
#         course_level = request.POST.get('level')
#
#
#         group, created = Group.objects.get_or_create(name=course_group)
#         level, created = Level.objects.get_or_create(level=course_level)
#
#         form = CourseForm(request.POST)
#         new_course = Course(picture=request.FILES['picture'], name=form.data['name'],
#                             time=form.data['time'], format=form.data['format'], price=form.data['price'],
#                             group=group, description=form.data['description'], file=request.FILES['file'],
#                             creator=request.user)
#         if not (Course.objects.filter(file=request.FILES['file']) or Course.objects.filter(name=new_course.name)):
#             new_course.save()
#             new_course.level.add(level)
#         return redirect('home')
#
#     context = {'form': form, 'groups': groups, 'levels': levels}
#     return render(request, 'base/add_course.html', context)



def add_course(request):
    groups = Group.objects.all()
    levels = Level.objects.all()
    form = CourseForm()

    if request.method == 'POST':
        course_group = request.POST.get('group')
        course_level = request.POST.get('level')

        group, created = Group.objects.get_or_create(name=course_group)
        level, created = Level.objects.get_or_create(level=course_level)

        form = CourseForm(request.POST)

        new_course =Course(picture=request.FILES['picture'],
                            name=form.data['name'],
                            time=form.data['time'],
                            format=form.data['format'],
                            price=form.data['price'],
                            group=group,
                            description=form.data['description'],
                            file=request.FILES['file'],
                            creator=request.user)
        print(Course.objects.filter(name=new_course.name))
        if not (Course.objects.filter(file=request.FILES['file']) or Course.objects.filter(name=new_course.name)):
            new_course.save()
            new_course.level.add(level)
        else:
            messages.error(request, 'File with same name already exists...')
        return redirect('home')

    context = {'form': form, 'groups': groups, 'levels': levels}
    return render(request, 'base/add_course.html', context)




def open(request, id):
    course = Course.objects.get(id=id)
    course_comments = course.comment_set.all()  # .order_by('-created')
    if request.method == "POST":
        Comment.objects.create(
            user=request.user,
            course=course,
            body=request.POST.get('body')
        )
    return render(request, 'base/open.html', {'course': course, 'comments': course_comments})


def delete_course(request, id):
    obj = Course.objects.get(id=id)

    if request.method == "POST":
        obj.picture.delete()
        obj.file.delete()
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)

    context = {'form': form}
    return render(request, 'base/update_user.html', context)

def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    course = comment.course
    if request.method == 'POST':
        comment.delete()
        return redirect('open', course.id)

    return render(request, 'base/delete.html', {'obj': comment})
