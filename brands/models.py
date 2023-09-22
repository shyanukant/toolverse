from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from fonts.fonts import popular_google_fonts
from django.templatetags.static import static
# Create your models here.

# Define choices for the brand fonts
BRAND_FONT_CHOICES = [(font, font) for font in popular_google_fonts]

    
# brand model - user brand details
class BrandModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="brand_profile")
    brand_name = models.CharField(max_length=50, default='My Brand', null=False, blank=False, unique=True)
    handle_or_website = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='brand_logos/')
    font = models.CharField(max_length=300, choices=BRAND_FONT_CHOICES, null=False, blank=False)
    color1 = ColorField(default='#FFFFFF', format='hexa', blank=True, null=True)
    color2 = ColorField(default='#FFFFFF',format='hexa', blank=True, null=True)
    color3 = ColorField(default='#FFFFFF',format='hexa', blank=True, null=True)
    color4 = ColorField(default='#FFFFFF',format='hexa', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.handle_or_website} for {self.user.username}"