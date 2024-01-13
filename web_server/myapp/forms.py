from django import forms
from .models import CSVFile

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # รับนามสกุลของไฟล์
    valid_extensions = ['.csv']  # นามสกุลที่ยอมรับ

    if not ext.lower() in valid_extensions:
        raise ValidationError('Please Upload the CSV file only')

class CSVFileForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        validate_file_extension(file)
        return file