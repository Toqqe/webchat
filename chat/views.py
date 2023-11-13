from django.shortcuts import render
from django.views import View
import random
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm, UpdateUserForm
from .models import ActiveRooms, CustomUser, MessagesRoom, DirectRooms, DirectMessages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from django.db.models import Q

# Create your views here.

class GuestView(View):
    
    def get(self, request):
        
        form = RegistrationForm()
        return render(request, 'chat/guest.html', {'form': form})

    def post(self,request):
        print(request.POST)
        form = RegistrationForm(request.POST)


        if form.is_valid():
            userform = form.save(commit=False)
            userform.username = userform.username.lower()
            userform.save()
            login(request,userform)
            return HttpResponseRedirect("/")
        else:
            return render(request, "chat/guest.html", {
                "form" : form
            })    
        
class LoginView(View):

    def get(self, request):
        
        form = LoginForm()

        return render(request, 'chat/login.html', {'form': form})

    def post(self,request):

        form = LoginForm(request.POST)


        if "on" in request.POST['is_guest']:

            entered_login = request.POST['username']

            username = entered_login + str(random.randint(0,100000000))
            email = "djioasjioriashihairiabfuiawehuetemp@temp.pl"
            password1 = "SAHSDUIhArghli12ghufas12431245@$!$2ASHF"
            is_guest = True

            temp_user = CustomUser(username=username, email=email, password=password1, is_guest=is_guest)
            temp_user.save()

            login(request,temp_user)


            return HttpResponseRedirect("/")
        else:
            return render(request, "chat/guest.html", {
                "form" : form
            })    


@method_decorator(login_required(login_url='/login'), name='dispatch')
class MainChat(View):

    def get(self,request):
        all_rooms = ActiveRooms.objects.all()
        user = CustomUser.objects.get(id=request.user.id)

        all_tmp_users = CustomUser.objects.filter(is_guest=True)
        context = {
            "all_rooms" : all_rooms,
            "friends_room" : user.direct_users.all(),
            #"friends_rooms" : user.friends.all(),
            "all_tmp_users" : all_tmp_users
        }
        
        return render(request, "chat/chat.html", context)
    

    def post(self, request):

        if "room-name-input" in request.POST:
            room_name = request.POST['room-name-input']
            filter_rooms = ActiveRooms.objects.filter(name=room_name).first()

            if filter_rooms:
                return HttpResponseRedirect('/chat/' + room_name)
            else:
                new_room = ActiveRooms(name=room_name)
                new_room.save()
        
                chat_content = render_to_string( "chat/test.html", { 
                    "room_name":room_name,
                    # "messages":messages,
                    "online_users":filter_rooms,
                    },
                    request=request)

                return JsonResponse({"chat_content":chat_content})
            

def search(request, search_query):

    friends = CustomUser.objects.get(id=request.user.id).friends.all().values('id')
    filtered_users = CustomUser.objects.filter(username__contains=search_query).exclude(is_superuser=True).exclude(id__in=friends).exclude(username=request.user.username)
    users_list = [ {'users' : user.username, 'user_img':user.user_img.url } for user in filtered_users ]
    return JsonResponse({"users_list":users_list})


def users(request, user_name):

    typedUser = CustomUser.objects.filter(username=user_name).first()
    currentUser = CustomUser.objects.get(id=request.user.id)

    if typedUser not in currentUser.friends.all():
        currentUser.friends.add(typedUser)
        test = DirectRooms(author=currentUser, friend=typedUser)
        test.save()
        test.users.add(currentUser, typedUser)

        return JsonResponse({"friends_list":typedUser.username,
                             "friend_code":test.default})

    return HttpResponseRedirect("/")

def directMessages(request, direct_room):

    filter_rooms = DirectRooms.objects.filter(default=direct_room).first()
    messages = DirectMessages.objects.filter(room=filter_rooms)
    
    if not filter_rooms:
        new_room = DirectRooms(author=request.user, friend=filter_rooms.friend)
        new_room.save()
        print("niema")
    else:
        print("jest")
    
    chat_content = render_to_string( "chat/users.html", { 
        ##"test": filter_rooms,
        ##"room_name":direct_message,
        "messages":messages,
        },
        request=request)

    return JsonResponse({"chat_content":chat_content})


def room(request, room_name):
    
    filter_rooms = ActiveRooms.objects.filter(name=room_name).first()

    if filter_rooms:
        messages = MessagesRoom.objects.filter(room=filter_rooms.id)
    else:
        messages = []

    chat_content = render_to_string( "chat/test.html", { 
        "room_name":room_name,
        "messages":messages,
        "online_users":filter_rooms,
        },
        request=request)

    return JsonResponse({"chat_content":chat_content})


def user_convert(request):
    user_form = UpdateUserForm(instance=request.user)

    if request.method == "POST":
        user_form_object = user_form.save(commit=False)
        user_form_object.save()
        return HttpResponseRedirect("/")
    else:
        user_form = UpdateUserForm(instance=request.user)

    context = {
        "form":user_form
    }

    return render(request, 'chat/convert.html', context)
