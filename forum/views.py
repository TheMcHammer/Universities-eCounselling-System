from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse

from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    ChatGrant
)

from .models import Room

fake = Faker()

def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'forum/index.html', {'rooms': rooms})

def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'forum/public_chat.html', {'room': room})

def token(request):
    identity = request.GET.get('identity', fake.user_name())
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    forum_service_sid = settings.TWILIO_PRIVATE_SERVICE_SID
    sync_service_sid = settings.TWILIO_SYNC_SID

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    if sync_service_sid:
        sync_grant = SyncGrant(service_sid=sync_service_sid)
        token.add_grant(sync_grant)

    if forum_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=forum_service_sid)
        token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'token': token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)

