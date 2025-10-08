from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
# class Magazine(models.Model):
#     email = models.EmailField()
    
#     def __str__(self):
#         return self.email
    

# ----------------------------E-NEWS CODE----------------------
    
class Newspaper(models.Model):
    date = models.DateField()
    pdf_file = models.FileField(upload_to='uploads/pdfs/', null=True, blank=True)
    video_file = models.FileField(upload_to='uploads/videos/', blank=True, null=True)

    def __str__(self):
        return f"{self.date} {self.pdf_file.name} {self.video_file.name}"
    
    
class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=50,unique=True)
    video_title = models.CharField(max_length=255)
    published_at = models.DateField() 

    def __str__(self):
        return self.video_title
    
    def get_youtube_embed_url(self):
        return f"https://www.youtube.com/embed/{self.video_id}"
    