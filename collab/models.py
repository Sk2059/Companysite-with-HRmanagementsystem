from django.db import models

class Collab(models.Model):
    company_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    industry = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    contact = models.CharField(max_length=15)  # changed from IntegerField

    def __str__(self):
        return self.company_name

class Partners(models.Model):
    partner = models.ForeignKey(Collab, on_delete=models.CASCADE, related_name='partner')

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact = models.CharField(max_length=15)  # fixed: CharField instead of IntegerField
    subject = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name
