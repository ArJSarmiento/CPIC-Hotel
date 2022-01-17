from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template import RequestContext
from django.utils import timezone
from .forms import ReservationForm
from .models import CheckOut, CheckIn, Room, Reservation, Customer, User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from math import ceil

@login_required(login_url='login')
def index(request):
    page_title = ("Hotel Management System")  # For page title as well as heading
    total_num_rooms = Room.objects.all().count()
    available_num_rooms = Room.objects.exclude(reservation__isnull=False).count()
    total_num_reservations = Reservation.objects.all().count()
    total_num_staffs = User.objects.filter(groups__name='Staff').count()
    total_num_customers = Customer.objects.all().count()
    total_check_in = CheckIn.objects.all().count()
    
    try:
        customer =  Customer.objects.get(user__id = request.user.id)
        my_reservation = Reservation.objects.filter(customer__customer_id=customer.customer_id).latest('reservation_date_time')
    except Customer.DoesNotExist:
        customer = None
        my_reservation = None
    
    my_room = None
    my_checkin = None
    if my_reservation != None and customer != None:
        try:
            my_room = Room.objects.get(reservation__reservation_id=my_reservation.reservation_id)
        except Room.DoesNotExist :
            my_room = None
        
        try:
            my_checkin = CheckIn.objects.filter(reservation__customer__customer_id=customer.customer_id).latest('reservation__reservation_date_time')
        except CheckIn.DoesNotExist:
            my_checkin =None
    
    if total_num_reservations == 0:
        last_reserved_by = Reservation.objects.none()
    else:
        last_reserved_by = Reservation.objects.get_queryset().latest('reservation_date_time')

    data = {
        'title': page_title,
        'total_num_rooms': total_num_rooms,
        'available_num_rooms': available_num_rooms,
        'total_num_reservations': total_num_reservations,
        'total_num_staffs': total_num_staffs,
        'total_num_customers': total_num_customers,
        'last_reserved_by': last_reserved_by,
        'total_check_in': total_check_in,
        'my_reservation': my_reservation,
        'my_room': my_room,
        'my_checkin': my_checkin
    }

    return render(request, "hotelSystem/index.html", data)

def empty(request, title, message):
    data = {
        'title': title,
        'message': message
    }
    return render(request, "hotelSystem/empty.html", data)

def offline(request):
    return render(request, "hotelSystem/offline.html")

@login_required(login_url='login')
def reserve(request):
    if not request.user.groups.filter(name='Staff').exists():
        return HttpResponseRedirect(reverse("index"))
    
    title = "Add Reservation"
    isSuccess = True
    reservation = Reservation.objects.none()
    reservation_form = ReservationForm()
    error = ""

    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            _username = reservation_form.cleaned_data.get('user_name')
            _email = reservation_form.cleaned_data.get('email')
            _first_name = reservation_form.cleaned_data.get('first_name')
            _middle_name = reservation_form.cleaned_data.get('middle_name')
            _last_name = reservation_form.cleaned_data.get('last_name')
            _sex=reservation_form.cleaned_data.get('sex')
            _contact_no=reservation_form.cleaned_data.get('contact_no')
            _address=reservation_form.cleaned_data.get('address')
            _no_of_children=reservation_form.cleaned_data.get('no_of_children')
            _no_of_adults=reservation_form.cleaned_data.get('no_of_adults')

            error="Number of guests should'nt be negative."
            if _no_of_children>=0 or _no_of_adults>=0: 
                error=""
                _user = User.objects.filter(username=_username).first()
                if _user is None:
                    _password = "password_1234"
                    _user = User.objects.create_user(_username, _email, _password)
                    _user.first_name = _first_name
                    _user.last_name = _last_name
                    _user.sex = _sex
                    _user.save() 
                
                if  _first_name != _user.first_name and _last_name != _user.last_name:
                    errorUserName = "Username is already taken."
                    return render(
                        request,
                        'hotelSystem/reserve.html', {
                            'title': title,
                            'reservation_form': reservation_form,
                            'isSuccess': isSuccess,
                            'error': errorUserName,
                        }
                    )
        
                try:
                    customer = Customer.objects.get(user__id=_user.id)
                except Customer.DoesNotExist:
                    customer = Customer(
                        first_name=_first_name,
                        middle_name=_middle_name,
                        last_name=_last_name,
                        email_address=_email,
                        contact_no=_contact_no,
                        address=_address,
                        sex=_sex,
                        user = _user,
                    )
                    customer.save() 


                reservation = Reservation(
                    staff=request.user,
                    customer=customer,
                    no_of_children=reservation_form.cleaned_data.get('no_of_children'),
                    no_of_adults=reservation_form.cleaned_data.get('no_of_adults'),
                    expected_arrival_date_time=reservation_form.cleaned_data.get('expected_arrival_date_time'),
                    expected_departure_date_time=reservation_form.cleaned_data.get('expected_departure_date_time'),
                    reservation_date_time=timezone.now(),
                )
                reservation.save()

                for room in reservation_form.cleaned_data.get('rooms'):
                    room.reservation = reservation
                    room.save()

                return render(
                    request,
                    'hotelSystem/reserve_success.html', {
                        'reservation': reservation,
                        'isSuccess': isSuccess,
                    }
                )

    if Room.objects.filter(reservation__isnull=True).count() == 0:
        return render(
            request,
            'hotelSystem/reserve_success.html', {
                'reservation': reservation,
                'isSuccess': False
            }
        )

    return render(
        request,
        'hotelSystem/reserve.html', {
            'title': title,
            'reservation_form': reservation_form,
            'isSuccess': isSuccess,
            'error': error
        }
    )

