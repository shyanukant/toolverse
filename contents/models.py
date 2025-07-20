from django.db import models
from django.contrib.auth.models import User
from brands.models import BrandModel
  
# response mdoel from opan ai api 
class ResponseModel(models.Model):
    brand = models.ForeignKey(BrandModel, on_delete=models.CASCADE, related_name="brand_response")
    response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.response['topic']