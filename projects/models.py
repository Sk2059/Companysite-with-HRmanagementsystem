from django.db import models
from myapp.models import Employee
from decimal import Decimal


# Create your models here
class Characterstics(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Skill name (e.g., "Python", "JavaScript")
    
    def __str__(self):
        return self.name


class Services(models.Model):
    class StreamChoices(models.TextChoices):
        DEVELOPMENT = 'development'
        DIGITAL_MARKETING = 'digitalmarketing'
        COMBO = 'combo'
    service_name=models.CharField(max_length=100)
    characterstics=models.ManyToManyField(Characterstics,blank=True)
    faculty=models.CharField(choices=StreamChoices.choices,max_length=100)
    price=models.IntegerField()
    

class Project(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=200) 
    company_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    contact=models.BigIntegerField()
    servicedetails=models.ForeignKey(Services,on_delete=models.CASCADE,related_name='project')
   
   
    def __str__(self) -> str:
        return self.name

class Startproject(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING='pending'
        STARTED='started'
        COMPLETED='completed'
        
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='startproject')
    assigned_users = models.ManyToManyField(Employee, related_name='assigned_projects')
    description=models.TextField(max_length=200)
    price = models.IntegerField()
    deadline = models.DateField()
    status = models.CharField(choices=StatusChoices.choices, max_length=100)
    
    def __str__(self):
        return f"{self.project.name} - {self.status}"
    
class Pastprojects(models.Model):
    class DepartChoices(models.TextChoices):
        DEVELOPMENT='development'
        DIGITAL_MARKETING='digital marketing'
    email=models.EmailField(max_length=100)
    contact=models.IntegerField()
    title=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100)
    faculty=models.CharField(choices=DepartChoices.choices,max_length=100)
    assigned_users = models.ManyToManyField(Employee,related_name='past_projects')
    price = models.IntegerField()
    deadline=models.DateField()
    rating = models.IntegerField(default=0)  # Changed to IntegerField since we're using whole numbers 1-5
    



    