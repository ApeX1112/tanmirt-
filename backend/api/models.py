from django.db import models
from django.contrib.auth.models import User



class TanmirtPost(models.Model):
    LOST="lost"
    FOUND="found"

    image=models.ImageField(upload_to="images",null=True, blank=True)
    title=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()
    lost_or_found=models.CharField(max_length=20,choices=[
        (LOST,"lost"),
        (FOUND,"found")
    ],default=LOST)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


    def __str__(self):
        return self.title[:100]
    

class Message(models.Model):
    body=models.TextField()
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    date=models.DateTimeField(auto_now_add=True)
    receiver=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='receiver',null=True)

    def __str__(self) -> str:
        return f"sent at {self.date}"
    

class Comment(models.Model):
    body=models.TextField()
    writer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='writer')
    date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(TanmirtPost,on_delete=models.CASCADE,related_name='post')

    def __str__(self) -> str:
        return f"comment written at : {self.date}"
    


class UserProfile(models.Model):
    image=models.ImageField(upload_to="profile_images",null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    latitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True )
    longitude=models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"




