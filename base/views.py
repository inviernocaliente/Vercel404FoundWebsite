from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, Lesson, UserProgress, LessonPage, UserLessonProgress
from .forms import RoomForm, UserForm, MyUserCreationForm, LessonPageForm
from django.utils.safestring import mark_safe
from django.views.generic.edit import UpdateView
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
        # Create a UserLessonProgress entry for each lesson if it doesn't exist
        for lesson in lessons:
            UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)

        # Get the progress of each lesson for the user
        user_lesson_progress = UserLessonProgress.objects.filter(user=user)
        lesson_progress_dict = {progress.lesson_id: progress.is_completed for progress in user_lesson_progress}

    # Create a list of tuples containing lessons and their progress status
    lessons_with_progress = [(lesson, lesson_progress_dict.get(lesson.id)) for lesson in lessons]


    return render(request, 'base/testlessonspage1.html', {'lessons_with_progress': lessons_with_progress})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, LessonPage, UserProgress

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, LessonPage, UserProgress, UserLessonProgress

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lesson, LessonPage, UserProgress, UserLessonProgress

def lesson_redirect(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    user = request.user if request.user.is_authenticated else None

    # Get all lesson pages for the lesson
    lesson_pages = LessonPage.objects.filter(lesson=lesson)

    # Get all UserProgress objects for the lesson pages
    user_progresses = UserProgress.objects.filter(user=user, lesson_page__in=lesson_pages)

    # Check if UserProgress objects exist for all lesson pages
    if user_progresses.count() == lesson_pages.count():
        # Check if all UserProgress objects are completed
        if all(progress.is_completed for progress in user_progresses):
            # All lesson pages are completed, redirect to the last lesson page
            last_lesson_page = lesson_pages.order_by('-order').first()
            return redirect('lesson_page_detail', lesson_id=lesson_id, lesson_page_id=last_lesson_page.pk)
        else:
            # Not all lesson pages are completed, redirect to the first uncompleted lesson page
            first_uncompleted_page = next((progress.lesson_page for progress in user_progresses if not progress.is_completed), None)
            return redirect('lesson_page_detail', lesson_id=lesson_id, lesson_page_id=first_uncompleted_page.pk)
    else:
        # Not all lesson pages have UserProgress objects, create them and redirect to the first one
        for lesson_page in lesson_pages:
            UserProgress.objects.get_or_create(user=user, lesson_page=lesson_page, defaults={'is_completed': False})
        first_lesson_page = lesson_pages.order_by('order').first()
        return redirect('lesson_page_detail', lesson_id=lesson_id, lesson_page_id=first_lesson_page.pk)

    

def lesson_page_detail(request, lesson_id, lesson_page_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson_page = get_object_or_404(LessonPage, pk=lesson_page_id)
    user = request.user if request.user.is_authenticated else None

    # Get the next and previous lesson pages
    next_lesson_page = LessonPage.objects.filter(lesson=lesson, order__gt=lesson_page.order).order_by('order').first()
    prev_lesson_page = LessonPage.objects.filter(lesson=lesson, order__lt=lesson_page.order).order_by('-order').first()

    context = {
        'lesson': lesson,
        'lesson_page': lesson_page,
        'next_lesson_page': next_lesson_page,
        'prev_lesson_page': prev_lesson_page,
    }

    return render(request, 'base/testpage.html', context)

def complete_lesson(request, lesson_page_id):
    lesson_page = get_object_or_404(LessonPage, id=lesson_page_id)
    lesson = lesson_page.lesson
    user = request.user

    if user.is_authenticated:
        # Mark the lesson page as completed
        user_progress, created = UserProgress.objects.get_or_create(user=user, lesson_page=lesson_page)
        user_progress.is_completed = True
        user_progress.save()

        # Check if all lesson pages of the lesson are completed
        lesson_pages = LessonPage.objects.filter(lesson=lesson)
        user_progresses = UserProgress.objects.filter(user=user, lesson_page__in=lesson_pages)
        if all(progress.is_completed for progress in user_progresses):
            # If all lesson pages are completed, mark the lesson as completed
            user_lesson_progress, created = UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)
            user_lesson_progress.is_completed = True
            user_lesson_progress.save()

    return redirect('home')  # Or redirect to another page

def aboutPage(request):
    return render(request, 'base/aboutPage.html')

def opportunitiesPage(request):
    return render(request, 'base/opportunitiespage.html')
#----------------------Admin Stuff ---------------------

def adminHome(request):
    if request.user.is_superuser:
        lessons = Lesson.objects.all()
        return render(request, 'base/adminHome.html', {'lessons': lessons})
    else:
        return redirect('home')

def lessonAdminPage(request, lesson_id): 
    if request.user.is_superuser:
        lesson = Lesson.objects.get(id=lesson_id)
        lesson_pages = lesson.lesson_pages.all()
        context = {
        'lesson': lesson,
        'lesson_pages': lesson_pages,
        }
        return render(request, 'base/lessonAdminPage.html', context)
    else:
        return redirect('home')

def create_lesson_page(request, lesson_id):
    
    if request.user.is_superuser:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        form = LessonPageForm(request.POST)
        if request.method == 'POST':
            form = LessonPageForm(request.POST)
        if form.is_valid():
            lesson_page = form.save(commit=False)
            lesson_page.lesson = lesson
            lesson_page.save()
            return redirect('lesson_detail_admin', lesson_id=lesson.id)
        else:
            form = LessonPageForm()
        context = {'lesson': lesson, 'form': form}
        return render(request, 'base/createLessonPage.html', context)
    else:
        return redirect('home')

    
    
    

def delete_lesson_page(request, lesson_id, lesson_page_id):
    if request.user.is_superuser:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson_page = get_object_or_404(LessonPage, id=lesson_page_id)
    
        if request.method == 'POST':
            lesson_page.delete()
            return redirect('lesson_detail_admin', lesson_id=lesson.id)

        context = {'lesson': lesson, 'lesson_page': lesson_page}
        return render(request, 'base/deleteLessonPage.html', context)
    
    else:
        return redirect('home')

def lesson_detail_admin(request, lesson_id):
    if request.user.is_superuser:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson_pages = lesson.lesson_pages.all().order_by('order')
        context = {'lesson': lesson, 'lesson_pages': lesson_pages}
        return render(request, 'base/lessonDetailAdmin.html', context)    
    else:
        return render('home')

def edit_lesson_page(request, lesson_id, lesson_page_id):
    if request.user.is_superuser:
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lesson_page = get_object_or_404(LessonPage, pk=lesson_page_id)

        if request.method == 'POST':
            form = LessonPageForm(request.POST, instance=lesson_page)
            if form.is_valid():
                form.save()
                return redirect('lesson_detail', lesson_id=lesson.id)
        else:
            form = LessonPageForm(instance=lesson_page)

        return render(request, 'base/lesson_page_edit_admin.html', {'form': form, 'lesson_page': lesson_page})
    else:
        return redirect('home')
#----------------------------------------------------------------------

# def lesson_edit_admin(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson_pages = lesson.lesson_pages.all().order_by('order')
#     context = {'lesson': lesson, 'lesson_pages': lesson_pages}
#     return render(request, 'base/lessonDetailAdmin.html', context)




# def complete_lesson(request, lesson_page_id): #need to update the url
#     lesson_page = get_object_or_404(LessonPage, id=lesson_page_id)
#     if request.user.is_authenticated:
#         user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
#         user_progress.is_completed = True
#         user_progress.save()
#         print("user_progress")
#         pass
#     else:
#         pass
#     return redirect('home')  # Or redirect to another page



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










# @login_required #need to edit to make it work with anonimous yusers
# def lessons_page(request):
#     lessons = Lesson.objects.all()
#     user = request.user

#     # Get user progress for all lessons
#     user_progress = UserProgress.objects.filter(user=user)
#     lesson_progress_dict = {progress.lesson_page.lesson_id: progress.is_completed for progress in user_progress}

#     # Create a list of tuples containing lessons and their progress status
#     lessons_with_progress = [(lesson, lesson_progress_dict.get(lesson.id, False)) for lesson in lessons]

#     #return redirect('home')

#     return render(request, 'base/lessons_page.html', {'lessons_with_progress': lessons_with_progress})


# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)

#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         # Find the user's progress for the current lesson
#         user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson_page=lesson.lesson_pages.first())

#         # If the lesson page is completed, redirect to the first uncompleted lesson page
#         if user_progress.is_completed:
#             next_uncompleted_page = UserProgress.objects.filter(user=request.user, is_completed=False).first()
#             if next_uncompleted_page and next_uncompleted_page.lesson_page:
#                 return redirect('lesson_page_detail', lesson_id=lesson_id, lesson_page_id=next_uncompleted_page.lesson_page.id)

#     # If the user is not authenticated or has no progress, create a new instance for them
#     else:
#         user_progress, created = UserProgress.objects.get_or_create(user=None, lesson_page=lesson.lesson_pages.first())

#     # Handle form submission for logged-in users
#     if request.method == 'POST' and request.user.is_authenticated:
#         # Mark the lesson as completed for the user
#         user_progress.is_completed = True
#         user_progress.save()
#         return redirect('home')  # Or redirect to another page

#     return render(request, 'home.html')





# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     print('entered')
    
#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         print('user authenticated')
#         #user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
#         user_progress = UserProgress.objects.filter(user=request.user, is_completed=False).first()
#         if user_progress:
#             # Redirect to the first uncompleted lesson
#                 print('redirected success')
#                 return redirect('lesson_page_detail', lesson_id=lesson.id, lesson_page_id=user_progress.lesson_page.id)
#         else:
#             print('no user progress')
        

#     else:
#         print('anonimoose')
#         # For anonymous users, create progress without user information
#         user_progress, created = UserProgress.objects.get_or_create(user=None, lesson=lesson)
#         first_lesson = Lesson.objects.first()
#         if first_lesson:
#             print('anonimoose')
#             return redirect('lesson_page_detail', lesson_id=lesson.id, lesson_page_id=first_lesson.id)
        

    
#     # Handle form submission for logged-in users
#     if request.method == 'POST' and request.user.is_authenticated:
#         #user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)

#         user_progress.is_completed = True
#         user_progress.save()
#         return redirect('home')  # Or redirect to another page

#     return render(request, 'home')











# @login_required
# def lesson_page_detail(request, lesson_id, lesson_page_id):
#     lesson_page = get_object_or_404(LessonPage, id=lesson_page_id)
#     user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson_page=lesson_page)

#     if request.method == 'POST':
#         # Assuming you want to mark the lesson page as completed when the form is submitted
#         user_progress.is_completed = True
#         user_progress.save()

#     rev_lesson_page = LessonPage.objects.filter(order__lt=lesson_page.order).last()
#     next_lesson_page = LessonPage.objects.filter(order__gt=lesson_page.order).first()

#     return render(request,'home', {'lesson_page': lesson_page, 'prev_lesson_page': prev_lesson_page, 'next_lesson_page': next_lesson_page})

#{'lesson_page': lesson_page, 'prev_lesson_page': prev_lesson_page, 'next_lesson_page': next_lesson_page}




# def lesson_page_detail(request, lesson_id, lesson_page_order):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson_page = get_object_or_404(LessonPage, lesson=lesson, order=lesson_page_order)

#     if request.method == 'POST':
#         # Handle form submission for logged-in users
#         if request.user.is_authenticated:
#             user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson_page=lesson_page)
#             user_progress.is_completed = True
#             user_progress.save()

#             # Redirect to the next lesson page
#             next_lesson_page = LessonPage.objects.filter(lesson=lesson, order__gt=lesson_page_order).order_by('order').first()
#             if next_lesson_page:
#                 return redirect('base/lesson_page_detail', lesson_id=lesson.id, lesson_page_order=next_lesson_page.order)

#     #Get the previous and next lesson pages
#     prev_lesson_page = LessonPage.objects.filter(lesson=lesson, order__lt=lesson_page_order).order_by('-order').first()
#     next_lesson_page = LessonPage.objects.filter(lesson=lesson, order__gt=lesson_page_order).order_by('order').first()

#     return render(request, 'lesson_page_detail.html', {
#         'lesson_page': lesson_page,
#         'prev_lesson_page': prev_lesson_page,
#         'next_lesson_page': next_lesson_page,
#     })






# def lesson_page_detail(request, lesson_id, lesson_page_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     lesson_page = get_object_or_404(LessonPage, id=lesson_page_id)



#     if request.method == 'POST':
#         # Handle form submission for logged-in users
#         if request.user.is_authenticated:
#             user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson_page=lesson_page)
#             user_progress.is_completed = True
#             user_progress.save()

#             # Redirect to the next lesson page
#             next_lesson_page = LessonPage.objects.filter(id__gt=lesson_page_id).order_by('id').first()
#             if next_lesson_page:
#                 return redirect('lesson_page_detail', lesson_page_id=next_lesson_page.id)

#     # Get the previous and next lesson pages
#     prev_lesson_page = LessonPage.objects.filter(id__lt=lesson_page_id).order_by('-id').first()
#     next_lesson_page = LessonPage.objects.filter(id__gt=lesson_page_id).order_by('id').first()

#     return render(request, 'lesson_page_detail.html', {
#         'lesson_page': lesson_page,
#         'prev_lesson_page': prev_lesson_page,
#         'next_lesson_page': next_lesson_page,
#     })


# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
    
#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         user_progress, created = UserProgress.objects.get_or_create(user=request.user, lesson=lesson)
#     else:
#         # For anonymous users, create progress without user information
#         user_progress, created = UserProgress.objects.get_or_create(user=None, lesson=lesson)
    
#     # Handle form submission for logged-in users
#     if request.method == 'POST' and request.user.is_authenticated:
#         user_progress.is_completed = True
#         user_progress.save()
#         return redirect('home')  # Or redirect to another page

#     return render(request, 'lesson_detail.html', {'lesson': lesson})

