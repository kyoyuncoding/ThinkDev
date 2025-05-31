from django.db import models

# Create your models here.

class Problems(models.Model):
    username = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255)
    problem_title = models.CharField(max_length=255)
    problem_description = models.CharField(max_length=255) 
    problem_summary = models.CharField(max_length=255)
    pseudo_code = models.CharField(max_length=255)
    source_code = models.CharField(max_length=255)
    submit_time = models.DateTimeField(auto_now_add=True)

