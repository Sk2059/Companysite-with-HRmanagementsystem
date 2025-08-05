from django.shortcuts import render, get_object_or_404
from .models import Course
from django.views.decorators.http import require_POST

# Create your views here.


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'courses.html', {'courses': courses})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'course_detail.html', {'course': course})

from django.shortcuts import render, redirect
from .forms import CourseForm , CourseRegistrationForm
from django.contrib import messages
from .models import CourseRegistration

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('add_course')
    else:
        form = CourseForm()
    return render(request, 'add_course_form.html', {'form': form})


def register_course(request, id=None):
    if id:
        course = get_object_or_404(Course, id=id)
    else:
        course = None
    
    if request.method == 'POST':
        form = CourseRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('course_register')
        else:
            # Show specific form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CourseRegistrationForm()
    return render(request, 'course_form.html', {'form': form, 'course': course})



def course_submissions(request):
    registrations = CourseRegistration.objects.order_by('-submitted_at')
    return render(request, 'course_submission.html', {'registrations': registrations})



@require_POST
def delete_registration(request, pk):
    """Delete a CourseRegistration instance and redirect back to submissions list."""
    registration = get_object_or_404(CourseRegistration, pk=pk)
    registration.delete()
    messages.success(request, 'Registration deleted successfully!')
    return redirect('course_submissions')


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_list.html', {'courses': courses})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully.')
        return redirect('course_list')
    return redirect('course_list') 
