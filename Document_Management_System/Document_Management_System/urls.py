"""
URL configuration for Document_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from app_sign import views
from django.conf import settings  # 确保导入 settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('login/', views.login_view, name='login'),  # 登陆网址跳转
                  path('register/', views.register_view, name='register'),  # 注册网址跳转
                  path('login_first/', views.login_first, name='login_first'),
                  path('help_center/', views.help_center, name='help_center'),
                  path('text_recognition/', views.text_recognition, name='text_recognition'),
                  path('text_classification/', views.text_classification, name='text_classification'),
                  path('my_files/', views.my_files, name='my_files'),
                  path('', RedirectView.as_view(url='/login_first/', permanent=False)),  # 根路径重定向到 /login_first/
                  path('text_classification/work_document/', views.work_document, name='work_document'),
                  path('text_classification/learning_document/', views.learning_document, name='learning_document'),
                  path('text_classification/life_document/', views.life_document, name='life_document'),
                  path('upload/', views.upload_file, name='upload_file'),
                  path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
                  path('generate_doc/', views.generate_doc, name='generate_doc'),
                  path('translate_text/', views.translate_text_view, name='translate_text'),
                  path('export_as_pdf/', views.export_as_pdf_view, name='export_as_pdf'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 在开发过程中使用Django提供的静态文件处理
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
