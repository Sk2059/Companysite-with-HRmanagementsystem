from django.shortcuts import render,redirect,get_object_or_404
from .models import Characterstics,Project,Services,Startproject,Pastprojects
from myapp.models import Employee  # Import User from myapp
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from datetime import date
from .models import Pastprojects
from django.core.mail import send_mail

# Create your views here.

def Servicelist_list(request):
    services = Services.objects.all()
    return render(request, 'service_list.html', {'services': services})


def service_list_frontt(request):
    services = Services.objects.all()
    context = {
        'services': services
    }
    return render(request, 'service.html', context)


def create_service(request):
    if request.method == 'POST':
        data = request.POST
        service_name = data.get('service_name')
        faculty = data.get('faculty')
        price = data.get('price')
        service_image=request.FILES.get('service_image')
        
        # Create the project
        service = Services.objects.create(
            service_name=service_name,
            faculty=faculty,
            price=price
        )
        
        # Handle characteristics (similar to skills in create.html)
        characteristics_input = request.POST.get('characteristics', '')
        characteristics_list = [char.strip() for char in characteristics_input.split(',') if char.strip()]
        characteristics_objects = []
        
        for char_name in characteristics_list:
            characteristic, created = Characterstics.objects.get_or_create(name=char_name)
            characteristics_objects.append(characteristic)
        
        characteristics_objects=characteristics_objects[:6]
        # Set the characteristics
        service.characterstics.set(characteristics_objects)
        
        return redirect('service-list')
        
    return render(request, 'create_service.html')


def update_service(request, id):
    service = get_object_or_404(Services, id=id)
    existing_characterstics=[characterstic.name for characterstic in service.characterstics.all()]
    characteristics_string = ', '.join([char.name for char in service.characterstics.all()])
    
    if request.method == 'POST':
        data = request.POST
        
        service.service_name = data.get('service_name')
        service.faculty = data.get('faculty')
        service.price = data.get('price')
        # Handle characteristics
        characteristics_input = request.POST.get('characteristics', '')
        characteristics_list = [char.strip() for char in characteristics_input.split(',') if char.strip()]
        characteristics_objects = []
        
        for char_name in characteristics_list:
            characteristic, created = Characterstics.objects.get_or_create(name=char_name)
            characteristics_objects.append(characteristic)
        
        service.characterstics.set(characteristics_objects)
        service.save()
        messages.success(request, f"{service.service_name} is updated successfully")

        return redirect('service-list')
    
    context = {
    'service': service,
    'existing_characteristics': json.dumps(existing_characterstics),
}
    return render(request, 'update_service.html', context) 


def delete_service(request,id):
    service=get_object_or_404(Services,id=id)
    service.delete()
    messages.success(request, f" {service.service_name} is removed from our services successfully")
    return redirect('service-list')
    

def delete_project(request,id):
    project = get_object_or_404(Project,id=id)
    project.delete()
    return redirect('project-list')


