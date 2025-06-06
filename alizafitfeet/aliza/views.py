from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Footwear, Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def home(request):
    # Get just 3 latest footwear items for the home page
    latest_footwear = Footwear.objects.filter(is_available=True)[:3]
    return render(request, 'index.html', {'footwear': latest_footwear})

def collections(request):
    category = request.GET.get('category', 'all')
    page = request.GET.get('page', 1)
    
    # Get all available footwear
    footwear_list = Footwear.objects.filter(is_available=True)
    
    # Apply category filter if not 'all'
    if category != 'all':
        footwear_list = footwear_list.filter(category=category)
    
    # Count items in each category
    category_counts = {
        'shoes': Footwear.objects.filter(is_available=True, category='shoes').count(),
        'slides': Footwear.objects.filter(is_available=True, category='slides').count(),
        'sandals': Footwear.objects.filter(is_available=True, category='sandals').count(),
    }
    
    # Set up pagination
    paginator = Paginator(footwear_list, 10)  # Show 10 items per page
    
    try:
        footwear = paginator.page(page)
    except PageNotAnInteger:
        footwear = paginator.page(1)
    except EmptyPage:
        footwear = paginator.page(paginator.num_pages)
    
    context = {
        'footwear': footwear,
        'category_counts': category_counts,
        'current_category': category,
        'page_obj': footwear,  # For pagination template
    }
    return render(request, 'collections.html', context)

def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            service = request.POST['service']
            message = request.POST['message']

            # Create a new contact entry
            contact = Contact.objects.create(
                name=name,
                email=email,
                service=service,
                message=message
            )

            # Prepare and send email notification
            context = {
                'name': name,
                'email': email,
                'service': service,
                'message': message,
            }
            
            # Render email template
            email_html = render_to_string('email/contact_notification.html', context)
            
            # Send email
            send_mail(
                subject=f'New Contact Form Submission from {name}',
                message=f'Name: {name}\nEmail: {email}\nService: {service}\nMessage: {message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                html_message=email_html,
                fail_silently=False,
            )

            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error submitting your message. Please try again.')
        
    return redirect('index') 