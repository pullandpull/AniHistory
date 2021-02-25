from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Anime_Bookmarks(models.Model):
    anime_title = models.CharField(max_length = 128, null = False)
    clean_title = models.CharField(max_length = 128, null = False)
    anime_cover = models.URLField(max_length=128, null = False)
    anime_vid_id = models.SlugField(max_length=128, null = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_added = models.DateField(auto_now_add=True, null = False)

    def __str__(self):
        return self.clean_title