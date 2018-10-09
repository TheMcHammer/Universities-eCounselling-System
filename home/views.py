from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView
from .forms import RegistrationForm, UserProfileForm, EditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from appointment.models import Entry
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = "/home/login/"
    template_name = 'home/index.html'
    context_object_name = 'all_entries'
    model = User


    def get_queryset(self):
        #friend = Friend.objects.get(current_user=request.user)
        #friends = friend.users.all()
        if self.request.user.groups.filter(name='Counsellor'):
            entries = Entry.objects.all()
        else:
            entries = Entry.objects.filter(creator=self.request.user)
        #args = {'friends': friends, 'entries':entries}
        return entries
        #return render(request, self.template_name, args)


def signup_view(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home:edit_profile')
    else:
        form = RegistrationForm()
    return render(request,'home/signup.html',{'form':form})

def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('appointment:index')
    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html',{'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home:signup')

def view_profile(request):
    args = {'user':request.user}
    return render(request, 'home/profile.html', args)


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name =  'home/edit_profile.html'

    def get_initial(self):
        initial = super(EditProfileForm, self).get_initial()
        try:
            current_group = self.object.groups.get()
        except:
            # exception can occur if the edited user has no groups
            # or has more than one group
            pass
        else:
            initial['group'] = current_group.pk
        return initial

    def get_form_class(self):
        return UserProfileForm

    def form_valid(self, form):
        self.object.groups.clear()
        self.object.groups.add(form.cleaned_data['group'])
        return super(EditProfileForm, self).form_valid(form)


def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/home/profile')

    else:
        form = UserProfileForm(instance=request.user)
        args = {'form':form}
        return render(request,'home/edit_profile.html', args)



