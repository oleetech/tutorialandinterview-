from django import forms
from .models import Tutorial
from django_ckeditor_5.widgets import CKEditor5Widget

class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['title', 'content', 'topic','level', 'company', 'serial_number']
        widgets = {
            'content': CKEditor5Widget(config_name='default'),  # CKEditor5 ব্যবহার করা হয়েছে 'content' ফিল্ডে।
        }
