from django.contrib import admin
from .models import Entry, Friend# EntryInstance
from django.contrib.auth.models import User

admin.site.register(Friend)

#admin.site.register(Entry)
#admin.site.register(EntryInstance)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('creator','date', 'description')

#@admin.register(EntryInstance)
#class EntryInstanceAdmin(admin.ModelAdmin):
    #pass
# list_filter = ('status', 'due_back')