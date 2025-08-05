from django.db import models
from django.forms import ValidationError
from decimal import Decimal



class Applicantskill(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Skill name (e.g., "Python", "JavaScript")
    
    def __str__(self):
        return self.name
class GenerateVacancy(models.Model):
    class LevelChoices(models.TextChoices):
        INTERN = 'intern'
        JUNIOR = 'junior'
        SENIOR = 'senior'
    class StreamChoices(models.TextChoices):
        DEVELOPMENT = 'development'
        DIGITAL_MARKETING = 'digitalmarketing'
    class JobTypeChoices(models.TextChoices):
        PART_TIME = 'parttime'
        FULL_TIME = 'fulltime'

    job_type = models.CharField(choices=JobTypeChoices.choices, default=JobTypeChoices.FULL_TIME, max_length=20)
    faculty = models.CharField(choices=StreamChoices.choices, default=StreamChoices.DEVELOPMENT, max_length=20)
    level = models.CharField(choices=LevelChoices.choices, default=LevelChoices.INTERN, max_length=20)
    position = models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    task=models.CharField(max_length=100)
    background_image=models.ImageField(upload_to='vacancy-background')


class Applicant(models.Model):
    
    class GenderChoices(models.TextChoices):
        MALE='male'
        FEMALE='female'
        OTHERS='others'
    class SchedulestatusChoices(models.TextChoices):
        scheduled='scheduled'
        pending='pending'
    name = models.CharField(max_length=100 ,null=False)
    age = models.IntegerField(default=20)
    gender=models.CharField(choices=GenderChoices.choices, max_length=10)
    schedule=models.CharField(choices=SchedulestatusChoices.choices,default=SchedulestatusChoices.pending,max_length=20)
    image = models.ImageField(upload_to="applicant-image")
    resume=models.FileField(upload_to="resume")
    email = models.EmailField(max_length=100)
    country=models.TextField(max_length=50)
    address=models.TextField(max_length=50)
    contact = models.CharField(max_length=15)  # Use CharField for contact (to handle dashes/parentheses)
    experience = models.IntegerField(default=0)
    education = models.CharField(max_length=100,default='not specified')
    schedule_date=models.DateField(null=True,blank=True)
    # Many-to-many relationship with skills
    skills = models.ManyToManyField(Applicantskill, blank=True)
    vacancydetails=models.ForeignKey(GenerateVacancy,on_delete=models.CASCADE,related_name='vacancy')
    def clean(self):

        if self.age <= 10:
            raise ValidationError('Age should be greater than 10.')
        if self.age < 0:
            raise ValidationError('Age cannot be negative.')
        if self.experience < 0:
            raise ValidationError('Experience cannot be negative.')
    def __str__(self):
        return self.name

class PostInterview(models.Model):
    filtered_applicant=models.ManyToManyField(Applicant,related_name='interview')
    rating=models.IntegerField(default=0)