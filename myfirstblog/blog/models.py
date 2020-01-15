from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# from django.core.urlresolvers import reverse
# [TYPECHECK]
# ignored-classes=approve_comments
# Create your models here.
# pylint: disable=no-member
class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # additional fields need to be added using onetoonefield

    protofolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approve_comments(self):
        return self.comments.filter(approve_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approve_comment = models.BooleanField(default=False)

    def approve(self):
        self.approve_comment = True
        self.save()
    
    def get_absolute_url(self):
        return reverse('post_list', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.text