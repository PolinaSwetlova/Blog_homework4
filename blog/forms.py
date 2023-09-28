from django import forms

from .models import Post, Comment, User


class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'})
        } 

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0] 


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',) 


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email') 