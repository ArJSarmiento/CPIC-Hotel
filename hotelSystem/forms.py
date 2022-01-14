from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Customer, User, Room
import datetime
from .widgets import MySplitDateTime, FilteredSelectMultiple

class ReservationForm(forms.Form):
    """
    This is the  form for reservation.
    """
    error_messages = {
        'date_time_error': 'Departure time earlier than Arrival time',
    }
    
    user_name = forms.CharField(
        label=_("Username"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter username'),
            }
        )
    )

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter first name'),
            }
        )
    )
    middle_name = forms.CharField(
        label=_('Middle Name'),
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter middle name'),
            }
        )
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter last name'),
            }
        )
    )
    contact_no = forms.CharField(
        label=_('Contact No'),
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter contact number'),
            }
        )
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=50,
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter email'),
            }
        )
    )
    address = forms.CharField(
        label=_("Address"),
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter address'),
            }
        )
    )
    no_of_children = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'id': 'reserveField',
                'placeholder': _('Enter number of children'),
                 'min': 0,
            }
        )
    )
    no_of_adults = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter number of adults'),
                'id': 'reserveField',
                'min': 0,
            }
        )
    )
    
    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.filter(reservation__isnull=True),
        widget=FilteredSelectMultiple(
            is_stacked=True,
            verbose_name="Rooms",
            attrs={
                'class': 'form-control',
                'data-role': 'none',
                'data-native-menu': 'false',
            },
        ),
    )
    
    GENDERS=Customer.SEX_CHOICES
    
    sex = forms.ChoiceField(
        choices = GENDERS, 
        label="", 
        widget=forms.Select(
            attrs={
            'class': 'form-control',
            'placeholder': "Gender",
            'id': 'gender-field',
            }
        )
    )
    

    expected_arrival_date_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'placeholder': 'Arrival Date Time',
            'id': 'reserveField',
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    expected_departure_date_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'placeholder': 'Departure Date Time',
            'id': 'reserveField',
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )