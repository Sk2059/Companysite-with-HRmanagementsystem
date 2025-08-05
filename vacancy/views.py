from django.shortcuts import redirect, render, get_object_or_404
from myapp.models import Employee,Skill
from vacancy.models import Applicant,GenerateVacancy,Applicantskill, PostInterview
from django.shortcuts import render, get_object_or_404
from django.core.files import File
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime
from datetime import date
from datetime import datetime
# Create your views here.


def vacancy_list(request):
    queryset=GenerateVacancy.objects.all()
    context={'vacancies':queryset}
    return render(request,'vacancy_list.html',context)

def internship(request):
    intern = GenerateVacancy.objects.filter(level=GenerateVacancy.LevelChoices.INTERN)
    return render(request,'internship.html',context={'intern':intern})

def jobs(request):
    jobs = GenerateVacancy.objects.filter(
        level__in=[GenerateVacancy.LevelChoices.JUNIOR, GenerateVacancy.LevelChoices.SENIOR]
    )
    return render(request,'jobs.html',context={'jobs':jobs})

def careers(request):
    jobs = GenerateVacancy.objects.filter(
        level__in=[GenerateVacancy.LevelChoices.JUNIOR, GenerateVacancy.LevelChoices.SENIOR]
    )
    intern = GenerateVacancy.objects.filter(level=GenerateVacancy.LevelChoices.INTERN)
    return render(request, 'careers.html', context={'jobs': jobs, 'intern': intern})

def create_vacancy(request):
    if request.method=='POST':
        data=request.POST
        job_type=data.get('job_type')
        position=data.get('position')
        level=data.get('level')
        faculty=data.get('faculty')
        description=data.get('description')
        background_image=request.FILES.get('background_image')
        task=data.get('task')
        GenerateVacancy.objects.create(
            job_type=job_type,
            position=position,
            level=level,
            faculty=faculty,
            description=description,
            background_image=background_image,
            task=task

        )
        messages.success(request,f"Vacancy for {job_type} {level} {position} is created successfully")
        return redirect('vacancy')
    return render(request,'create_vacancy.html')

def update_vacancy(request,id):
    vacancy=get_object_or_404(GenerateVacancy,id=id)
    if request.method=='POST':
        data=request.POST
        vacancy.job_type=data.get('job_type')
        vacancy.position=data.get('position')
        vacancy.level=data.get('level')
        vacancy.faculty=data.get('faculty')
        vacancy.description=data.get('description')
        vacancy.task=data.get('task')
        if request.FILES.get('background_image'):
            vacancy.background_image=request.FILES.get('background_image')
        vacancy.save()
        messages.success(request,f"Vacancy for {vacancy.job_type} {vacancy.level} {vacancy.position} is updated  successfully")
        return redirect('vacancy')
    return render(request,'update_vacancy.html',context={'vacancy':vacancy})


def delete_vacancy(request,id):
    vacancy=get_object_or_404(GenerateVacancy,id=id)
    vacancy.delete()
    return redirect('vacancy')


def apply_for_vacancy(request, vacancy_id):
    
    ages=range(15,60)
    experience=range(0,20)
    countries = ["Nepal", "India", "China", "Canada", "Germany", "USA",'Pakistan','Bangladesh']
    vacancydetails = get_object_or_404(GenerateVacancy, id=vacancy_id)

    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        applicant = Applicant.objects.create(
            name=data.get('name'),
            age=data.get('age'),
            gender=data.get('gender'),
            image=files.get('image'),
            resume=files.get('resume'),
            email=data.get('email'),
            country=data.get('country'),
            address=data.get('address'),
            contact=data.get('contact'),
            experience=data.get('experience'),
            education=data.get('education'),
            vacancydetails=vacancydetails,
            schedule=Applicant.SchedulestatusChoices.pending
        )

        # Handle skills
        skills_input = data.get('skills', '')
        skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        skills_objects = [Applicantskill.objects.get_or_create(name=skill)[0] for skill in skills_list]
        applicant.skills.set(skills_objects)
        messages.success(request,f"{applicant.name} has applied for {applicant.vacancydetails.job_type} {applicant.vacancydetails.position} ({applicant.vacancydetails.level})")
        return redirect('vacancy_applicants_list')  # Or success page

    return render(request, 'apply_form.html',context={'vacancy': vacancydetails,'ages': ages,'experience':experience,'countries':countries})



def schedule_interview(request, id):
    applicant = get_object_or_404(Applicant, id=id)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        if date_str:
            try:
                schedule_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                applicant.schedule_date = schedule_date
                applicant.schedule = Applicant.SchedulestatusChoices.scheduled
                applicant.save()
                message = (
    f"Thank you for your interest in joining Click Digitals.\n We have successfully received your application and CV for the position of {applicant.vacancydetails.position}.\nYou are requested to attend your  interview on {applicant.schedule_date} with a set of task as our hiring process.\n\n TASK :\n[{applicant.vacancydetails.task}]\nPlease bring your competed taskin the interview on {applicant.schedule_date}.\nIf you have any questions about the task or the interview, feel free to contact us.\n\nBest regards,\n[Click Gigitals]"
)

                send_mail(
    f"Dear {applicant.name}",
    message,
    "clickdigitals2024@gmail.com",  # from email
    [applicant.email],                   # recipient list
    fail_silently=False             # keyword argument
)
                return redirect('vacancy_applicants_list')
            except ValueError:
                messages.error(request, 'Invalid date format.')
        else:
            messages.error(request, 'Please select a date.')

    return render(request, 'schedule.html', context={'applicant': applicant})

    
