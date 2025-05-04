from django.shortcuts import render
from .models import Car
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def home_view(request):
 return render(request, 'carss/home.html')
    
# Create your views here.
def browse_cars(request):
    cars = Car.objects.all()
    return render(request, 'carss/browse_cars.html', {'cars': cars})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Login view accessed")
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('browse_cars')  # Redirect to a page after login
        else:
            print("Invalid credentials")
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login page on failure

    return render(request, 'carss/login.html')  # Render the login page

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')  # matches name="password"
        password2 = request.POST.get('password_confirmation')  # matches name="password_confirmation"

        if not username or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('browse_cars')  # or any other page after registration

    return render(request, 'carss/signup.html')
             
             
        
        
          
@login_required
def profile_view(request):
    return render(request, 'carss/profile.html')
            
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login after logout
@login_required
def list_car_view(request):
    if request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = request.POST.get('year')
        price_per_day = request.POST.get('price_per_day')
        location = request.POST.get('location')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if make and model and year and price_per_day and location:
            Car.objects.create(
                make=make,
                model=model,
                year=year,
                price_per_day=price_per_day,
                location=location,
                description=description,
                image=image,
                owner=request.user  # Optional: if your model supports owner
            )
            messages.success(request, "Your car has been listed successfully!")
            return redirect('browse_cars')  # Redirect to list of cars
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'carss/listur.html')
