from django.db import models


    
class Testimonial(models.Model):
    company_name = models.CharField(max_length=100)
    company_type = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='testimonials/logos/')
    
    quote = models.TextField()
    
    author_name = models.CharField(max_length=100)
    author_position = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='testimonials/authors/')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author_name} - {self.company_name}"