@login_required(login_url='login')
def customers(request):
    if not request.user.groups.filter(name='Staff').exists():
        return HttpResponseRedirect(reverse("index"))
    
    page_title = "Guests"  # For page title as well as heading
    reservations = Customer.objects.filter(status = 'Reserved')
    no_reservations = Customer.objects.filter(status = 'Not Reserved')
    checked_in = Customer.objects.filter(status = 'Checked In')
    checked_out = Customer.objects.filter(status = 'Checked Out')
    
    if reservations.count() == 0 and no_reservations.count() == 0 and checked_in.count() == 0 and checked_out.count() == 0:
        return empty(request, "No guests found.", "There are no customers to display.")
    
    data = {
        'title': page_title,
        'no_reservations': no_reservations,
        'reservations': reservations,
        'checked_in': checked_in,
        'checked_out': checked_out
    }
    return render(request, "hotelSystem/customers.html", data)

@login_required(login_url='login')
def customer_view(request, customerID):
    customer =  Customer.objects.get(customer_id = customerID)
    
    if not request.user.groups.filter(name='Staff').exists() and customer.user.id!=request.user.id:
        return HttpResponseRedirect(reverse("index")) 
    
    room= Room.objects.filter(reservation__customer = customer)
    page_title = str(customer.first_name)+" "+str(customer.last_name)
    data = {
        'title': page_title,
        'customer': customer,
        'reservation': reservations,
        'room': room
    }
    return render(request, "hotelSystem/customer_view.html", data)

@login_required(login_url='login')
def reservations(request):
    if request.user.groups.filter(name='Staff').exists():
        r= Reservation.objects.all().order_by('-reservation_date_time')
    else:
        try:
            customer =  Customer.objects.get(user__id = request.user.id)
        except Customer.DoesNotExist:
            return empty(request, 'No reservations found.', "There are no reservations to display.") 
        r = Reservation.objects.filter(customer__customer_id=customer.customer_id).order_by('-reservation_date_time')
    
    if r.count() == 0:
        return empty(request, 'No reservations found.', "There are no reservations to display.")

    page_title = "Reservations"  # For page title as well as heading

    rooms =  Room.objects.exclude(reservation__isnull=True)
    rinRooms = [x.reservation for x in rooms]
    checkIns = CheckIn.objects.all()
    checkInR = [x.reservation for x in checkIns]

    data = {
        'title': page_title,
        'reservations': r,
        'rooms': rooms,
        'rinRooms':rinRooms,
        'checkIns':checkIns,
        'checkInR':checkInR 
    }
    return render(request, "hotelSystem/reservations.html", data)

@login_required(login_url='login')
def reservations_view(request, reservationID):
    r= Reservation.objects.get(reservation_id = reservationID)
    
    if not request.user.groups.filter(name='Staff').exists() and r.customer.user.id != request.user.id:
        return HttpResponseRedirect(reverse("index")) 
    
    page_title = "Reservation No. " + str(r.reservation_id)+ " Details"  
    room = Room.objects.filter(reservation__reservation_id=reservationID)
    try:
        checkin = CheckIn.objects.get(reservation__reservation_id=reservationID)
    except CheckIn.DoesNotExist:
        checkin = None
    data = {
        'title': page_title,
        'r': r,
        'rooms': room,
        'checkin': checkin
    }
    return render(request, "hotelSystem/reservation_view.html", data)

