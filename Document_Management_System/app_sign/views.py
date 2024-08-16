from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile


# Create your views here.
# 登录视图
def login_view(request):
    if request.method == "POST":
        phone_number = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户信息
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            if user_profile.password == password:
                # 假设你使用自定义的UserProfile模型进行身份验证
                # Django的默认用户模型通常不会以明文存储密码，而是使用加密的形式
                # 这里假设你还没有使用django自带的用户身份验证体系
                messages.success(request, "登录成功！")
                return redirect('/help_center/')  # 登录成功后跳转到主页
            else:
                messages.error(request, "密码错误，请重试。")
        except UserProfile.DoesNotExist:
            messages.error(request, "该手机号未注册，请先注册。")

    return render(request, 'login.html')


# 注册视图
def register_view(request):
    if request.method == "POST":
        phone_email = request.POST.get('phone-email')
        password = request.POST.get('password')
        agree = request.POST.get('agree')

        if not agree:
            messages.error(request, "您必须同意服务协议和隐私政策才能注册。")
        else:
            # 检查是否手机号/邮箱已存在
            if UserProfile.objects.filter(phone_number=phone_email).exists():
                messages.error(request, "手机号/邮箱已被注册，请使用其他手机号/邮箱。")
            else:
                # 创建新的用户
                UserProfile.objects.create(phone_number=phone_email, password=password)
                messages.success(request, "注册成功，请登录。")
                return redirect('login')

    return render(request, 'register.html')


def upload_file(request):
    return render(request, 'upload.html')


def login_first(request):
    return render(request, 'login_first.html')


def help_center(request):
    return render(request, 'help_center.html')


def text_recognition(request):
    return render(request, 'text_recognition.html')


def text_classification(request):
    return render(request, 'text_classification.html')
