from django import template

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