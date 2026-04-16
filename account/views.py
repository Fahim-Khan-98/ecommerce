from django.http import HttpResponse
from account.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile



@login_required
def profile_update(request):
    # Safe for old + new users
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # ✅ Show message ONLY when profile is newly created
    if created:
        messages.info(request, "Profile created! Please complete your details.")

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('store:index')

    return render(request, 'profile.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You are authenticated")
    else:
        form = RegistrationForm()
        if request.method =='post' or request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account:login')

        
        context={
            'form' : form
        }
    return render(request,'register.html',context)



def CustomerLogin(request):
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist!")
            return redirect('account:login')

        # Authenticate user
        customer = authenticate(request, username=username, password=password)

        if customer is not None:
            login(request, customer)
            return redirect('store:index')
        else:
            messages.error(request, "Password is incorrect!")
            return redirect('account:login')

    return render(request, 'login.html')


def CustomerLogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('account:login')