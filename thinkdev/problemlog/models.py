from django.db import models

# Create your models here.

class Problems(models.Model):
    problem_title = models.CharField(max_length=10000)
    problem_description = models.CharField(max_length=10000) 
    problem_summary = models.CharField(max_length=10000)
    pseudo_code = models.CharField(max_length=10000)
    source_code = models.CharField(max_length=10000)
    submit_time = models.DateTimeField(auto_now_add=True)

