from django.db import models

# Create your models here.

class Course(models.Model):

    All_levels=[
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('advanced','Advanced'),
        ('all_levels','All Levels'),
        ('beginner_to_advanced','Beginner to Advanced'),
    ]
    course_type=[
        ('web_development','Web Development'),
        ('digital_marketing','Digital Marketing'),
        ('data_science','Data Science & AI'),
        ('ui_ux','UI/UX Design'),
    ]
   
    mode=[
        ('online','Online'),
        ('offline','Offline'),
        ('online/offline','online/offline'),
    ]
        

    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=200, choices=All_levels, default='beginner')
    duration = models.CharField(max_length=200)
    course_type = models.CharField(max_length=200, choices=course_type, default='web_development')
    mode = models.CharField(max_length=200, choices=mode, default='online')
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    syllabus = models.JSONField(default=list, blank=True, help_text="Course syllabus stored as JSON")

    def __str__(self):
        return self.title



class CourseRegistration(models.Model):
    COURSE_TYPES = [
        ('web_development', 'Web Development'),
        ('digital_marketing', 'Digital Marketing'),
        ('data_science', 'Data Science & AI'),
        ('ui_ux', 'UI/UX Design'),
    ]
    DURATION_CHOICES = [
        ('3_months', '3 Months'),
        ('6_months', '6 Months'),
        ('1_year', '1 Year'),
    ]
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    ]
    BATCH_CHOICES = [
        ('morning', 'Morning (9 AM - 12 PM)'),
        ('afternoon', 'Afternoon (2 PM - 5 PM)'),
        ('evening', 'Evening (6 PM - 9 PM)'),
    ]

    # Personal Info
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    # Course Selection
    course_type = models.CharField(max_length=50, choices=COURSE_TYPES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    batch = models.CharField(max_length=20, choices=BATCH_CHOICES)

    # Education
    qualification = models.CharField(max_length=100)
    institute = models.CharField(max_length=150)
    experience = models.TextField(blank=True)

    # Technical
    skills = models.TextField(blank=True)
    expectations = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.course_type}"
