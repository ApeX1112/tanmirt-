from django.db import models
from django.contrib.auth.models import User

class TanmirtPost(models.Model):
    image=models.ImageField(upload_to="images")
    title=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()


    def __str__(self):
        return self.title[:100]




