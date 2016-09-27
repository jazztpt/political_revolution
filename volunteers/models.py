import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_extensions.db.models import TimeStampedModel

from tagging.registry import register


class PhoneNumber(TimeStampedModel):
    HOME = 'H'
    CELL = 'C'
    WORK = 'W'
    MAIN = 'M'
    PHONE_TYPE_CHOICES = ( (HOME, 'home'), (CELL, 'cell'),
        (WORK, 'work'), (MAIN, 'main'), )

    phone_type = models.CharField(max_length=1, choices=PHONE_TYPE_CHOICES, default=CELL) 
    number = models.CharField(max_length=32, blank=False)
    is_main = models.BooleanField(default=True)

    # def save(self):
        # on save, change all other phones for this person to not main.

    def people(self):
        if self.person_set.count() == 0:
            return ''
        elif self.person_set.count() == 1:
            return self.person_set.all()[0]
        elif self.person_set.count() == 2:
            return "{} and {}".format(self.person_set.all()[0], self.person_set.all()[1])
        else:
            return "{}, {},...".format(self.person_set.all()[0], self.person_set.all()[1])

    def __str__(self):
        return "{} ({})".format(self.number, self.phone_type)


# @receiver(post_save, sender=PhoneNumber, dispatch_uid="enforce_one_main")
# def enforce_one_main(sender, instance, **kwargs):
#      for person in instance.person_set.all():
#         # if person.id is not None:
#         for phone_number in person.phones.all():
#             if phone_number.number is not self.number:
#                 phone_number.is_main = False


class Person(TimeStampedModel):
    FEMALE = "F"
    MALE = "M"
    OTHER = "O"
    GENDER_CHOICES = ( (FEMALE, "female"), (MALE, "male"), (OTHER, "other") )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    first_name = models.CharField(max_length=100, blank=True)
    # nick_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True)
    phones = models.ManyToManyField(PhoneNumber, blank=True)
    party = models.CharField(max_length=100, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    volunteer = models.BooleanField(default=True)
    contact_after = models.DateTimeField(null=True, blank=True)
    contact_before = models.DateTimeField(null=True, blank=True) # someday, send email when this gets close

    def age(self):
        # return self.birthdate ? date.today().year - self.birthdate.year : ''
        if self.birthdate:
            return datetime.date.today().year - self.birthdate.year
        else:
            return ''

    def main_phone(self):
        # TODO: make it unique
        if self.phones.filter(is_main=True).count() > 0:
            return self.phones.filter(is_main=True)[0]
        else:
            return ''

    def __unicode__(self):
        return "{} {}".format(self.first_name, self.last_name)

register(Person)


class Location(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True)
    contact = models.ManyToManyField(Person)
    phones = models.ManyToManyField(PhoneNumber, blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    HOME = 'H'
    WORK = 'W'
    ADDRESS_TYPE_CHOICES = ( (HOME, 'home'), (WORK, 'work'))

    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPE_CHOICES, default=HOME)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    person = models.ManyToManyField(Person)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)


class Note(TimeStampedModel):
    creator = models.ForeignKey(User)
    text = models.CharField(max_length=500)
    private = models.BooleanField(default=False)
    # person = models.ForeignKey(Person, blank=True, null=True) # maybe just attached to canvass?


class Canvass(TimeStampedModel): 
    PHONE = 'P'
    EMAIL = 'E'
    EVENT = 'V'
    HOME = 'H'
    HOW_CANVASSED_CHOICES = (
        (PHONE, 'phone'), (EMAIL, 'email'), (EVENT, 'event'), (HOME, 'home')
    )

    canvasser = models.ForeignKey(Person, related_name='volunteer_canvassing')
    person_canvassed = models.ForeignKey(Person, related_name='person_reached')
    how_canvassed = models.CharField(max_length=1, 
                        choices=HOW_CANVASSED_CHOICES, 
                        default=PHONE)
    date_canvassed = models.DateTimeField(default=datetime.datetime.now())
    note = models.ForeignKey(Note, blank=True, null=True)


# TODO: replace this with django-schedule or django-scheduler
class Event(TimeStampedModel): 
    # owners will get the emails about the event
    owners = models.ManyToManyField(Person)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    location = models.ForeignKey(Location, null=True, blank=True)
    start_datetime = models.DateTimeField()
    # day_of_week
    # start_date
    # end_date

    def __str__(self):
        return self.title
    

class EventPerson(TimeStampedModel):
    INVITED = 'I'
    TENTATIVE = 'T'
    SCHEDULED = 'S'
    CONFIRMED = 'C'
    DECLINED = 'D'
    ATTENDED = 'A'
    HOST = 'H'         # anyone who helps host the event
    ATTENDEE = 'A'
    STATUS_CHOICES = (
        (INVITED, "invited"), (TENTATIVE, "tentative"), (SCHEDULED, "scheduled"),
        (CONFIRMED, "confirmed"), (DECLINED, 'declined'), (ATTENDED, "attended")
    )
    TYPE_CHOICES = ((HOST, "host"), (ATTENDEE, "attendee"))

    event = models.ForeignKey(Event)
    person = models.ForeignKey(Person)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INVITED)
    attendee_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=ATTENDEE)




# TODO: for location phone numbers, have intermediate field link to user?