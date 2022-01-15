from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path("offline", views.offline, name="offline"),
    path("reserve", views.reserve, name="reserve"),
    path("reservations", views.reservations, name="reservations"),
    path("reservations/<int:reservationID>", views.reservations_view, name="reservations_view"),
    path("customers", views.customers, name="customers"),
    path("customers/<int:customerID>", views.customer_view, name="customer_view"),
    path("checkin", views.checkin, name="checkin"),
    path("checkins", views.checkins, name="checkins"),
    path("checkins/<checkinID>", views.checkin_view, name="checkin_view"),
    path("checkout",views.checkout, name="checkout"),
    path("checkouts", views.checkouts, name="checkouts"),
    path("checkouts/<checkoutID>", views.checkout_view, name="checkout_view"),
    path("rooms", views.roomList, name="rooms"),
    path("roomsVacant", views.roomListVacant, name="roomsVacant"),
    path("rooms/<int:roomID>", views.room_view, name="room_view"),
    path("payments", views.payments, name="payments"),
    path("profile", views.profile, name="profile"),
    path("staff", views.staff, name="staff"),
    path("change_password", views.change_password, name="change_password"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