@login_required(login_url='login')
def checkin(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('reservations'))
    
    reservationID = str(request.POST.get("reservation_id"))
    my_reservation = Reservation.objects.get(reservation_id = reservationID)
    my_rooms = Room.objects.filter(reservation__reservation_id = reservationID)
    facilities = [y for x in my_rooms for y in x.facility.all()]
    room_types_price = sum(x.room_type.price for x in my_rooms)
    price = sum(f.price for f in facilities) + room_types_price
    newcheckIn = CheckIn(
        id="checkin_" + str(my_reservation.reservation_id),
        reservation = my_reservation,
        initial_amount = price,
        check_in_date_time= datetime.now(),
        last_edited_on= datetime.now(),
        user=request.user
    )
    newcheckIn.save()
    newcheckIn.rooms.set(my_rooms)
    newID = '/checkins/' + str(newcheckIn.id)
    return redirect(newID)

@login_required(login_url='login')
def checkins(request):
    if request.user.groups.filter(name='Staff').exists():
        checkIns = CheckIn.objects.all().order_by('-check_in_date_time')
    else:
        try:
            customer =  Customer.objects.get(user__id = request.user.id)
        except Customer.DoesNotExist:
            return empty(request, 'No check-ins found.', "There are no check-ins to display.")
            
        checkIns = CheckIn.objects.filter(reservation__customer__customer_id= customer.customer_id).order_by('-check_in_date_time')
    
    if checkIns.count() == 0:
        return empty(request, 'No check-ins found.', "There are no check-ins to display.")
    
    page_title = "Check-in List"  # For page title as well as heading
    checkouts = CheckOut.objects.all()
    checkIncheckout = [x.check_in for x in checkouts ]
    
    data = {
        'title': page_title,
        'checkIns': checkIns,
        'checkouts':checkouts,
        'checkIncheckout':checkIncheckout
    }
    return render(request, "hotelSystem/checkinList.html", data)

@login_required(login_url='login')
def checkin_view(request,checkinID):
    my_checkin = CheckIn.objects.get(id = checkinID)
    if not request.user.groups.filter(name='Staff').exists() and my_checkin.reservation.customer.user.id != request.user.id:
            return HttpResponseRedirect(reverse("index")) 
        
    title =  "Check-in No. " + str(my_checkin.id)
    try:
        checkout=CheckOut.objects.get(check_in__id = checkinID)
    except CheckOut.DoesNotExist:
        checkout = None
    data = {
        'title': title,
        'my_checkin': my_checkin,
        "checkout":checkout
    }
    return render(request, "hotelSystem/checkin_view.html", data)
    
@login_required(login_url='login')
def checkout(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("checkins"))
    
    checkinID = str(request.POST.get("checkin_id"))
    my_checkin = CheckIn.objects.get(id=checkinID)
    my_stay_duration = datetime.now().astimezone() - my_checkin.check_in_date_time
    calculated_duration = timezone.timedelta(days=ceil(my_stay_duration.total_seconds() / 3600 / 24))
    my_total_amount = calculated_duration.days * my_checkin.initial_amount
    for r in my_checkin.rooms.all():
        r.reservation = None
        r.save()

    newcheckout = CheckOut(
        check_in = my_checkin,
        stay_duration = my_stay_duration,
        total_amount = my_total_amount,
        pay_amount = my_total_amount-my_checkin.initial_amount,
        check_out_date_time= datetime.now(),
        user=request.user
    )
    newcheckout.save()
    newID = '/checkouts/' + str(newcheckout.id)
    return redirect(newID)

@login_required(login_url='login')
def checkouts(request):
    if request.user.groups.filter(name='Staff').exists():
        my_checkouts = CheckOut.objects.all().order_by('-check_out_date_time')
    else:
        try:
            customer =  Customer.objects.get(user__id = request.user.id)
        except Customer.DoesNotExist:
            return empty(request, 'No Checkouts found.', "There are no checkouts to display.")
        my_checkouts = CheckOut.objects.filter(check_in__reservation__customer__customer_id=customer.customer_id).order_by('-check_out_date_time')
        
    if my_checkouts.count() == 0:
        return empty(request, 'No Checkouts found.', "There are no checkouts to display.")
    
    title = "Checkout List"  # For page title as well as heading
   
    data = {
        'title': title,
        'checkOuts': my_checkouts
    }
    return render(request, "hotelSystem/checkoutList.html", data)

@login_required(login_url='login')
def checkout_view(request,checkoutID):
    my_checkout = CheckOut.objects.get(id = checkoutID)
    if not request.user.groups.filter(name='Staff').exists() and my_checkout.check_in.reservation.customer.user.id != request.user.id:
            return HttpResponseRedirect(reverse("index")) 
        
    title = "Checkout No. " + str(my_checkout.id)
    data = {
        'title': title,
        'my_checkout': my_checkout
    }
    return render(request, "hotelSystem/checkout_view.html", data)