def vacancy_applicants_list(request):
    filtered_ids = PostInterview.filtered_applicant.through.objects.values_list('applicant_id', flat=True)
    applicants = Applicant.objects.exclude(id__in=filtered_ids)
    today = date.today()
    applicants_list = []

    for applicant in applicants:
        if applicant.schedule_date:
            days_remaining = (applicant.schedule_date - today).days
            if days_remaining < 0:
                days_remaining = abs(days_remaining)
                days_text = f"{days_remaining} days ago"
            elif days_remaining == 0:
                days_text = "Today"
            elif days_remaining == 1:
                days_text = "Tomorrow"
            else:
                days_text = f"After {days_remaining} days"
        else:
            days_text = "Pending"

        applicants_list.append({
            'applicant': applicant,
            'days_remaining': days_text,
        })

    return render(request, 'applicants_list.html', context={'applicants_list': applicants_list})

def applicant_details(request,id):
    applicant=get_object_or_404(Applicant,id=id)
    skills=applicant.skills.all()
    base_url = f"{request.scheme}://{request.get_host()}"
    
    context={
       'applicant':applicant,
       'skills':skills,
       'base_url': base_url
    }
    return render(request,'applicant_details.html',context)





def reject_applicant(request,id):
    applicant=get_object_or_404(Applicant,id=id)
    applicant.delete()
    return redirect('vacancy_applicants_list')

def filter_applicants(request, id):
    applicant = get_object_or_404(Applicant, id=id)

    if request.method == 'POST':
        rating = request.POST.get('rating')

        # Step 1: Create the PostInterview object
        post_interview = PostInterview.objects.create(
            rating=rating
        )

        # Step 2: Assign the applicant to the many-to-many field
        post_interview.filtered_applicant.set([applicant])  # ✅ Correct way

        return redirect('filter_list')

    context = {
        'applicant': applicant,
        'rate': [1, 2, 3, 4, 5]
    }
    return render(request, 'filter_applicant.html', context)



def filter_list(request):
    filtered_applicants=PostInterview.objects.all()
    context={
        'filtered_applicants':filtered_applicants
    }
    return render(request,'filter_applicant_list.html',context)  

def filter_appplicant_details(request,interview_id,applicant_id):
    interview = get_object_or_404(PostInterview, id=interview_id)
    applicant = get_object_or_404(interview.filtered_applicant.all(), id=applicant_id)

    context = {
        'applicant': applicant,
        'interview': interview,
        
    }
    return render(request,'filter_applicant_details.html',context)


def hire_applicant(request, interview_id, applicant_id):
    interview = get_object_or_404(PostInterview, id=interview_id)
    applicant = get_object_or_404(Applicant, id=applicant_id)

    if request.method == 'POST':
        try:
            salary = request.POST.get('salary')

            user = Employee.objects.create(
                name=applicant.name,
                age=applicant.age,
                gender=applicant.gender,
                position=applicant.vacancydetails.position,
                image=applicant.image,
                email=applicant.email,
                country=applicant.country,
                address=applicant.address,
                contact=applicant.contact,
                faculty=applicant.vacancydetails.faculty,
                level=applicant.vacancydetails.level,
                salary=salary,
                experience=applicant.experience,
                job_type=applicant.vacancydetails.job_type,
                education=applicant.education,
                project_ratings=[],
                rating=0,
                projects=0
            )
            applicant_skill_names = applicant.skills.values_list('name', flat=True)
            skills_for_user = []
            
            for name in applicant_skill_names:
                skill_obj, created = Skill.objects.get_or_create(name=name)
                skills_for_user.append(skill_obj)
                user.skills.set(skills_for_user)
            user.save()

            message = (
    f"Welocome to the team {user.name} as a {user.position} in ClICK DIGITALS.\n\n"
    "Looking forward to interact with you in the following days.\n"
    f"Warm welcome for you in the {user.faculty} team"
)

            send_mail(
    f"Dear {user.name}",
    message,
    "clickdigitals2024@gmail.com",  # from email
    [user.email],                   # recipient list
    fail_silently=False             # keyword argument
)
            
            # Remove applicant from interviews
            for interview in PostInterview.objects.filter(filtered_applicant=applicant):
                interview.filtered_applicant.remove(applicant)

            # Delete applicant after transferring
            applicant.delete()

            return redirect('employee-list')

        except Exception as e:
            print(f'Error creating user: {e}')
            return redirect('filter_list')

    context = {
        'interview': interview,
        'applicant': applicant
    }
    return render(request, 'salary_discussion.html', context)


def delete_applicant_completely(request, applicant_id):
    # Get the applicant object
    applicant = get_object_or_404(Applicant, id=applicant_id)
    
    # Remove the applicant from all PostInterview records
    PostInterview.objects.filter(filtered_applicant=applicant).update()
    for interview in PostInterview.objects.filter(filtered_applicant=applicant):
        interview.filtered_applicant.remove(applicant)

    # Delete the applicant object
    applicant.delete()
    messages.success(request,f"{applicant.name} is rejected successfully.")

    # Redirect to the applicant list page or any appropriate page
    return redirect('filter_list')