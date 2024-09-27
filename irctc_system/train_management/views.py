from .models import Train
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

def home(request):
    return HttpResponse("Welcome to the IRCTC Railway Management System API.")
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User created successfully'}, status=201)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def add_train(request):
    # Check for API key in the headers
    api_key = request.headers.get('API-Key')
    if api_key != settings.ADMIN_API_KEY:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        train_number = data['train_number']
        source = data['source']
        destination = data['destination']
        total_seats = data['total_seats']
        available_seats = total_seats
        train = Train.objects.create(
            train_number=train_number,
            source=source,
            destination=destination,
            total_seats=total_seats,
            available_seats=available_seats
        )
        return JsonResponse({'message': 'Train added successfully'}, status=201)

def check_seat_availability(request, source, destination):
    trains = Train.objects.filter(source=source, destination=destination)
    data = [{"train_number": train.train_number, "available_seats": train.available_seats} for train in trains]
    return JsonResponse(data, safe=False)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_seat(request, train_number):
    try:
        train = Train.objects.select_for_update().get(train_number=train_number)
        if train.available_seats > 0:
            booking = Booking.objects.create(user=request.user, train=train, seat_number=train.total_seats - train.available_seats + 1)
            train.available_seats = F('available_seats') - 1
            train.save()
            return JsonResponse({'message': 'Seat booked successfully'}, status=200)
        return JsonResponse({'error': 'No seats available'}, status=400)
    except Train.DoesNotExist:
        return JsonResponse({'error': 'Train not found'}, status=404)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_booking_details(request):
    bookings = Booking.objects.filter(user=request.user)
    data = [{"train_number": booking.train.train_number, "seat_number": booking.seat_number} for booking in bookings]
    return JsonResponse(data, safe=False)
