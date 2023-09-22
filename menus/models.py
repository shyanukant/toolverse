from django.db import models

# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=300, null=False, blank=False)
    file = models.FileField(upload_to="contacts/", null=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.subject