from django.db import models
from django.forms import ValidationError
from decimal import Decimal
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Skill name (e.g., "Python", "JavaScript")
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    class StreamChoices(models.TextChoices):
        DEVELOPMENT = 'development'
        DIGITAL_MARKETING = 'digitalmarketing'

    class LevelChoices(models.TextChoices):
        INTERN = 'intern'
        JUNIOR = 'junior'
        SENIOR = 'senior'
    class GenderChoices(models.TextChoices):
        MALE='male'
        FEMALE='female'
        OTHERS='others'
    class JobTypeChoices(models.TextChoices):
        PART_TIME = 'parttime'
        FULL_TIME = 'fulltime'
    
    name = models.CharField(max_length=100 ,null=False)
    age = models.IntegerField(default=20)
    gender=models.CharField(choices=GenderChoices.choices, max_length=10)
    position = models.CharField(max_length=50)
    image = models.ImageField(upload_to="employee-image")
    email = models.EmailField(max_length=100)
    country=models.TextField(max_length=50)
    address=models.TextField(max_length=50)
    contact = models.CharField(max_length=15)  # Use CharField for contact (to handle dashes/parentheses)
    faculty = models.CharField(choices=StreamChoices.choices, default=StreamChoices.DEVELOPMENT, max_length=20)
    level = models.CharField(choices=LevelChoices.choices, default=LevelChoices.INTERN, max_length=20)
    salary = models.BigIntegerField(default=10000)
    experience = models.IntegerField(default=0)
    job_type = models.CharField(choices=JobTypeChoices.choices, default=JobTypeChoices.FULL_TIME, max_length=20)
    education = models.CharField(max_length=100,default='not specified')
    project_ratings = models.JSONField(default=list, blank=True)
    rating= models.IntegerField()
    projects = models.IntegerField(default=0,null=True)

    
    # Many-to-many relationship with skills
    skills = models.ManyToManyField(Skill, blank=True)

    def clean(self):
        if self.salary < 0:
            raise ValidationError('Salary cannot be negative.')
        if self.age <= 10:
            raise ValidationError('Age should be greater than 10.')
        if self.age < 0:
            raise ValidationError('Age cannot be negative.')
        if self.experience < 0:
            raise ValidationError('Experience cannot be negative.')
        if self.rating is not None and (Decimal(self.rating) < 0 or Decimal(self.rating) > 5):
            raise ValidationError('Rating must be between 0 and 5')
    def add_rating(self, rating):
        """Add a new rating and update the average."""
        if isinstance(rating, int) and 0 <= rating <= 5:
            self.project_ratings.append(rating)
            avg = sum(self.project_ratings) / len(self.project_ratings)
            self.rating = round(avg, 1)
            self.save()
        else:
            raise ValueError("Rating must be an integer between 0 and 5")
    def __str__(self):
        return self.name
