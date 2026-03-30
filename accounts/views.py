from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegisterForm, LoginForm, UpdateForm
from accounts.models import UserProfile, UserDepartment, Department
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def is_hr_user(user):
    if not user.is_authenticated:
        return False

    try:
        user_profile = UserProfile.objects.get(user=user)
        user_department = UserDepartment.objects.get(user=user_profile)
        return user_department.department.department == "HR"
    except:
        return False
    
def policy_upload(request):
    if not is_hr_user(request.user):
        return redirect('profile')
    else:
        return render(request, 'policy_upload.html')
    
def hr_profile(request):
    if not is_hr_user(request.user):
        return redirect('profile')
    return render(request, 'hr_profile.html')

def register_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            department = form.cleaned_data["department"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            gender = form.cleaned_data["gender"]
            create_user = User.objects.create_user(
                username = username,
                email = email,
                password = password
            )
            user_profile = UserProfile.objects.create(
                user = create_user,
                date_of_birth = date_of_birth,
                gender = gender
            )
            dept_obj = Department.objects.get(department = department)
            UserDepartment.objects.create(
                user = user_profile,
                department = dept_obj
            )
            login(request, create_user)
            return redirect('home')
    return render(request, 'register.html', {'form' : form})
            
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print("POST DATA:", request.POST)
        if form.is_valid():
           username = form.cleaned_data.get("username")
           password = form.cleaned_data.get("password")
           user = authenticate(
            request,
            username = username,
            password = password
           )
           print("AUTH USER:", user)
           if user is None:
               print("❌ AUTH FAILED")
               messages.error(request, "Invalid username and password")
               
           else :
               login(request,user) 
               if not is_hr_user(user):
                    return redirect('profile')
               else :
                    return redirect('hr_profile')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form' : form})
            
def view_profile(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user = request.user)
    else: 
        return redirect('login')
    return render(request, 'profile.html', {'profile' : user_profile})

def update_profile(request):
    if request.user.is_authenticated:
       profile = get_object_or_404(UserProfile, user = request.user)
       form = UpdateForm(instance=profile)
       if request.method == "POST":
           form = UpdateForm(request.POST,instance=profile)
           if form.is_valid():
               form.save()
               return redirect('profile')
    else :
        return redirect('login')
    return render(request, 'update.html', {'form': form})  

def users_list(request):
    if not is_hr_user(request.user):
        return redirect('profile')
    users = UserProfile.objects.all()
    return render(request, 'users_list.html', {'users' : users}) 

def logout_user(request):
    logout(request)
    return redirect('home')