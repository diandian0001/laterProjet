import json
import os
import uuid
import re

from django.core.paginator import Paginator
from django.db.transaction import atomic
from django.shortcuts import render, HttpResponse, redirect


# Create your views here.

from redis import Redis
from laterproject import settings
from .models import Banner
from until.send_msg import YunPian
from django.views.decorators.csrf import csrf_exempt


# 全局变量
REDIS = Redis()


@csrf_exempt
def index(request):
    """
    渲染首页
    :param request:
    :return:
    """
    name1 = request.POST.get('name')
    # name2 = request.session.get('username')
    # print(name1, name2)
    # if name1 == name2:
    #     print(1111)
    return render(request, 'index.html', {'username': name1})
    # return redirect('index:login')


def login(request):
    # 登录页面
    return render(request, 'login.html')


@csrf_exempt
def get_code(request):
    # 发送验证码
    mobile = request.POST.get('mobile')
    reg = re.compile(r'^1[3-9]\d{9}')    # 后端对手机号进行验证
    # print(reg.match(mobile))
    if reg.match(mobile):
        yunpian = YunPian(settings.APIKEY)
        code, result = yunpian.send_msg(mobile), 1
        REDIS.set(mobile, code, ex=60)
    else:
        result = 0
    return HttpResponse(result)


@csrf_exempt
def test_captcha(request):
    # 判断用户输入的验证码是否一致
    mobile = request.POST.get('mobile')
    name = request.POST.get('name')
    code = request.POST.get('code')
    res = REDIS.get(mobile)
    if res is None:
        res = b'0'
    request.session['username'] = name
    return HttpResponse(name if res.decode() == code else 0)


def get_uuid(filename):
    # 生成唯一的文件名
    img_id = str(uuid.uuid4())
    extend = os.path.splitext(filename)[1]
    return img_id + extend


@csrf_exempt
def save(request):
    title = request.POST.get('title')
    status = request.POST.get('status')
    file = request.FILES.get('pic')
    file.name = get_uuid(file.name)
    file_path = f'/static/imgs/{file.name}'
    # print(title, status, file, type(file.name))
    result = 1
    with atomic():
        try:
            Banner.objects.create(title=title, status=status, pic=file, path=file_path)
        except:
            result = 0
        return HttpResponse(result)


def get_dict(param: Banner):
    if isinstance(param, Banner):
        # print('get_dict', param)
        return {
            'id': param.id,
            'title': param.title,
            'status': param.status,
            'pic': str(param.pic),
            'time': str(param.add_time).split(".")[0],
            'path': param.path
        }


def query(request):
    page_num = int(request.GET.get('page'))
    rows = int(request.GET.get('rows'))
    pics = Banner.objects.all()
    pagtor = Paginator(pics, per_page=rows)
    page = pagtor.page(page_num)
    data = {
        'page': page_num,
        'total': pagtor.num_pages,
        'records': pagtor.count,
        'rows': list(page.object_list),
    }
    json_str = json.dumps(data, skipkeys=True, ensure_ascii=False, default=get_dict)
    # print(json_str)
    return HttpResponse(json_str)


@csrf_exempt
def update(request):
    # 更新数据
    pic_id = request.POST.get("id")
    title = request.POST.get("title")
    status = request.POST.get("status")
    with atomic():
        try:
            pic = Banner.objects.get(id=pic_id)
            pic.title = title
            pic.status = status
            pic.save()
            ret = 1
        except:
            ret = 0
        return HttpResponse(ret)


@csrf_exempt
def delete_data(request):
    # 删除数据
    # print(request.POST)
    pic_id = request.POST.get("id")
    with atomic():
        try:
            Banner.objects.get(id=pic_id).delete()
            ret = 1
        except:
            ret = 0
        return HttpResponse(ret)



