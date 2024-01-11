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
from django.views.decorators.csrf import csrf_exempt

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
            print(request)
            entered_login = request.POST['username']

            username = entered_login + str(random.randint(0,100000000))
            email = " "
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
            "all_tmp_users" : all_tmp_users
        }
        return render(request, "chat/index.html", context)
    
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
            
                    chat_content = render_to_string( "chat/chat.html", { 
                        "room_name":room_name,
                        "filter_room":filter_rooms,
                        },
                        request=request)

                    return JsonResponse({"status":"new", "chat_content":chat_content, "private":is_private_value })
            

def search(request, search_query):
    friends = CustomUser.objects.get(id=request.user.id).friends.all().values('id')
    filtered_users = CustomUser.objects.filter(username__contains=search_query).exclude(is_superuser=True).exclude(id__in=friends).exclude(id=request.user.id)
    users_list = [ {'users' : user.username, 'user_img':user.user_img.url } for user in filtered_users ]
    return JsonResponse({"users_list":users_list})


def search_channel(request, room_name, user_name=None):
    private_room = ActiveRooms.objects.filter(name=room_name).first()
    list_users_not_in_room = CustomUser.objects.filter(username__contains=user_name).exclude(id__in=private_room.users.all().values_list('id', flat=True)).exclude(is_superuser=True)
    
    users_not_in_room = [ {'users' : user.username, 'user_img':user.user_img.url, "added":True } for user in list_users_not_in_room ]
    users_in_room = [ {'users' : user.username, 'user_img':user.user_img.url, "added":False } for user in private_room.users.all() ]

    combined_list = users_not_in_room + users_in_room ## can use .extend method

    return JsonResponse({"room_users":combined_list})

@csrf_exempt
def add_to_channel(request, room_name, user_name):

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        private_room = ActiveRooms.objects.filter(name=room_name).first()
        choosed_user = CustomUser.objects.filter(username=user_name).first()

        if choosed_user in private_room.users.all():
            private_room.users.remove(choosed_user)
        else:
            private_room.users.add(choosed_user)

        return JsonResponse({"status":"ok"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request type"})




def users(request, user_name):

    typedUser = CustomUser.objects.filter(username=user_name).first()
    currentUser = CustomUser.objects.get(id=request.user.id)

    if typedUser not in currentUser.friends.all():
        currentUser.friends.add(typedUser)
        newDirectRoom = DirectRooms(author=currentUser, friend=typedUser)
        newDirectRoom.save()
        newDirectRoom.users.add(currentUser, typedUser)
    ##dodać statusy userów
        return JsonResponse({"friend_added":typedUser.username,
                             "friend_code":newDirectRoom.default,
                             "friend_avatar": typedUser.user_img.url,
                             "friend_online":typedUser.online,
                             })

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

    chat_content = render_to_string( "chat/chat.html", { 
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
            

def user_convert(request):
    user_form = UpdateUserForm(instance=request.user)

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        print(request.POST)
        if user_form.is_valid():
            user_form_object = user_form.save(commit=False)
            user_form_object.save()
            return HttpResponseRedirect("/")
        else:
            ## return jsoon with errors
            user_form.full_clean()
            errors = user_form.errors.as_json()
            print(errors)
            return JsonResponse({"status":"failed","errors":errors})
    else:
        user_form = UpdateUserForm(instance=request.user)

    context = {
        "form":user_form
    }

    return render(request, 'chat/convert.html', context)

def chat_redirect(request, channel):

#     # filter_room = ActiveRooms.objects.filter(name=channel).first()

#     # if filter_room:
#     #     messages = MessagesRoom.objects.filter(room=filter_room.id)
#     # else:
#     #     messages = []

#     # chat_content = render_to_string( "chat/chat.html", { 
#     #     "room_name":channel,
#     #     "messages":messages,
#     #     "filter_room":filter_room,
#     #     },
#     #     request=request)
    
#     # return JsonResponse({"chat_content":chat_content})
#     ##return JsonResponse({"status":"ok", }) 
    return HttpResponseRedirect("/")