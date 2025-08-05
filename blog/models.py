from django.db import models
import datetime
class Author(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='authors/')
    description=models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.word


class Blog(models.Model):
    title = models.CharField(max_length=200)
    detail=models.TextField()
    photo = models.ImageField(upload_to='blogs/')  # media/blogs/
    keywords = models.ManyToManyField(Keyword, related_name='blogs')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    time_to_read = models.PositiveIntegerField(help_text="Estimated reading time in minutes")
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class SubTopic(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='subtopics')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} (Blog: {self.blog.title})"