@login_required(login_url='login')
def roomList(request):
    rooms =  Room.objects.all()
    if rooms.count() == 0:
        return empty(request, 'No rooms found.', "There are no rooms to display.")
    
    title = "Room List"
    
    data = {
        'title': title, 
        'rooms': rooms
    }
    return render(request, "hotelSystem/roomList.html", data)

@login_required(login_url='login')
def roomListVacant(request):
    rooms =  Room.objects.filter(availability = True)
    if rooms.count() == 0:
        return empty(request, 'No rooms found.', "There are no rooms to display.")
    
    title = "Vacant Rooms List"
    
    data = {
        'title': title, 
        'rooms': rooms
    }
    return render(request, "hotelSystem/roomList.html", data)

@login_required(login_url='login')
def room_view(request, roomID):
    title = "Room No. " + str(roomID) + " Details"
    room =  Room.objects.get(room_no = roomID)
    data = {
        'title': title, 
        'room': room
    }
    return render(request, "hotelSystem/roomView.html", data)

@login_required(login_url='login')
def payments(request):
    if not request.user.groups.filter(name='Staff').exists():
        return HttpResponseRedirect(reverse("index")) 
    title = "Payment Dashboard"
    num_of_reservations = Reservation.objects.all().count()
    num_of_check_ins = CheckIn.objects.all().count()
    num_of_check_outs = CheckOut.objects.all().count()
    vacant_rooms = Room.objects.filter(reservation__isnull=True).count()
    total_income = sum(
        CheckOut.objects.all().values_list('total_amount', flat=True)
    )

    last_checked_in = CheckIn.objects.none()
    if num_of_check_ins > 0:
        last_checked_in = CheckIn.objects.get_queryset().latest('check_in_date_time')
    data = {
        'title': title, 
        'num_of_reservations': num_of_reservations,
        'num_of_check_ins': num_of_check_ins,
        'last_checked_in': last_checked_in,
        'num_of_check_outs': num_of_check_outs,
        'vacant_rooms': vacant_rooms,
        'total_income': total_income
    }
    return render(request, "hotelSystem/payment.html", data)

@login_required(login_url='login')
def profile(request):
    user = request.user
    customer = Customer.objects.filter(user__id=user.id).first()
    data = {
        'user': user,
        'customer': customer
    }
    return render(request, "hotelSystem/my_profile.html", data)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'hotelSystem/change_password.html', {
        'form': form,
        "title": "Change Password"
    })
    
@login_required(login_url='login')
def staff(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == 'POST':
        newStaffIds = request.POST.getlist('isStaff')
        newStaff = User.objects.filter(id__in=newStaffIds)
        oldStaff =User.objects.filter(groups__name='Staff')    
        for x in oldStaff:
            if x not in newStaff:
                x.groups.remove(Group.objects.get(name='Staff'))
        for user in newStaff:
            if user not in oldStaff:
                user.groups.add(Group.objects.get(name='Staff'))
            
    users = User.objects.order_by('first_name')
    data = {
        'users': users,
        'title': 'Edit Staffs'
    }
    return render(request, "hotelSystem/staff.html", data)

@login_required(login_url='login')  
def handler400(request, exception):
    context = {'message': "Bad Request",
                'error' : "400"  
            }
    response = render(request, "hotelSystem/error.html", context=context)
    response.status_code = 400
    return response

@login_required(login_url='login')   
def handler403(request, exception):
    context = {'message': "You are not authorized to view this page",
                'error' : "403"  
            }
    response = render(request, "hotelSystem/error.html", context=context)
    response.status_code = 403
    return response    

@login_required(login_url='login')
def handler404(request, exception):
    context = {'message': "Page not found",
                'error' : "404"  
            }
    response = render(request, "hotelSystem/error.html", context=context)
    response.status_code = 404
    return response

@login_required(login_url='login')
def handler500(request):
    context = {'message': "Internal Server Error",
                'error' : "500"  
            }
    response = render(request, "hotelSystem/error.html", context=context)
    response.status_code = 500
    return response

@cache_control(no_cache=True, must_revalidate=True)
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    if request.method != "POST":
        return render(request, "hotelSystem/login.html")

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

        # Check if authentication successful
    if user is None:
        return render(request, "hotelSystem/login.html", {
            "message": "Invalid username and/or password."
        })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

@cache_control(no_cache=True, must_revalidate=True)
def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method != "POST":
        return render(request, "hotelSystem/login.html")
    username = request.POST["username"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    sex= request.POST["sex"]
    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
    if password != confirmation:
        return render(request, "hotelSystem/login.html", {
            "message": "Passwords must match."
        })

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.sex = sex
        user.save()
    except IntegrityError:
        return render(request, "hotelSystem/login.html", {
            "message": "Username already taken."
        })
    login(request, user)
    return HttpResponseRedirect(reverse("index"))