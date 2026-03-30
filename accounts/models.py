from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    def __str__(self):
        return self.user.username
    
class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'HR'),
        ('IT', 'IT'),
        ('FINANCE','FINANCE'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    
    def __str__(self):
        return self.department
    
class UserDepartment(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.user.username} - {self.department.department}"