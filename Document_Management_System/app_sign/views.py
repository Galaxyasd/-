import mimetypes

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .models import UploadedFile
from .forms import FileUploadForm
from pdf2image import convert_from_path
import os

os.environ['TESSDATA_PREFIX'] = 'D:/AppGallery/Tesseract-OCR/tessdata/'
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"D:\AppGallery\Tesseract-OCR\tesseract.exe"
from pdf2image import convert_from_path
import docx
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from PIL import Image
import logging

logger = logging.getLogger(__name__)  # 使用全局配置过的logger
import time
from googletrans import Translator
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create your views here.
def translate_text_function(text):
    translator = Translator()
    translated = translator.translate(text, dest='en')  # 你也可以选择别的目标语言
    return translated.text
def export_pdf_function(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, text)
    c.showPage()
    c.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="export.pdf"'
    return response




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
                return redirect('/my_files/')  # 登录成功后跳转到主页
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


def login_first(request):
    return render(request, 'login_first.html')


def help_center(request):
    return render(request, 'help_center.html')


def text_classification(request):
    return render(request, 'text_classification.html')


def my_files(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # 自动识别文件属性并保存
            uploaded_file = form.save(commit=False)
            mime_type, _ = mimetypes.guess_type(uploaded_file.file.name)
            uploaded_file.attributes = mime_type or 'Unknown'
            uploaded_file.save()
            return redirect('my_files')  # 上传成功后重新加载页面
    else:
        form = FileUploadForm()

    # 搜索功能
    search_query = request.GET.get('search', '')

    # 排序功能
    sort_by = request.GET.get('sort_by', 'default')

    # 默认按上传时间排序
    files = UploadedFile.objects.all().order_by('-upload_date')

    if search_query:
        files = files.filter(name__icontains=search_query)

    if sort_by == 'name':
        files = files.order_by('name')
    elif sort_by == 'recent':
        files = files.order_by('-upload_date')
    else:
        files = files.order_by('-id')  # 默认排序为按ID排序

    context = {
        'form': form,
        'files': files,
        'search_query': search_query,
        'sort_by': sort_by,  # 传递排序选项到模板
    }

    return render(request, 'my_files.html', context)


def work_document(request):
    return render(request, 'work_document.html')


def learning_document(request):
    return render(request, 'learning_document.html')


def life_document(request):
    return render(request, 'life_document.html')


logger = logging.getLogger(__name__)


def text_recognition(request):
    form = FileUploadForm()
    uploaded_file = UploadedFile.objects.last()  # 只显示最后一次上传的文件
    ocr_text = None
    pdf_url = None

    if uploaded_file:
        pdf_url = uploaded_file.file.url
        logger.info(f"Processing file: {uploaded_file.file.path}")
        file_extension = os.path.splitext(uploaded_file.file.path)[1].lower()

        if file_extension == '.pdf':
            try:
                ocr_text = extract_text_from_pdf(uploaded_file.file.path)
                logger.info(f"OCR 处理成功，文件路径: {uploaded_file.file.path}")
            except Exception as e:
                logger.error(f"OCR 处理失败: {e}")
        else:
            logger.error(f"文件类型不支持: {file_extension}")

    context = {
        'form': form,
        'uploaded_file': uploaded_file,
        'ocr_text': ocr_text,
        'pdf_url': pdf_url
    }
    return render(request, 'text_recognition.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('file')
            if uploaded_file.content_type == 'application/pdf':
                form.save()
                logger.info(f"文件上传成功: {uploaded_file.name}")
            else:
                logger.error(f"非法文件类型上传: {uploaded_file.content_type}")
                return HttpResponse("仅支持 PDF 文件", status=400)
            return redirect(reverse('text_recognition'))
    return redirect(reverse('text_recognition'))


def delete_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    if os.path.exists(uploaded_file.file.path):
        os.remove(uploaded_file.file.path)
    uploaded_file.delete()
    return redirect(reverse('text_recognition'))


def generate_doc(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        doc = docx.Document()
        doc.add_paragraph(text)
        doc_path = os.path.join(settings.MEDIA_ROOT, 'download', 'recognized_text.docx')
        doc.save(doc_path)
        response = HttpResponse(open(doc_path, 'rb').read(),
                                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response['Content-Disposition'] = f'attachment; filename=recognized_text.docx'
        os.remove(doc_path)
        return response


def extract_text_from_pdf(pdf_path):
    start_time = time.time()  # 开始时间

    images = convert_from_path(pdf_path)
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img, lang='chi_sim')  # 使用中文语言包

    end_time = time.time()  # 结束时间
    logger.info(f"OCR处理时间: {end_time - start_time} 秒")  # 输出处理时间
    return text



def translate_text_view(request):
    if request.method == 'POST':
        text = request.POST['text']
        # 翻译逻辑
        translated_text = translate_text_function(text)
        return JsonResponse({'translated_text': translated_text})
    return HttpResponse(status=400)


def export_as_pdf_view(request):
    if request.method == 'POST':
        text = request.POST['text']
        # 导出PDF逻辑
        pdf_response = export_pdf_function(text)
        return pdf_response
    return HttpResponse(status=400)