
from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee,Skill
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.info(request,"username not registered .please register")
            return redirect('login')
    
        user=authenticate(username=username,password=password)
        if user==None:
            messages.error(request,"invalid password")
            return redirect('login') 
        else:
            login(request,user)
            messages.success(request,f"Logged in as {username}")
            return redirect('employee-list')
    
    return render(request, './templates/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def employee_list(request):
    queryset=Employee.objects.all()
    context={'employees':queryset}
    return render(request,'list.html',context)

def create_employee(request):
    ages=range(15,60)
    experience=range(0,20)
    countries = ["Nepal", "India", "China", "Canada", "Germany", "USA",'Pakistan','Bangladesh']
    if request.method=='POST':
        
        data=request.POST
        name=data.get('name')
        age=data.get('age')
        gender=data.get('gender')
        position=data.get('position')
        image=request.FILES.get('image')
        email=data.get('email')
        contact=data.get('contact')
        faculty=data.get('faculty')
        level=data.get('level')
        salary=data.get('salary')
        job_type=data.get('jobtype')
        experience=data.get('experience')
        education=data.get('education')
        address=data.get('address')
        country=data.get('country')
        skills_input = request.POST.get('skills', '')
        skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        skills_objects = []
        for skill_name in skills_list:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            skills_objects.append(skill)
    
        user = Employee.objects.create(
            name=name,level=level,image=image,email=email,contact=contact,faculty=faculty,salary=salary,
            position=position,job_type=job_type,experience=experience,education=education,age=age,address=address,country=country,gender=gender,
            rating=0.0,projects=0
        )
        user.skills.set(skills_objects)
        message = (
    f"Welocome to the team {user.name} in CliCK DIGITALS.\n\n"
    "Looking forward to interact with you in the following days."
    "We wish you the best in your future endeavors."
)

        send_mail(
    f"Dear {user.name}",
    message,
    "clickdigitals2024@gmail.com",  # from email
    [user.email],                   # recipient list
    fail_silently=False             # keyword argument
)
        messages.success(request, f"{name} is added to the team successfully.")
        return redirect('employee-list')
    return render(request, 'create.html', context={'ages': ages,'experience':experience,'countries':countries})

# @login_required(login_url="login")
def update_employee(request, id):
    ages=range(15,60)
    experience=range(0,15)
    countries = ["Nepal", "India", "China", "Canada", "Germany", "USA",'Pakistan','Bangladesh']
    queryset = get_object_or_404(Employee, id=id)
    existing_skills = [skill.name for skill in queryset.skills.all()]
    skills_string = ', '.join([skill.name for skill in queryset.skills.all()])
    previous_rating=queryset.rating
    previous_projects=queryset.projects
    if request.method == 'POST':
        data = request.POST

        queryset.name = data.get('name')
        queryset.age = data.get('age')
        queryset.gender = data.get('gender')
        queryset.level = data.get('level')
        queryset.email = data.get('email')
        queryset.contact = data.get('contact')
        queryset.faculty = data.get('faculty')
        queryset.salary = data.get('salary')
        queryset.position = data.get('position')
        queryset.job_type = data.get('jobtype')
        queryset.experience = data.get('experience')
        queryset.education = data.get('education')
        queryset.address = data.get('address')
        queryset.country = data.get('country')
        rating_float=(data.get('rating'))
        queryset.rating=rating_float
        int_projects=(data.get('projects'))
        if int_projects.isdigit():
            if int(int_projects)<0:
                queryset.projects=previous_projects

        if 'image' in request.FILES:
            queryset.image = request.FILES['image']

     
        skills_input = request.POST.get('skills', '')
        skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        skills_objects = []
        for skill_name in skills_list:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            skills_objects.append(skill)
        queryset.skills.set(skills_objects)

        queryset.save()
        messages.success(request, f"{queryset.name}'s data is updated successfully")

        return redirect('details', id=id)

    context = {'employee': queryset, 'skills': skills_string, 'ages': ages,'experience':experience,'countries':countries,'existing_skills':existing_skills}
    return render(request, 'update.html', context)


# def employee_details(request,id):
#     queryset=User.objects.filter(id=id)
#     return render(request,'details.html',context={'employee':queryset})
# @login_required(login_url="login")
def employee_details(request,id):
    queryset=Employee.objects.get(id=id)
    context={'employee':queryset}
    return render(request,'details.html',context)
def delete_employee(request,id):
    user=get_object_or_404(Employee,id=id)
    name=user.name
    message = (
    f"I regret to inform you that you are fired from Click Digitals.\n\n"
    "Thank you for your efforts and contributions during your time at Click Digitals. "
    "We wish you the best in your future endeavors."
)

    send_mail(
    f"Dear {user.name}",
    message,
    "clickdigitals2024@gmail.com",  # from email
    [user.email],                   # recipient list
    fail_silently=False             # keyword argument
)
    user.delete()
    messages.success(request, f"{name} is fired from the company")
    return redirect('employee-list')
