from django import template
from hotelSystem.models import CheckIn, CheckOut
from django.utils import timezone
from datetime import datetime
from math import ceil
register = template.Library()

@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours =  (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    return (
        str(days)
        + f" day{'s'[:days^1]}, "
        + str(hours)
        + f" hour{'s'[:hours^1]}, "
        + str(minutes)
        + f" minute{'s'[:minutes^1]}"
    )

@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

@register.filter
def balance(check_in):
    my_checkin = CheckIn.objects.get(id=check_in)
    if CheckOut.objects.filter(check_in__id = my_checkin.id).exists():
        return "Fully Paid"
    
    my_stay_duration = datetime.now().astimezone() - my_checkin.check_in_date_time
    calculated_duration = timezone.timedelta(days=ceil(my_stay_duration.total_seconds() / 3600 / 24))
    my_total_amount = calculated_duration.days * my_checkin.initial_amount
    return str(my_total_amount-my_checkin.initial_amount)