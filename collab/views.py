from django.shortcuts import render,redirect,get_object_or_404
from collab.models import Collab,ContactUs,Partners
from django.contrib import messages
from collab.forms import ContactUsForm
from django.core.mail import send_mail


def create_collab(request):
    if request.method == 'POST':
        data = request.POST
        company_name = data.get('company_name')
        email = data.get('email')
        industry = data.get('industry')
        description = data.get('description')
        contact = data.get('contact')

        try:
            Collab.objects.create(
                company_name=company_name,
                email=email,
                industry=industry,
                description=description,
                contact=contact
            )
            messages.success(request, "Your collaboration request has been submitted. We'll reach out soon!")
            return redirect('create_collab')
        except Exception as e:
            messages.error(request, f"Error submitting request: {str(e)}")
            return redirect(request.path)

    return render(request, 'collabform.html')

def delete_collab(request,id):
    
    collab=get_object_or_404(Collab,id=id)
    collab.delete()
    return redirect('collab_list')


def collab_list(request):
    queryset = Collab.objects.exclude(
        id__in=Partners.objects.values_list('partner_id', flat=True)
    )
    context={'queryset':queryset}
    return render(request,'collab_list.html',context)

def create_partner(request,id):
    queryset=get_object_or_404(Collab,id=id)
    Partners.objects.create(
        partner=queryset
    )
    message = (
    f"Thank you for your collaboration idea {queryset.company_name} .\n"
    "Our team has decided to accept the your collaboration idea.\n\n"
    "Looking forward to interact wand grow together .\n"
    
)

    send_mail(
    f"Dear {queryset.company_name}",
    message,
    "clickdigitals2024@gmail.com",  # from email
    [queryset.email],                   # recipient list
    fail_silently=False             # keyword argument
)    
    return redirect('partner_list')

def partners_list(request):
    queryset=Partners.objects.all()
    context={'queryset':queryset}
    return render(request,'partners_list.html',context)


def delete_partner(request,id):
    queryset=get_object_or_404(Partners,id=id)
    collab=queryset.partner
    queryset.delete()
    collab.delete()
    
    return redirect('partner_list')


def create_contact(request):
    if request.method == 'POST':
        print("POST request received")
        form = ContactUsForm(request.POST)
        print("Form data:", request.POST)
        if form.is_valid():
            print("Form is valid")
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # Here you can add code to send email or save to database
            # Create a new Contact object and save to database
            contact = ContactUs.objects.create(
                name=name,
                email=email, 
                contact=contact,
                subject=subject,
                message=message
            )
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            print("Form errors:", form.errors)
    else:
        form = ContactUsForm()
    
    return render(request, 'contact.html', context={'form': form})


def contact_list(request):
    queryset=ContactUs.objects.all()
    context={'queryset':queryset}
    return render(request,'message_list.html',context)

def delete_contact(request,id):
    queryset=get_object_or_404(ContactUs,id=id)
    queryset.delete()
    messages.success(request,"contact deleted successfully")
    return redirect('contact_list')
    


