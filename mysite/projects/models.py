from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # upload_to creates a 'portfolio' folder inside your medio directory
    image = models.ImageField(upload_to='portfolio/')

    # for external websites like github etc
    project_link = models.URLField(blank=True)

    # for internal apps built inside the web portfolio
    inSiteProject = models.BooleanField(default=False)
    # the URL path name (grpc-demo)
    slug = models.SlugField(blank=True, max_length=200)

    def __str__(self):
        return self.title

