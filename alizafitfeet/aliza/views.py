from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Footwear, Contact

# Create your views here.
def home(request):
    # Get just 3 latest footwear items for the home page
    latest_footwear = Footwear.objects.filter(is_available=True)[:3]
    return render(request, 'index.html', {'footwear': latest_footwear})

def collections(request):
    # Get all available footwear
    all_footwear = Footwear.objects.filter(is_available=True)
    
    # Count items in each category
    category_counts = {
        'shoes': all_footwear.filter(category='shoes').count(),
        'slides': all_footwear.filter(category='slides').count(),
        'sandals': all_footwear.filter(category='sandals').count(),
    }
    
    context = {
        'footwear': all_footwear,
        'category_counts': category_counts
    }
    return render(request, 'collections.html', context)

def contact(request):
    if request.method == 'POST':
        try:
            # Create a new contact entry
            contact = Contact.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                service=request.POST['service'],
                message=request.POST['message']
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error submitting your message. Please try again.')
        
    return redirect('index') 