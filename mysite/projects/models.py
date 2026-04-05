from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # upload_to creates a 'portfolio' folder inside your medio directory
    image = models.ImageField(upload_to='portfolio/')
    project_link = models.URLField(blank=True)

    def __str__(self):
        return self.title

