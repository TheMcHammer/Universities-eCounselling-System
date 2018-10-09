from django.http import Http404
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models import Entry
from .forms import EntryForm#, DetailForm

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Entry
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from home.models import UserProfile
from django.contrib.auth.models import User
from .models import Friend

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = "/home/login/"
    template_name = 'appointment/index.html'
    context_object_name = 'all_entries'
    model = User

    def get_queryset(self):
        if self.request.user.groups.filter(name='Counsellor'):
            entries = Entry.objects.all()
        else:
            entries = Entry.objects.filter(creator=self.request.user)
        return entries

def change_friends(request, operation, pk):
    new_friend = User.object.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.loose_friend(request.user, new_friend)
    return redirect('/appointment')


class Index_View(LoginRequiredMixin, generic.ListView):
    login_url = "/home/login/"
    template_name = 'appointment/indextwo.html'
    context_object_name = 'all_entries'
    model = User

    def get_queryset(self):
        return Entry.objects.all()


class EntryByUserListView(LoginRequiredMixin, generic.ListView):
    login_url = "/home/login/"
    model = Entry
    context_object_name = 'entry_list'
    template_name = 'appointment/entry_list_creator_user.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Counsellor'):
            return Entry.objects.filter(creator=self.request.user)

class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/home/login/"
    model = Entry
    #context_object_name = "all_entries"
    template_name = 'appointment/detail.html'

#class ConfirmView(LoginRequiredMixin, generic.TemplateView):
#    login_url = "/home/login/"
    #context_object_name = "all_entries"
#    template_name = 'appointment/detail.html'

#    def get(self, request, pk):
        #form = EntryForm()
        #return render(request, self.template_name, {'form':form})

 #   def post(self, request, pk):
  #      form = EntryForm(request.POST)
  #      if form.is_valid():
   #         form.instance.creator = self.request.user
   #         form.save()
   #         confirm = form.cleaned_data['confirmed']
   #         user = form.cleaned_data['creator']
   #         form = EntryForm()
   #         return redirect('appointment/')
    #    args = {'form':form, 'confirm':confirm, 'pk':pk}
    #    return render(request, self.template_name, args)

class EntryCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = "/home/login/"
    model = Entry
    fields = [ 'reason', 'date', 'description']
    success_message = 'Appointment created succesfully'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


def entry_change_status(request):
    confirmed = request.GET.get('active', False)
    entry_id = request.GET.get('job_id', False)
    # first you get your Entry   model
    entry = Entry.objects.get(pk=entry_id)
    try:
        entry.confirmed = confirmed
        entry.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})
    return JsonResponse(data)

#
   # def post(self, request):
    #    form = EntryForm(request.POST)
     #   if form.is_valid():
     #       accept = form.cleaned_data('confirmed')
     #   args = {'form':form, 'accept':accept}
      #  return render(request, self.template_name, args)








#def index(request):
 #   entries = Entry.objects.all()
  #  return render(request, 'appointment/index.html',{'entries':entries})

#def detail(request, entry_id):
   # try:
      #  entry = Entry.objects.get(pk=entry_id)
  #  except Entry.DoesNotExist:
     #   raise Http404("Entry does not exist")
   # return render(request, 'appointment/detail.html',{'entry':entry})

#def add(request):

 #   if request.method == 'POST':
  #      form = EntryForm(request.POST)
#
 #       if form.is_valid():
  #          name = form.cleaned_data['name']
   #         date = form.cleaned_data['date']
    #        description = form.cleaned_data['description']
#
 #           Entry.object.create(
  #              name=name,
   #             date=date,
    #            descriiption=description,
     #       ).save()
#
 ##           return HttpResponseRedirect('/')
   # else:
    #    form = EntryForm()
#
 #   return render(request, 'appointment/form.html', {'form':form})
