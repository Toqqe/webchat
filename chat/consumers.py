import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ActiveRooms, MessagesRoom,  CustomUser, DirectMessages, DirectRooms
from channels.db import database_sync_to_async
from django.db.models import F
from datetime import datetime

class ChatCustomer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name_id"]
        self.user = self.scope["user"]

        print("Connect:", self.scope["user"])

        self.room_group_name = "chat_%s" % self.room_name
        #join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.sync_db()


        await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_update',
                'message': "user_connected",
                'user_online': self.user.username,
            })

    async def send_user_update(self, event):

        message = event['message']
        user_online = event['user_online']


        await self.send(text_data=json.dumps({
            "message": message,
            "user_online" : user_online,
        }))

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_update',
                'message': "user_disconnected",
                'user_online': self.user.username,

        })
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.del_sync_db()

        if message['code'] == None:
            message['code'] = 1001
        
        print('disconnected! ', message)
        await super().websocket_disconnect(message)

    async def receive(self, text_data): ##2
        text_data_json = json.loads(text_data)
        print("JSON: ", text_data_json)

        if "close" in text_data_json:
            await self.del_sync_db()

            await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_update',
                'message': "user_disconnected",
                'user_online': self.user.username,
            })
            
            await self.close()
        else:

            message = text_data_json["message"]
            username = text_data_json["username"]
            user_img = self.user.user_img.url

            timestamp = await self.message_save_sync(message=message, user=username)

            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type":"chat_message", ## to jest dlatego, że poniżej mamy chat_message
                    "message": message,
                    "username" : username,
                    "user_online_img": user_img,
                    "message_timestamp": str(timestamp.strftime("%A %H:%M"))
                    
                })
            
    async def chat_message(self,event): ##3
        message = event["message"]
        username = event["username"]
        user_online_img = event["user_online_img"]
        message_timestamp = event["message_timestamp"]


        await self.send(text_data=json.dumps({
            "message":message,
            "username" : username,
            "user_online_img" : user_online_img,
            "message_timestamp" : message_timestamp,
            }))


    @database_sync_to_async
    def sync_db(self):

        db_room = ActiveRooms.objects.filter(name=self.room_name)
        online_users = CustomUser.objects.filter(username=self.user).first()

        if online_users not in db_room.first().users.all():
            db_room.first().users.add(self.user)
    
    @database_sync_to_async
    def del_sync_db(self):

        db_room = ActiveRooms.objects.filter(name=self.room_name)
        db_room.first().users.remove(self.user)


    @database_sync_to_async
    def message_save_sync(self, message, user):
        db_room = ActiveRooms.objects.filter(name=self.room_name).first()
        user = CustomUser.objects.filter(username=user).first()

        db_room_message = MessagesRoom(room=db_room, author=user, context=message)
        db_room_message.save()

        return db_room_message.timestamp

    @database_sync_to_async
    def test(self, room_name):
        active_users = ActiveRooms.objects.filter(name=room_name).first().users.all().count()
        return active_users
        

############################################################################################ Online


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = "general"
        self.room_group_name = "main_chat_%s" % self.room_name
        self.user = self.scope["user"]

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_status',
                'status': await self.get_current_status(self.user),
                'user': self.user.username,
            })

    # async def disconnect(self, close_code):
    #     pass
    #     #await self.change_status()

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_status',
                'status': False,
                'user': self.user.username,
        })
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if message['code'] == None:
            message['code'] = 1001
        
        print('disconnected! ', message)
        await super().websocket_disconnect(message)


    async def receive(self, text_data): ##2
        text_data_json = json.loads(text_data)
        print("JSON, user_status: ", text_data_json)

        new_status = await self.change_status(text_data_json['username'])

        await self.channel_layer.group_send(
            self.room_group_name,{
            'type': 'send_user_status',
            'status': new_status,
            'user': text_data_json['username'],
        })

    async def send_user_status(self, event):

        status = event['status']
        user = event['user']

        await self.send(text_data=json.dumps({
            "status": status,
            "user" : user,
        }))


    @database_sync_to_async
    def change_status(self, user):
        user_object = CustomUser.objects.get(username=user)
        
        if user_object.online:
            user_object.online = False
            user_object.save()
        else:
            user_object.online = True
            user_object.save()

        return user_object.online
    
    @database_sync_to_async
    def get_current_status(self, user):
        user_object = CustomUser.objects.get(username=user)

        return user_object.online

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

    # async def websocket_disconnect(self, message):
    #     await self.channel_layer.group_send(
    #          self.room_group_name,{
    #             'type': 'send_user_update',
    #             'message': "user_disconnected",
    #             'user_online': self.user.username,

    #     })
    #     await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    #     await self.del_sync_db()

    #     if message['code'] == None:
    #         message['code'] = 1001
        
    #     print('disconnected! ', message)
    #     await super().websocket_disconnect(message)




############################################################################################ For direct users

class DirectMessage(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["direct_room_id"]


        self.user = self.scope["user"]

        print("Connect:", self.scope["user"])

        self.room_group_name = "direct_message_%s" % self.room_name
        #join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()



    async def websocket_disconnect(self, message):
        await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_update',
                'message': "user_disconnected",

        })
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        if message['code'] == None:
            message['code'] = 1001
        
        print('disconnected! ', message)
        await super().websocket_disconnect(message)

    async def receive(self, text_data): ##2
        text_data_json = json.loads(text_data)
        print("JSON: ", text_data_json)

        if "close" in text_data_json:
            await self.channel_layer.group_send(
             self.room_group_name,{
                'type': 'send_user_update',
                'message': "user_disconnected",
            })
            
            await self.close()
        else:

            message = text_data_json["message"]
            username = text_data_json["username"]
            user_img = self.user.user_img.url

            timestamp = await self.message_save_sync(message=message, user=username)
            
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    "type":"chat_message", ## to jest dlatego, że poniżej mamy chat_message
                    "message": message,
                    "username" : username,
                    "user_online_img": user_img,
                    "message_timestamp": str(timestamp.strftime("%A %H:%M"))
                })
            
    async def chat_message(self,event): ##3
        message = event["message"]
        username = event["username"]
        user_online_img = event["user_online_img"]
        message_timestamp = event["message_timestamp"]


        await self.send(text_data=json.dumps({
            "message":message,
            "username" : username,
            "user_online_img" : user_online_img,
            "message_timestamp" : message_timestamp,

            }))


    @database_sync_to_async
    def message_save_sync(self, message, user):
        db_room = DirectRooms.objects.filter(default=self.room_name).first()

        user = CustomUser.objects.filter(username=user).first()

        db_room_message = DirectMessages(room=db_room, author=user, context=message)
        db_room_message.save()
        return db_room_message.timestamp