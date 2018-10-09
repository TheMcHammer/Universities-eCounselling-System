from django.conf.urls import url
from chat import views

app_name = 'chat'

urlpatterns = [
    url(r'^$', views.private_rooms, name="private_rooms"),
    url(r'chat_token$', views.chat_token, name="chat_token"),
    url(r'myrooms/(?P<slug>[-\w]+)/$', views.private_room_detail, name="private_room_detail"),
]