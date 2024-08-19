from django import forms
from .models import UploadedFile
import mimetypes


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']  # 只包括 file 字段，不包括 attributes

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = instance.file.name
        instance.size = instance.file.size

        # 自动设置 attributes 字段 (基于文件 MIME 类型)
        mime_type, _ = mimetypes.guess_type(instance.file.name)
        instance.attributes = mime_type or 'Unknown'

        if commit:
            instance.save()
        return instance
