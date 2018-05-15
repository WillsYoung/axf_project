from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from app_for_homepage.models import UserModel


class AuthMiddlewere(MiddlewareMixin):
    """
    中间件设置，统一验证登录的位置
    return none 或者不写return表示验证成功进入下一步
    """
    def process_request(self, request):
        if request.path in ['/axf/login/', '/axf/regist/', '/axf/ttmarket/',
                            '/axf/ttmarket/(\d+)/(\d+)/(\d+)/', '/axf/home/', '/axf/mine/']:
            return None

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect('/axf/login/')

        user = UserModel.objects.get(ticket=ticket)
        if not user:
            return HttpResponseRedirect('/axf/login')

        request.user = user


class AuthMiddleware(MiddlewareMixin):
    """
    中间件设置，统一验证登录的位置
    return none 或者不写return表示验证成功进入下一步
    """
    def process_request(self, request):

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return None
        # 判断用户是否登录，cookie是否有效这里注意排除别的网站的登录cookie的干扰
        if 'TK+' in ticket:
            user = UserModel.objects.filter(ticket=ticket)
            request.user = user[0]
        else:
            return None



