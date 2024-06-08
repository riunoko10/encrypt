from django.db import models

# Create your models here.

class DataUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone} - {self.address}"

class LoginUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dataUser = models.ForeignKey(DataUser, on_delete=models.CASCADE, null=True, blank=True, related_name='loginUser')
    
    def __str__(self):
        return f"{self.username} - {self.password}"