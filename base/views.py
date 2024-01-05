from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, Lesson, UserProgress
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AnonymousUser



# Create your views here.

# rooms = [
#     {'id':1, 'name':'Lets learn Python!'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developement'},
# ]

#------------------------------------------------------ Chat app section --------------------------------------------------------------------------#
def loginPage(request):

    page = 'login'
    previous_page = request.META.get('HTTP_REFERER')


    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            next_page = request.GET.get('next') or previous_page or 'home'
            return redirect(next_page)
        else:
            messages.error(request, 'Username OR Password is Invalid')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False)
           user.username = user.username.lower()
           user.save()
           login(request, user)
           return redirect('home')
        else: 
            messages.error(request, mark_safe('An error: invalid form.<br/>Make sure your email is valid.<br/>Then make sure your passwords match and are:<br/>*at least 8 characters<br/>*not entirely numeric<br/>*commonly used.'))

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    return render(request, 'base/home.html')

def home_studybuddy(request):
    q = request.GET.get('q') if request.GET.get('q') !=  None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages': room_messages}
    return render(request, 'base/home_studybuddy.html', context)




def room(request, pk):
    if request.user.is_authenticated == False:
        return redirect('login')
    else:
        room = Room.objects.get(id=pk)
        room_messages = room.message_set.all()#sdfsdfsdf
        participants = room.participants.all()

        if request.method == 'POST':
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)
        context = {'room':room, 'room_messages':room_messages, 'participants':participants}
        return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms': rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('lessons_page')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' :room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You cannot!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' :message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        print('valid')
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') !=  None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

#------------------------------------------------------------------------------------ end chat app section --------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------- start course section -------------------------------------------------------------------------------#

def lessons_page(request):
    lessons = Lesson.objects.all()
    user = request.user

    # Initialize user_progress based on user type
    if isinstance(user, AnonymousUser):
        lesson_progress_dict = {}  # For anonymous users
    else:
        # Assuming each lesson has a corresponding UserProgress entry for the user
        user_progress = UserProgress.objects.filter(user=user)
        lesson_progress_dict = {progress.lesson_id: progress.is_completed for progress in user_progress}

    # Create a list of tuples containing lessons and their progress status
    lessons_with_progress = [(lesson, lesson_progress_dict.get(lesson.id)) for lesson in lessons]
    
    return render(request, 'base/lessons_page.html', {'lessons_with_progress': lessons_with_progress})


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
    else:
        # For anonymous users, create progress without user information
        user_progress, created = UserProgress.objects.get_or_create(user=None, lesson=lesson)
    
    # Handle form submission for logged-in users
    if request.method == 'POST' and request.user.is_authenticated:
        user_progress.is_completed = True
        user_progress.save()
        return redirect('home')  # Or redirect to another page
    
    return render(request, 'lesson_detail.html', {'lesson': lesson})


def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user.is_authenticated:
        user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
        user_progress.is_completed = True
        user_progress.save()
        print("user_progress")
        pass
    else:
        pass
    return redirect('home')  # Or redirect to another page

def aboutPage(request):
    return render(request, 'base/aboutPage.html')













# def view_lesson(request, user_id, lesson_id):
#     user = get_object_or_404(User, id=user_id)
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     user_lesson_progress, created = UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)
#     # Render the lesson view with user_lesson_progress data
#     return render(request, 'view_lesson.html', {'user_lesson_progress': user_lesson_progress})

# def lesson_progress(request, user_id, lesson_id):
#     user = get_object_or_404(User, id=user_id)
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     user_lesson_progress, created = UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)
    
#     if request.method == 'POST':
#         # Update user_lesson_progress fields based on form data
#         user_lesson_progress.progress = request.POST.get('progress', 0)
#         user_lesson_progress.entered = request.POST.get('entered', False)
#         user_lesson_progress.finished = request.POST.get('finished', False)
#         user_lesson_progress.save()
#         # Redirect to lesson view or user dashboard
#         return redirect('lesson_progress', user_id=user.id, lesson_id=lesson.id)
    
#     # Render the lesson view with user_lesson_progress data for GET requests
#     return render(request, 'lesson_progress.html', {'user_lesson_progress': user_lesson_progress})


# def lessons_page(request):
#     lessons = Lesson.objects.all()
#     user = request.user

#     if isinstance(user, AnonymousUser):
#         user_progress = None  # Handle anonymous user differently
#     else:
#         user_progress, created = UserProgress.objects.get_or_create(user=user, lesson=lesson)

#     #user_progress = UserProgress.objects.filter(user=user)
    
#     lesson_progress_dict = {progress.lesson_id: progress.is_completed for progress in user_progress}
    
#     # Create a list of tuples containing lessons and their progress status
#     lessons_with_progress = [(lesson, lesson_progress_dict.get(lesson.id)) for lesson in lessons]
    
#     return render(request, 'base/lessons_page.html', {'lessons_with_progress': lessons_with_progress})

