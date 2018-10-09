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
from .models import CounselRoom

fake = Faker()

def private_rooms(request):
    myrooms = CounselRoom.objects.all()
    return render(request, 'chat/index.html', {'myrooms': myrooms})

def private_room_detail(request, slug):
    myroom = CounselRoom.objects.get(slug=slug)
    return render(request, 'chat/private_room_detail.html', {'myroom': myroom})

def chat_token(request):
    identity = request.GET.get('identity', fake.user_name())
    device_id = request.GET.get('device', 'default')  # unique device ID

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID
    sync_service_sid = settings.TWILIO_SYNC_SID

    chat_token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Create a unique endpoint ID for the device
    endpoint = "MyDjangoChatRoom:{0}:{1}".format(identity, device_id)

    # Create a Sync grant and add to token
    if sync_service_sid:
        sync_grant = SyncGrant(service_sid=sync_service_sid)
        chat_token.add_grant(sync_grant)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        chat_token.add_grant(chat_grant)

    response = {
        'identity': identity,
        'chat_token': chat_token.to_jwt().decode('utf-8')
    }

    return JsonResponse(response)

