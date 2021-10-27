from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver



def upload_location(instance ,filename ,**kwargs):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
      )
    return file_path


class BlogPost(models.Model):
    title =models.CharField(max_length=50, null= False, blank=False)
    body  =models.TextField(max_length=500, null =False, blank =False)
    image = models.ImageField(upload_to=upload_location, null=True,blank=True)
    status =models.CharField(max_length=50, null= False, blank=False ,default ="none")
    date_published = models.DateTimeField(auto_now_add=True,verbose_name="date_published")
    date_updated = models.DateTimeField(auto_now_add=True,verbose_name="date_updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):  
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "_"+ instance.title)
    
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)



class comment (models.Model):

    post = models.CharField(null=True,blank=True,max_length=20)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    content = models.TextField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating= models.CharField(max_length=1 , null=True , blank=True ,default="none")
    status =models.CharField(max_length=50, null= True, blank=True ,default ="none")


    def __str__(self):
        return self.content



 


    
       



