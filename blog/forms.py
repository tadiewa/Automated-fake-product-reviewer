from django import forms

from blog.models import BlogPost , comment

class CreateBlogPostForm(forms.ModelForm):

     class Meta:
         model = BlogPost
         fields =['title' , 'body' ,'image']



## store the comment content into the db


class commentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['content' ,'rating']