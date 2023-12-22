from django.shortcuts import render
from django.views import View
import random
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm, UpdateUserForm, CreateNewChannel
from .models import ActiveRooms, CustomUser, MessagesRoom, DirectRooms, DirectMessages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.middleware.csrf import get_token
from asgiref.sync import async_to_sync
from django.db.models import Q

# Create your views here.

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


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

        if request.user.is_authenticated:
            visible_rooms = all_rooms.filter(Q(is_private=False) | Q(author=request.user) | Q(users=request.user)).distinct()
            print(visible_rooms)
        else:
        # Jeśli użytkownik nie jest zalogowany, pokaż tylko publiczne pokoje
            visible_rooms = all_rooms.filter(is_private=False)

        user = CustomUser.objects.get(id=request.user.id)
        new_channel_form = CreateNewChannel()

        all_tmp_users = CustomUser.objects.filter(is_guest=True)
        context = {
            "all_rooms" : visible_rooms,
            "friends_room" : user.direct_users.all(),
            "new_channel_form": new_channel_form,
            #"friends_rooms" : user.friends.all(),
            "all_tmp_users" : all_tmp_users
        }
        return render(request, "chat/chat.html", context)
    
    def post(self, request):

        form = CreateNewChannel(request.POST)

        if "channel_name" in request.POST:
            if form.is_valid():
                
                room_name = request.POST['channel_name']
                
                is_private_value = request.POST.get('is_private', False)
                is_private_value = is_private_value == 'on' 
                
                filter_rooms = ActiveRooms.objects.filter(name=room_name).first()

                if filter_rooms:
                    return JsonResponse({"status":"exist", "message":"already created", "room":filter_rooms.name})
                else:
                    new_room = ActiveRooms(author=request.user ,name=room_name, is_private=is_private_value)
                    new_room.save()
                    new_room.users.add(request.user)
            
                    chat_content = render_to_string( "chat/test.html", { 
                        "room_name":room_name,
                        "filter_room":filter_rooms,
                        },
                        request=request)

                    return JsonResponse({"status":"new", "chat_content":chat_content, "private":is_private_value })
            

def search(request, search_query):

    friends = CustomUser.objects.get(id=request.user.id).friends.all().values('id')
    filtered_users = CustomUser.objects.filter(username__contains=search_query).exclude(is_superuser=True).exclude(id__in=friends).exclude(username=request.user.username)
    users_list = [ {'users' : user.username, 'user_img':user.user_img.url } for user in filtered_users ]
    return JsonResponse({"users_list":users_list})


def users(request, user_name):

    typedUser = CustomUser.objects.filter(username=user_name).first()
    currentUser = CustomUser.objects.get(id=request.user.id)
    print(currentUser)
    print(currentUser.friends.all())
    if typedUser not in currentUser.friends.all():
        currentUser.friends.add(typedUser)
        newDirectRoom = DirectRooms(author=currentUser, friend=typedUser)
        newDirectRoom.save()
        newDirectRoom.users.add(currentUser, typedUser)
    ##dodać statusy userów
        return JsonResponse({"friend_added":typedUser.username,
                             "friend_code":newDirectRoom.default})

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
    
    filter_room = ActiveRooms.objects.filter(name=room_name).first()

    if filter_room:
        messages = MessagesRoom.objects.filter(room=filter_room.id)
    else:
        messages = []

    chat_content = render_to_string( "chat/test.html", { 
        "room_name":room_name,
        "messages":messages,
        "filter_room":filter_room,
        },
        request=request)

    return JsonResponse({"chat_content":chat_content})

# def update_user_status(request, id):
#     pass
    # user_object = CustomUser.objects.get(id=id)
    
    # if request.user == user_object:
    #     if user_object.online:
    #         user_object.online = False
    #         user_object.save()
    #         return JsonResponse({"status":"ok",
    #                              "user_status":user_object.online})
    #     else:
    #         user_object.online = True
    #         user_object.save()
    #         return JsonResponse({"status":"ok",
    #                              "user_status":user_object.online})
            

def add_to_channel(request, room_name, user_name):
    choosed_user = CustomUser.objects.filter(username=user_name).first()
    private_room = ActiveRooms.objects.filter(name=room_name).first()

    private_room.users.add(choosed_user)


    return JsonResponse({"status":"ok"}) 

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
