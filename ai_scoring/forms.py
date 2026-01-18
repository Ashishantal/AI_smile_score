from django import forms
from .models import ScoredImage

class ScoredImageForm(forms.ModelForm):
    class Meta:
        model = ScoredImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
