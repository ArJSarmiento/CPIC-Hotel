from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.urls import reverse

class User(AbstractUser):
    SEX_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female',),
        ('O', 'Others',),
    )
    sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        default=SEX_CHOICES[0][1]
    )


class Customer(models.Model):
    """Model for customers"""
    customer_id = models.BigAutoField(primary_key=True)  
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(null=True, blank=True)
    
    SEX_CHOICES = (
        ('M', 'Male',),
        ('F', 'Female',),
        ('O', 'Others',),
    )
    sex = models.CharField(
        max_length=20,
        choices=SEX_CHOICES,
        default=SEX_CHOICES[0][1]
    )
    
    STATUS_CHOICES = (
        ('NR', 'Not Reserved'),
        ('R', 'Reserved'),
        ('CI', 'Checked In'),
        ('CO', 'Checked Out')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][1]
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('customer_view', kwargs={'customerID': self.customer_id})
    
    class Meta:
        ordering = ['first_name', 'middle_name', 'last_name']
    def get_absolute_url(self):
        """
        This generates the url for customer detail.
        'customer-detail' is the name of the url.
        Takes argument customer_id
        """
        return reverse('customer-detail', args=str([self.customer_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.customer_id, self.first_name, self.last_name)

class Reservation(models.Model):
    """Models for reservations"""
    reservation_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    no_of_children = models.PositiveSmallIntegerField(default=0)
    no_of_adults = models.PositiveSmallIntegerField(default=1)
    reservation_date_time = models.DateTimeField(default=datetime.datetime.now())
    expected_arrival_date_time = models.DateTimeField(default=datetime.datetime.now())
    expected_departure_date_time = models.DateTimeField(default=datetime.datetime.now())

    def get_absolute_url(self):
        return reverse('reservation-detail', args=str([self.reservation_id]))

    def __str__(self):
        return '({0}) {1} {2}'.format(self.reservation_id, self.customer.first_name, self.customer.last_name)
    
    def save(self, *args, **kwargs):
        if not CheckIn.objects.filter(reservation=self).exists():
            c=self.customer
            c.status = c.STATUS_CHOICES[1][1]
            c.save()
        super().save(*args, **kwargs)

DEFAULT_ROOM_ID = 1
class Room(models.Model):
    room_no = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=256)
    room_type = models.ForeignKey('RoomType', null=False, blank=True, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.SET_NULL)
    facility = models.ManyToManyField('Facility', blank=True)
    ordering = ['room_no', ]

    def __str__(self):
        return "%s - %s - Php. %i" % (self.room_no, self.room_type.name, self.room_type.price)

    def display_facility(self):
        """
        This function should be defined since facility is many-to-many relationship
        It cannot be displayed directly on the admin panel for list_display
        """
        return ', '.join(facility.name for facility in self.facility.all())

    display_facility.short_description = 'Facilities'

    def get_absolute_url(self):
        return "/rooms/%s" % self.room_no

    def save(self, *args, **kwargs):  # Overriding default behavior of save
        self.availability = 0 if self.reservation else 1
        super().save(*args, **kwargs)

class Facility(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveIntegerField(default = 0)

    class Meta:
        verbose_name_plural = 'Facilities'  # Otherwise admin panel shows Facilities

    def __str__(self):
        return f"{self.name}"

class RoomType(models.Model):
    name = models.CharField(max_length=25)
    price = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return f"{self.name}"

class CheckIn(models.Model):
    id = models.CharField(max_length=50, primary_key=True, blank=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    rooms = models.ManyToManyField('Room', blank=True)
    initial_amount = models.PositiveSmallIntegerField(blank=True)
    check_in_date_time = models.DateTimeField(default=datetime.datetime.now())
    last_edited_on = models.DateTimeField(default=datetime.datetime.now())
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%i - %s" % (self.reservation.reservation_id, self.reservation.customer)
   
    def save(self, *args, **kwargs):
        if not CheckOut.objects.filter(check_in=self).exists():
            c = self.reservation.customer
            c.status = c.STATUS_CHOICES[2][1]
            c.save()
            
        self.last_edited_on = datetime.datetime.now()
        super().save(*args, **kwargs)

class CheckOut(models.Model):
    check_in = models.OneToOneField(CheckIn, on_delete=models.CASCADE)
    stay_duration = models.DurationField(null=True)
    total_amount = models.PositiveSmallIntegerField(default=0 )
    pay_amount = models.PositiveSmallIntegerField(default=0)
    check_out_date_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL )

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        c = self.check_in.reservation.customer
        c.status = c.STATUS_CHOICES[3][1]
        c.save()
        super().save(*args, **kwargs)