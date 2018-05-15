import random

from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from app_for_homepage.models import MainWheel, MainNavigate,CarModel, \
    MainMustBuy, MainShop, MainShow, UserModel, Goods, FoodType, OrderModel, OrderGoodsModel


def verify_user(request):
    """验证用户当前注册的用户名是否存在"""
    if request.method == 'POST':
        value = request.POST.get('value')
        data = {
            'code': '200',
            'msg': '请求成功',
            'user': False
        }
        user = UserModel.objects.filter(username=value)
        if len(user) > 0:
            data['user'] = True

        return JsonResponse(data)


def regist(request):
    """
    :param request: 页面url请求
    :return: 返回注册页面
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        r = request.POST
        name = r['username']
        password = r['password']
        email = r['email']
        img = request.FILES.get('icon')

        UserModel.objects.create(
            username=name,
            password=password,
            email=email,
            icon=img
        )
        return HttpResponseRedirect('/axf/login/')


def login(request):
    """
    :param request: 页面url请求
    :return: 返回登录页面
    """
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        r = request.POST
        name = r['username']
        password = r['password']
        try:
            if UserModel.objects.get(username=name):
                if UserModel.objects.get(username=name).password == password:
                    all_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-*/.[]{}:;!'
                    ticket = 'TK+'
                    ticket += str(datetime.now())
                    for i in range(15):
                        ticket += random.choice(all_char)

                    user = UserModel.objects.get(username=name)
                    user.ticket = ticket
                    user.save()

                    response = HttpResponseRedirect('/axf/home/')
                    response.set_cookie('ticket', ticket, max_age=50000)

                    return response
                else:
                    return HttpResponse('密码错误')
        except Exception as e:
            print(e)
            return HttpResponse('用户不存在')


def logout(request):
    """
    退出登录
    :param request: 页面url请求
    :return: 返回登录页面
    """
    response = HttpResponseRedirect('/axf/home/')
    response.delete_cookie('ticket')
    return response


def home(request):
    """
    :param requeset: 页面url请求
    :return: 返回一个主页的html页面
    """
    data = MainWheel.objects.all()
    navigate = MainNavigate.objects.all()
    mustbuy = MainMustBuy.objects.all()
    shops = MainShop.objects.all()
    commidities = MainShow.objects.all()

    return render(request, 'home/home.html',
                  {'data': data, 'nav': navigate, 'mustbuy': mustbuy,
                   'shops': shops, 'commidities': commidities})


def mine(request):
    """
    :param request: 页面url请求
    :return: 返回个人页面
    """
    if request.method == 'GET':

        ticket = request.COOKIES.get('ticket', 0)
        # 判断用户是否登录
        if ticket:
            user = UserModel.objects.get(ticket=ticket)
            user_order_wait_pay = 0
            user_order_wait_goods = 0
            user_order_wait_evaluate = 0
            user_order_over = 0
            for order in user.ordermodel_set.all():
                if order.o_status == 0:
                    user_order_wait_pay += 1
                elif order.o_status == 1:
                    user_order_wait_goods += 1
                elif order.o_status == 2:
                    user_order_wait_evaluate += 1
                elif order.o_status == 10:
                    user_order_over += 1
            data = {
                'user': user,
                'wait_pay': user_order_wait_pay,
                'wait_goods': user_order_wait_goods,
                'wait_evaluate': user_order_wait_evaluate,
                'over': user_order_over
                }
        else:
            user = False
            data ={
                'user': user
            }
        return render(request, 'mine/mine.html', data)


def order(request):
    """
    订单查询
    :param reqeuset: 页面url
    :return: 返回订单页面
    """
    if request.method == 'GET':
        user = request.user

        if user and user.id:
            orders = OrderModel.objects.all()
            return render(request, 'order/order_list_all.html', {'orders': orders})
        else:
            return HttpResponseRedirect('/axf/login/')


def market(request):
    """传递参数"""
    return HttpResponseRedirect(reverse('axf:tms', args=('104749', '0', '0')))


def marketargvs(request, typeid, childcid, sid):
    """给页面传入三个参数"""
    if request.method == 'GET':

        # 获取商品的分类
        types = FoodType.objects.all().order_by('id')
        # 获取所有商品
        goods = Goods.objects.filter(category=typeid)
        if childcid != '0':
            goods = goods.filter(childcid=childcid)
        # 获取全部分类子类型
        childtypes = FoodType.objects.get(typeid=typeid)
        childtypes = childtypes.childtypenames.split('#')
        cs = []
        for childtype in childtypes:
            childtype = childtype.split(':')
            cs.append(childtype)
        childtypes = cs

        if sid:
            if sid == '0':
                pass
            elif sid == '1':
                goods = goods.order_by('productnum')
            elif sid == '2':
                goods = goods.order_by('-price')
            elif sid == '3':
                goods = goods.order_by('price')

        data = {'types': types,
                'goods': goods,
                'childtypes': childtypes,
                'typeid': int(typeid),
                'childcid': childcid,
                'sid': sid}

        return render(request, 'market/market.html', data)


def cart(request):
    """
    :param request: 页面url请求
    :return: 返回个人页面
    """
    if request.method == 'GET':
        ticket = request.COOKIES.get('ticket', 0)
        if not ticket:
            return HttpResponseRedirect('/axf/login/')
        user = UserModel.objects.get(ticket=ticket)
        carts = CarModel.objects.filter(user=user)

        return render(request, 'cart/cart.html', {'user': user, 'carts': carts})


def add_goods(request):
    """获取购物车信息"""

    if request.method == "POST":
        data = {
            'code': '200',
            'msg': '请求成功',
        }

        user = request.user
        if user and user.id:
            goods_id = request.POST.get('goods_id')

            user_carts = CarModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                user_carts.is_select = True
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CarModel.objects.create(
                    user=user,
                    goods_id=goods_id,
                    c_num=1
                )
                data['c_num'] = 1

            carts = CarModel.objects.filter(user=user)
            data['money'] = 0
            data['choose_all_status'] = True
            for cart in carts:
                if cart.is_select:
                    data['money'] += cart.c_num * cart.goods.price
                else:
                    data['choose_all_status'] = False

        return JsonResponse(data)


def sub_goods(request):

    if request.method == 'POST':
        data = {
            'code': '200',
            'msg': '请求成功'
        }
        user = request.user

        goods_id = request.POST.get('goods_id')
        if user and user.id:
            user_carts = CarModel.objects.filter(
                user=user, goods_id=goods_id).first()
            if user_carts:
                user_carts.is_select = True
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num

            carts = CarModel.objects.filter(user=user)
            data['money'] = 0
            data['choose_all_status'] = True
            for cart in carts:
                if cart.is_select:
                    data['money'] += cart.c_num * cart.goods.price
                else:
                    data['choose_all_status'] = False
        return JsonResponse(data)


def change_select(request):
    """异步加载购物车商品是否选中"""
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        user = request.user
        data = {
            'code': '200',
            'msg': '请求成功'
        }

        if user and user.id:
            cart = CarModel.objects.filter(goods_id=cart_id).filter(user_id=user.id).first()

            if cart.is_select:
                cart.is_select = False
                data['cart_id'] = cart.is_select
            else:
                cart.is_select = True
                data['cart_id'] = cart.is_select
            cart.save()

            carts = CarModel.objects.filter(user=user)
            data['money'] = 0
            data['change'] = True
            for cart in carts:
                if cart.is_select:
                    data['money'] += cart.c_num * cart.goods.price
                else:
                    data['change'] = False

        return JsonResponse(data)


def money(request):
    """计算购物车中选中商品总价"""

    if request.method == 'GET':

        data = {
            'code': '200',
            'msg': '请求成功'
        }
        user = request.user
        if user and user.id:
            carts = CarModel.objects.filter(user=user)
            all_money = 0
            data['status'] = True
            for cart in carts:
                if cart.is_select:
                    all_money += cart.c_num * cart.goods.price
                else:
                    data['status'] = False

            all_money = float('%.2f' % all_money)
            data['money'] = all_money

        return JsonResponse(data)


def choose_all(request):
    """全选按钮控制函数"""
    if request.method == 'POST':
        data = {
            'code': '200',
            'msg': '请求成功'
        }
        status = request.POST.get('status')
        data['status'] = True if status == '√' else False
        user = request.user

        # 判断是否登录
        if user and user.id:
            carts = CarModel.objects.filter(user=user)
            data['money'] = 0
            flags = []
            for cart in carts:
                if status == '√':
                    cart.is_select = 0
                else:
                    cart.is_select = 1
                cart.save()
                flags.append(cart.goods_id)

                if cart.is_select:
                    data['money'] += cart.c_num * cart.goods.price

            data['status'] = not data['status']
            data['flags'] = flags
        return JsonResponse(data)


def user_generate_order(request):
    """用户下单了逻辑处理"""
    if request.method == 'GET':
        # 先查询is_select 为true的购物车数据
        user = request.user
        carts_goods = CarModel.objects.filter(is_select=True).filter(user=user)

        if len(carts_goods) > 0:
            # 创建订单 ,0未付款 1已付款

            order = OrderModel.objects.create(user=user, o_num=0, o_status=0)

            # 创建订单详情
            for cart in carts_goods:
                OrderGoodsModel.objects.create(goods=cart.goods, order=order,
                                               goods_num=cart.c_num)
                order.o_num += cart.c_num
            order.save()
            # 删除购物车中的数据
            carts_goods.delete()

            data = {
                'order': order,
            }
            return order_info(request, data)
        else:
            return HttpResponseRedirect('/axf/cart/')


def order_info(request, data):
    """处理单个未付款订单"""
    return render(request, 'order/order_info.html', data)


def wait_pay(request):
    """在个人中心所有待付款订单处理"""
    if request.method == 'GET':
        order_id = request.GET.get('order_id', 0)
        if order_id:
            order = OrderModel.objects.get(id=order_id)
            data = {'order': order}
            return order_info(request, data)

        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user)
            return render(request, 'order/order_list_wait_pay.html', {'orders': orders})
        else:
            return HttpResponseRedirect('/axf/login/')


def wait_goods(request):
    """个人中心所有待收货订单处理"""
    if request.method == 'GET':
        user = request.user
        # 判断用户是否登录，没有登录跳转登录页面
        if user and user.id:
            orders = OrderModel.objects.filter(user=user).filter(o_status=1)
            return render(request, 'order/order_list_payed.html', {'orders': orders})
        else:
            return HttpResponseRedirect('/axf/login/')


def get_goods(request):
    """未收货订单的确认收货"""
    if request.method == 'GET':
        user = request.user
        order_id = request.GET.get('order_id')

        order = OrderModel.objects.get(id=order_id)
        order.o_status = 2
        order.save()

        return HttpResponseRedirect('/axf/mine/')


def pay_money(request):
    """用户订单的付款处理"""

    if request.method == 'GET':
        user = request.user
        order_id = request.GET.get('order_id')
        order = OrderModel.objects.get(id=order_id)
        order.o_status = 1
        order.save()

        return HttpResponseRedirect('/axf/mine/')


def cart_buy(request):
    """
    实现购物车与闪购已经购买商品页面一致
    """
    if request.method == 'GET':
        user = request.user

        data = {
            'code': '200',
            'msg': '请求成功',
        }
        infos = []
        cart_goods = CarModel.objects.filter(user=user)
        for good in cart_goods:
            infos.append((good.goods_id, good.c_num))

        data['infos'] = infos

        return JsonResponse(data)






