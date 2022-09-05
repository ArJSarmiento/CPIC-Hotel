import re
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Room

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    def items (self):
        return['reserve', 'reservations', 'customers', 'checkins', 'checkouts', 'login', 'rooms']
    def location(self, items):
        return reverse(items)
    
class RoomViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
 
    def items (self):
        return Room.objects.all().order_by("-room_no")