from django.db import models

# Create your models here.
class Footwear(models.Model):
    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('slides', 'Slides'),
        ('sandals', 'Sandals'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    front_image = models.ImageField(upload_to='footwear/')
    side_image = models.ImageField(upload_to='footwear/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name 

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=100, choices=[('custom', 'Custom Design'), ('repair', 'Repair'), ('consultation', 'Consultation')], default='Select Service')
    message = models.TextField()

    def __str__(self):
        return self.name