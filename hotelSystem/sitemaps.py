import re
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    def items (self):
        return['reserve', 'reservations', 'customers', 'checkins', 'checkouts', 'login', 'rooms']
    def location(self, items):
        return reverse(items)