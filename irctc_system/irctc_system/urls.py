from django.contrib import admin  # Make sure this is added
from django.urls import path
from train_management import views

urlpatterns = [
    path('admin/', admin.site.urls),  # This is the admin URL
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('add_train/', views.add_train, name='add_train'),
    path('check_availability/<str:source>/<str:destination>/', views.check_seat_availability, name='check_availability'),
    path('book_seat/<str:train_number>/', views.book_seat, name='book_seat'),
    path('booking_details/', views.get_booking_details, name='booking_details'),
]
