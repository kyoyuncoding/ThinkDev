from django.db import models

# Create your models here.
class Problems(models.Model):
    username = models.CharField(max_length=255)
    problem_title = models.CharField(max_length=10000)
    problem_description = models.CharField(max_length=10000) 
    problem_summary = models.CharField(max_length=10000)
    pseudo_code = models.CharField(max_length=10000)
    source_code = models.CharField(max_length=10000)
    solved = models.CharField(max_length=50)
    submit_time = models.DateTimeField(auto_now_add=True)

class ProblemVersions(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    version_number = models.IntegerField(default=1)
    problem_title = models.CharField(max_length=10000)
    problem_description = models.CharField(max_length=10000) 
    problem_summary = models.CharField(max_length=10000)
    pseudo_code = models.CharField(max_length=10000)
    source_code = models.CharField(max_length=10000)
    solved = models.CharField(max_length=50)
    submit_time = models.DateTimeField(auto_now_add=True)


