from django.db import models


class Main(models.Model):
    """
    图片数据的父类表
    img： 分类图片
    name： 分类名称
    trackid： 通用id
    """
    img = models.CharField(max_length=256)
    name = models.CharField(max_length=128)
    trackid = models.CharField(max_length=16)

    class Meta:
        """
        抽象类主要用来继承
        """
        abstract = True


class MainWheel(Main):
    """
    首页的轮播横幅广告图片数据表，继承 Main
    """
    class Meta:
        db_table = 'axf_banner'


class MainNavigate(Main):
    """
    首页导航模块图片数据表，继承 Main
    """
    class Meta:
        db_table = 'axf_navigate'


class MainMustBuy(Main):
    """
    首页必购模块的图片数据表，继承 Main
    """
    class Meta:
        db_table = 'axf_must_buy'


class MainShop(Main):
    """
    首页商店表
    """
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    """
    主页主要展示的商品的图片数据表，继承 Main
    img*： 图片数据
    longname*： 图片名称
    price*： 优惠价格
    marketprice*： 原始价格
    """
    categoryid = models.CharField(max_length=16, null=True)
    brandname = models.CharField(max_length=128, null=True)

    img1 = models.CharField(max_length=256)

    childcid1 = models.CharField(max_length=16, null=True)
    productid1 = models.CharField(max_length=16, null=True)

    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=256)

    childcid2 = models.CharField(max_length=16, null=True)
    productid2 = models.CharField(max_length=16, null=True)

    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=256)

    childcid3 = models.CharField(max_length=16, null=True)
    productid3 = models.CharField(max_length=16, null=True)

    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    """
    闪购页面的食物分类表
    typeid： 食品分类的唯一id
    typename： 食品分类名字
    """
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=128)
    childtypenames = models.CharField(max_length=256)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    """
    所有商品表
    productid： 商品编号
    productimg： 商品图片
    productname： 商品名字
    productlongname： 商品规格
    isxf：
    pmdesc：
    specifics： 详细规格
    price： 折后价格
    marketprice： 原价
    categoryid： 当前分类 id,关联到食物类型表
    childcid： 子分类 id
    childcidname： 子分类id 名字
    dealerid：
    storenums： 排序
    productnum： 销量排序
    """
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=256)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=256)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=128)
    specifics = models.CharField(max_length=128)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    category = models.ForeignKey(FoodType)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=128)
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):
    """
    用户表
    username： 用户名
    password： 密码
    email： 邮箱
    sex： 性别采用布尔值保存，默认为0。0表示女 1表示男
    icon： 用户头像
    is_delete： 用户数据不实际删除，
    """
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)

    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')
    is_delete = models.BooleanField(default=False)
    ticket = models.CharField(max_length=64)

    class Meta:
        db_table = 'axf_users'


class CarModel(models.Model):
    """
    购物车数据表
    user： 关联到用户表
    goods： 关联到商品表
    c_num： 表示商品数量
    is_selet： 默认为True，表示是否选中商品
    """
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    """
    订单表
    user: 关联用户表
    o_num: 订单的数量
    o_status: 0表示下单，但未付款； 1已付款未发货； 2已付款已发货
    o_create：订单创建的时间
    """
    user = models.ForeignKey(UserModel)
    o_num = models.CharField(max_length=64)
    o_status = models.IntegerField(default=0)
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    """
    订单详细信息表
    goods：关联商品表，展示商品的详细信息
    order：关联订单，表示哪一张订单
    goods_num：商品的个数
    """
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_order_goods'