def create_project(request, id):
    service = get_object_or_404(Services, id=id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        description = request.POST.get('description')
        
        # Create the project
        project = Project.objects.create(
            name=name,
            company_name=company_name,
            email=email,
            contact=contact,
            description=description,
            servicedetails=service
        )
        
        messages.success(request, f"A new {service.service_name} project from {company_name}")
        return redirect('project-list')

    context = {
        'service': service
    }

    return render(request, 'create_project.html', context)


def project_list(request):
    # Get all projects that don't have a corresponding Startproject entry
    projects = Project.objects.exclude(
        id__in=Startproject.objects.values_list('project_id', flat=True)
    )
    return render(request, 'project_list.html', context={'projects': projects})


def create_startproject(request, id):
    project = get_object_or_404(Project, id=id)
    
    if request.method == 'POST':
        description = request.POST.get('description')
        price = request.POST.get('price')
        deadline = request.POST.get('deadline')
        assigned_users_str = request.POST.get('assigned_users', '')
        
        print("Assigned Users String:", assigned_users_str)  # Debug print
        
        # Create the start project
        start_project = Startproject.objects.create(
            project=project,
            description=description,
            price=price,
            deadline=deadline,
            status='started'
        )
        
        # Add assigned users by their IDs
        if assigned_users_str:
            assigned_user_ids = [id.strip() for id in assigned_users_str.split(',') if id.strip()]
            print("Assigned User IDs:", assigned_user_ids)  # Debug print
            users = Employee.objects.filter(id__in=assigned_user_ids)
            print("Found Users:", [user.name for user in users])  # Debug print
            start_project.assigned_users.set(users)
            print("Assigned Users after save:", [user.name for user in start_project.assigned_users.all()])  # Debug print

            send_mail(
                f"Dear {project.company_name}",
        f"We are pleased to confirm Our acceptance of the {project.servicedetails.service_name} project. Thank you for the opportunity—We are looking forward to work together to ensure a successful outcome.",
        "Click Digitals"
        'clickdigitals2024@gmail.com',  # from email
        [project.email],  # to email (must be a list)
        fail_silently=False,
    )
        
        return redirect('startproject-list')
    
    # Get all users for the available employees list
    available_users = Employee.objects.all()
    
    context = {
        'project': project,
        'available_users': available_users
    }
    return render(request, 'accept_project.html', context)


def update_startproject(request, id):
    startproject = get_object_or_404(Startproject, id=id)
    if request.method == 'POST':
        startproject.description = request.POST.get('description')
        startproject.status = request.POST.get('status')
        startproject.deadline = request.POST.get('deadline')
        
        # Handle assigned users
        assigned_users_str = request.POST.get('assigned_users', '')
        if assigned_users_str:
            assigned_user_ids = [id.strip() for id in assigned_users_str.split(',') if id.strip()]
            users = Employee.objects.filter(id__in=assigned_user_ids)
            startproject.assigned_users.set(users)
        
        startproject.save()
        messages.success(request,f"{startproject.project.servicedetails.service_name} project of {startproject.project.company_name} is update successfully")
        return redirect('startproject-list')
    
    # Get all users for the available employees list
    available_users = Employee.objects.all()
    
    # Get currently assigned user IDs
    assigned_user_ids = [str(user.pk) for user in startproject.assigned_users.all()]
    
    context = {
        'startproject': startproject,
        'status_choices': Startproject.StatusChoices.choices,
        'available_users': available_users,
        'assigned_user_ids': ','.join(assigned_user_ids)
    }
    return render(request, 'update_startproject.html', context)


def startproject_list(request):
    startprojects = Startproject.objects.all().order_by('deadline').prefetch_related('assigned_users')
    today = date.today()
    
    projects_data = []
    for project in startprojects:
        days_remaining = (project.deadline - today).days
        if days_remaining < 0:
            days_remaining = abs(days_remaining)
            days_text = f"{days_remaining} days ago"
        else:
            days_text = f"{days_remaining} days remaining"
        
        assigned_users = project.assigned_users.all()
        print( [user.name for user in assigned_users])  # Debug print
            
        projects_data.append({
            'project': project,
            'days_remaining': days_text,
            'is_urgent': days_remaining <= 7,
            'assigned_users': assigned_users
        })
    
    context = {
        'projects_data': projects_data
    }
    return render(request, 'startproject_list.html', context)


def delete_startproject(request,id):
    startproject=get_object_or_404(Startproject,id=id)
    queryset=startproject.project
    startproject.delete()
    startproject.delete()
    messages.success(request,f"{startproject.project.servicedetails.service_name} project for {startproject.project.company_name} is deleted successfully")
    return redirect('deploy-list')


def deploy_project(request, id):
    startproject = get_object_or_404(Startproject, id=id)
    projects=Pastprojects.objects.all()
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating:
            # Create Pastproject entry
            past_project = Pastprojects.objects.create(
                title=startproject.project.name,
                company_name=startproject.project.company_name,
                faculty=startproject.project.servicedetails.faculty,
                price=startproject.price,
                email=startproject.project.email,
                contact=startproject.project.contact,
                deadline=startproject.deadline,
                rating=int(rating)  # Convert to integer since we're using whole numbers 1-5
            )
            
            # Add assigned users to past project
            past_project.assigned_users.set(startproject.assigned_users.all())
            
            # Delete from Startproject and Project
            project_pk = startproject.project.pk
            startproject.delete()
            Project.objects.filter(pk=project_pk).delete()
            for user in past_project.assigned_users.all():
                user.projects=user.projects+1
                user.add_rating(int(rating))
                user.save()
            messages.success(request,f"{past_project.title} project of {startproject.project.company_name} is update successfully")
            return redirect('deploy-list')
    context = {
        'project': startproject,
        'rate': [1, 2, 3, 4, 5]
    }
    return render(request, 'deploy_project.html', context)


def deploy_list(request):
    deployed_projects = Pastprojects.objects.all().order_by('-deadline').prefetch_related('assigned_users')
    today = date.today()
    search_query = request.GET.get('search', '').strip()

    if search_query:
        deployed_projects = deployed_projects.filter(
            Q(title__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(faculty__icontains=search_query) |
            Q(assigned_users__name__icontains=search_query) 
        ).distinct()

    projects_data = []
    for project in deployed_projects:
        days_remaining = (project.deadline - today).days
        if days_remaining < 0:
            days_remaining = abs(days_remaining)
            days_text = f"Completed {days_remaining} days ago"
        else:
            days_text = f"{days_remaining} days remaining"

        projects_data.append({
            'project': project,
            'days_text': days_text
        })

    context = {
        'projects_data': projects_data,
        'search_query': search_query,
    }
    return render(request, 'deploy_list.html', context)


@csrf_exempt
def delete_deployed_project(request, id):
    if request.method == 'POST':
        deployed = Pastprojects.objects.get(id=id)
        # Try to delete from Project and Startproject if possible (by title/company_name)
        Project.objects.filter(name=deployed.title, company_name=deployed.company_name).delete()
        Startproject.objects.filter(project__name=deployed.title, project__company_name=deployed.company_name).delete()
        deployed.delete()
    return redirect('deploy-list')



