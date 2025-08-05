from django.shortcuts import render, redirect
from vacancy.models import GenerateVacancy,Applicant,Applicantskill
from projects.models import Services,Project
from django.shortcuts import render,redirect,get_object_or_404
from course.models import Course
from django.contrib import messages
from .models import Testimonial
from .forms import TestimonialForm


def home(request):
    service = Services.objects.all()[:3]
    intern = GenerateVacancy.objects.filter(level=GenerateVacancy.LevelChoices.INTERN)[:3]
    jobs = GenerateVacancy.objects.filter(
        level__in=[GenerateVacancy.LevelChoices.JUNIOR, GenerateVacancy.LevelChoices.SENIOR]
    )[:3]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    courses = Course.objects.filter(is_active=True)[:3]
    context ={
        'service':service,
        'intern':intern,
        'jobs':jobs,
        'testimonials':testimonials,
        'courses':courses
    }


    return render(request,'home.html',context)



def development_services(request):
    queryset=Services.objects.filter(faculty='development')
    context={'queryset':queryset}
    return render(request,'development.html',context)


def marketing_services(request):
    service=Services.objects.filter(faculty='digitalmarketing')
    context={'service':service}
    return render(request,'Digitalmarketing_form.html',context)

def combo_packages(request):
    combos = Services.objects.filter(faculty='combo')  # Use 'combo' as the faculty tag
    context = {'combos': combos}
    return render(request, 'combo.html', context)



def Digitalmarketing_form(request):
    return render(request,'Digitalmarketing_form.html')


def applicant(request,id):
    vacancy=GenerateVacancy.objects.get(id=id)
    return render(request,'applicant_form.html',{'vacancy':vacancy})


# def contact(request):
#     if request.method == 'POST':
#         print("POST request received")
#         form = ContactForm(request.POST)
#         print("Form data:", request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             phone = form.cleaned_data['phone']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             # Here you can add code to send email or save to database
#             # Create a new Contact object and save to database
#             contact = Contact.objects.create(
#                 name=name,
#                 email=email, 
#                 phone=phone,
#                 subject=subject,
#                 message=message
#             )
#             contact.save()
#             messages.success(request, 'Your message has been sent successfully!')
#             return redirect('contact')
#         else:
#             print("Form errors:", form.errors)
#     else:
#         form = ContactForm()
    
#     return render(request, 'contact.html', {'form': form})

def application_form(request,id):
    vacancydetails = get_object_or_404(GenerateVacancy,id=id)

    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        try:
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
                vacancydetails=vacancydetails
            )

            # Handle skills
            skills_input = data.get('skills', '')
            if skills_input:
                try:
                    # Try to parse as JSON first (in case it's still in JSON format)
                    import json
                    skills_list = json.loads(skills_input)
                except json.JSONDecodeError:
                    # If not JSON, treat as comma-separated string
                    skills_list = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
                
                skills_objects = [Applicantskill.objects.get_or_create(name=skill)[0] for skill in skills_list]
                applicant.skills.set(skills_objects)

            messages.success(request,f"{applicant.name} has applied for {applicant.vacancydetails.job_type} {applicant.vacancydetails.position} ({applicant.vacancydetails.level})")
            return redirect('applicant')
        except Exception as e:
            # messages.error(request, f"Error submitting application: {str(e)}")
            return redirect(request.path)

    return render(request, 'applicant_form.html')

# def collabform(request):
#     if request.method == 'POST':
#         print("POST request received for collaboration")
#         company_name = request.POST.get('company_name')
#         company_email = request.POST.get('email')
#         industry_type = request.POST.get('industry')
#         message = request.POST.get('message')
        
#         print("Form data:", request.POST)
        
#         try:
#             collaboration = Collaboration.objects.create(
#                 company_name=company_name,
#                 company_email=company_email,
#                 industry_type=industry_type,
#                 message=message
#             )
#             collaboration.save()
#             messages.success(request, 'Your collaboration proposal has been submitted successfully!')
#             return redirect('collab')
#         except Exception as e:
#             print("Error saving collaboration:", str(e))
#             messages.error(request, 'There was an error submitting your proposal. Please try again.')
#     return render(request, 'collabform.html')

from django.contrib import messages


def service_form(request, id):
    service = get_object_or_404(Services, id=id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        description = request.POST.get('description')
        
        try:
            # Create the project
            Project.objects.create(
                name=name,
                company_name=company_name,
                email=email,
                contact=contact,
                description=description,
                servicedetails=service
            )
            messages.success(request, "Your service request has been submitted. We'll contact you soon!")
            return redirect('service_form', id=id)
        except Exception as e:
            messages.error(request, f"Error submitting request: {str(e)}")
            return redirect(request.path)

    context = {
        'service': service
    }

    return render(request, 'service_form.html', context)




def about(request):
    return  render(request,'about.html')



# @api_view(['POST'])
# def postdata(request):
#     serializer = userserializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response (serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.data,status=status.http_400_BAD_REQUEST)


def blog_post(request):
    return render(request, 'blog-post.html')


def courses(request):
    try:
        from course.models import Course
        courses = Course.objects.filter(is_active=True)
        return render(request, 'courses.html', {'courses': courses})
    except Exception as e:
        print(f"Error in courses view: {str(e)}")
        return render(request, 'courses.html', {'courses': [], 'error': str(e)})


def course_registration(request):
    return render(request, 'course_form.html')


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})




def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                testimonial = form.save()
                messages.success(request, 'Thank you! Your testimonial has been submitted successfully.')
                return redirect('testimonial-form')
            except Exception as e:
                messages.error(request, 'An error occurred while saving your testimonial. Please try again.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TestimonialForm()
    return render(request, 'testimonial_form.html', {'form': form})

def testimonial_list(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'testimonial_list.html', {'testimonials': testimonials})


def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully!')
    return redirect('testimonial-list')

