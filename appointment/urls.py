from django.conf.urls import url
from . import views


app_name = 'appointment'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'detail/connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name="change_friends"),
    url(r'c/$', views.Index_View.as_view(), name='indextwo'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'entry/add/$', views.EntryCreate.as_view(), name='entry-add'),
    url(r'myappointments/$', views.EntryByUserListView.as_view(), name='my-entries'),
    # url(r'^entry/add/', views.add, name='add'),
]