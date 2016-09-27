from django.contrib import admin

from .models import Person, PhoneNumber, Address, Location, Note, Canvass, Event, EventPerson


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'main_phone', 'age')


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'phone_type', 'people')


class EventPersonInline(admin.TabularInline):
    model = EventPerson


class EventAdmin(admin.ModelAdmin):
    inlines = [ EventPersonInline, ]

admin.site.register(Person, PersonAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Canvass)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Note)