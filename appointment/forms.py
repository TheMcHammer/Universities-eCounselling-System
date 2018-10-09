from django import forms
from .models import Entry
from django.contrib.auth.models import User, Group

class EntryForm(forms.ModelForm):
    date = forms.DateTimeField()
    reason = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    creator = forms.CharField()
    confirmed = forms.BooleanField()

    class Meta:
        model = Entry
        fields = ('reason','date','description','creator','confirmed')

    def __init__(self, *args, **kwargs):
         super(EntryForm, self).__init__(*args, **kwargs)
         self.fields['creator'].queryset = User.objects.filter(groups__name='Student')

