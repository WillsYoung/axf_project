from django.conf.urls import url

from app_for_homepage import views


urlpatterns = [
    # 主页
    url(r'^home/', views.home),

    # 注册，登录，登出
    url(r'^regist/', views.regist),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),

    # 个人中心
    url(r'^mine/', views.mine),

    # 购物车
    url(r'^cart/', views.cart),

    # 订单
    url(r'^order/', views.order),

    # 另一种办法写 market 页面
    url(r'^ttmarket/$', views.market, name='tm'),
    url(r'^ttmarket/(\d+)/(\d+)/(\d+)/', views.marketargvs, name='tms'),

    # 添加商品到购物车
    url(r'^addgoods/', views.add_goods, name='add'),
    url(r'^subgoods/', views.sub_goods, name='sub'),

    # 修改购物车商品选择
    url(r'^change_cart_select/', views.change_select),

    # 计算购物车商品总价
    url(r'^money/', views.money),

    # 全选按钮
    url(r'^choose_all/', views.choose_all),

    # 下单处理
    url(r'^generate_order/', views.user_generate_order, name='u_g_o'),

    # 待付款的订单处理
    url(r'^wait_pay/', views.wait_pay),

    # 付款操作
    url(r'^pay_money/', views.pay_money),

    # 未收货订单处理
    url(r'^wait_goods/', views.wait_goods),

    # 个人中心未收货订单的确认收货
    url(r'^get_goods/', views.get_goods),

    # 用户注册信息判断
    url(r'^verify_user', views.verify_user),

    # 实现购物车与闪购已经购买商品页面保持一致方法
    url(r'^cart_buy', views.cart_buy)


]