from django.shortcuts import HttpResponse,render,redirect
from django.conf.urls import url
from django.urls import reverse
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from types import FunctionType
from stark.utils.page import Pagination
from crm import models

"""
迭代器：有next方法
生成器：yield就是生成器；有next方法； -> 也是一种迭代器
可迭代对象：类中有__iter__方法且该方法返回一个 迭代器
"""
# 1. 如果一个对象是，是可迭代对象就可以被for循环
# 2. 如何让对象变成可迭代对象？
import copy
class FilterRow(object):
    def __init__(self,queryset,name,request_get,changelist_url,is_choice=False):
        """
        :param queryset: queryset类型
        :param name:  字段名称
        :param request_get:  get请求传过来参数 gender=1&dp=2&status=1
        :param changelist_url:  当前列表页面url
        """
        self.queryset = queryset
        self.is_choice = is_choice
        self.name = name
        self.changelist_url = changelist_url
        self.params = copy.deepcopy(request_get)
        self.params._mutable = True

    def __iter__(self):
        # self.params, QueryDict,   urlencode => gender=1&dp=2&status=1
        from django.http import QueryDict
        if self.name in self.params:
            oldval = self.params.get(self.name)
            # print(oldval)
            self.params.pop(self.name)  #['2']
            yield mark_safe("<a href='{0}?{1}'>全部</a>".format(self.changelist_url, self.params.urlencode()))
        else:
            oldval = None
            yield mark_safe("<a class='active' href='{0}?{1}'>全部</a>".format(self.changelist_url,self.params.urlencode()))

        for obj in self.queryset:
            # print(self.queryset)
            if self.is_choice:
                # obj = ((1, '男'), (2, '女'))
                nid = str(obj[0])
                text = obj[1]
            else:
                nid = str(obj.pk)
                text = str(obj)
            self.params[self.name] = nid #其他的不变，只改变自己

            # print(self.name,oldval,nid)
            if oldval == nid:
                yield mark_safe("<a class='active' href='{0}?{1}'>{2}</a>".format(self.changelist_url,self.params.urlencode(),text,))
            else:
                yield mark_safe( "<a href='{0}?{1}'>{2}</a>".format(self.changelist_url, self.params.urlencode(), text, ))


class ChangeList(object):
    """
    同于对列表页面的功能做拆分
    """
    def __init__(self,config,result_list,request):
        """
        :param config: 处理每个表增删改查功能的对象
        :param result_list:从数据库查询到的数据
        """
        self.config = config
        self.request = request

        self.search_list = config.search_list
        # 默认为空
        self.search_value = request.GET.get('key','')

        self.action_list = config.action_list
        self.comb_filter = config.comb_filter

        # 分页组件
        total_count = result_list.count()
        page_obj = Pagination(request.GET.get('page'), total_count, request.path_info,request.GET)

        if result_list:
            self.result_list = result_list[page_obj.start():page_obj.end()]
        else:
            self.result_list = result_list
        self.page_obj = page_obj

    def header_list(self):
        """
        处理页面表头的内容
        :return:
        """
        result = []
        # ['id', 'name', 'email',display_edit,display_del]
        # header_list.extend(self.list_display)
        # 反向查找字段 --> verbose_name属性
        for n in self.config.get_list_display():
            if isinstance(n, FunctionType):
                # 执行list_display中的函数
                val = n(self.config, is_header=True)
            else:
                val = self.config.mcls._meta.get_field(n).verbose_name
            # print(self.mcls)
            result.append(val)
        return result

    def body_list(self):
        """
        处理表内容
        :return:
        """
        result = []
        # body_list = [
        #     ['1','刘成彪','liuchengbaio@qq.com'],
        #     ['2','曲令涛','qulingtao@qq.com'],
        # ]
        """
        result_list=
        [
            obj,
            obj,
            obj,
        ]
        ['id', 'name', 'email']
        """
        for row in self.result_list:
            # print(row.id,row.name,row.email)
            # print(row)
            temp = []
            for n in self.config.get_list_display():
                if isinstance(n, FunctionType):
                    val = n(self.config, row=row)
                else:
                    val = getattr(row, n)
                temp.append(val)
                # print(val)
            result.append(temp)
        return result
        # print(body_list)

    def add_url(self):
        """
        处理添加按钮的URL
        :return:
        """
        app_model_name = ( self.config.mcls._meta.app_label,  self.config.mcls._meta.model_name,)
        name = "stark:%s_%s_add" % app_model_name
        add_url = reverse(name)
        return add_url

    def show_comb_search(self):
        """
        组合搜索
        :return:
        """
        # self.comb_filter # ['gender','status','dp']
        # 'gender',找到类中的gender字段对象，并将其对象的choice获取
        # 'status',找到类中的status字段对象，并将其对象的choice获取
        # dp',找到类中的dp字段对象，并将其关联的表中的所有数据获取到

        from django.db.models.fields.related import ForeignKey
        # Foo(models.Group.objects.all()),
        # Foo(models.Role.objects.all()),
        # Foo(models.UserInfo.objects.all()),
        for name in self.comb_filter:
            _field = self.config.mcls._meta.get_field(name)
            # print(_field,type(_field))
            changelist_url = self.config.get_changelist_url()
            if type(_field) == ForeignKey:
                # 跨表找数据
                yield FilterRow(_field.rel.to.objects.all(),name,self.request.GET,changelist_url)
            else:
                # 多选择(男女） name为数据库字段名称
                yield FilterRow(_field.choices,name,self.request.GET,changelist_url,is_choice=True)


class StarkConfig(object):
    """
    用于封装 单独数据库操作类
    """
    def display_chekbox(self,is_header=False,row=None):
        if is_header:
            return "选择"
        return mark_safe("<input type='checkbox' name='pk' value='%s' />" %(row.id,))

    def display_edit(self,is_header=False,row=None):
        if is_header:
            return "编辑"
        app_model_name = (self.mcls._meta.app_label, self.mcls._meta.model_name,)
        name = "stark:%s_%s_change" % app_model_name
        url_path = reverse(name, args=(row.id,))
        return mark_safe("<a href='%s'>编辑</a>" % (url_path,))

    def display_del(self,is_header=False,row=None):
        if is_header:
            return "删除"
        app_model_name = (self.mcls._meta.app_label, self.mcls._meta.model_name,)
        name = "stark:%s_%s_delete" % app_model_name
        url_path = reverse(name, args=(row.id,))
        return mark_safe("<a href='%s'>删除</a>" %(url_path,))

    list_display = []
    def get_list_display(self):
        result = []
        # ['id', 'name', 'email']
        if self.list_display:
            result.extend(self.list_display)
            result.insert(0,StarkConfig.display_chekbox)
            result.append(StarkConfig.display_edit)
            result.append(StarkConfig.display_del)
            return result

    model_form_cls = None

    def get_model_form_cls(self):
        """
        如果类中定义了 model_form_cls,则使用，否则创建TempModelForm
        :return:
        """
        if self.model_form_cls:
            return self.model_form_cls

        class TempModelForm(ModelForm):
            class Meta:
                model = self.mcls
                fields = "__all__"
        return TempModelForm

    # 关键字搜索功能
    search_list = []

    # 批量操作
    action_list = []


    # 组合搜索
    comb_filter = []

    def __init__(self, mcls):
        self.mcls = mcls

    # 增删改查
    @property
    def urls(self):
        # self = StarkConfig(models.UserInfo) # obj.mcls = models.UserInfo 相当于self.mcls = models.UserInfo = /app01/userinfo/
        # StarkConfig(models.Role), # obj.mcls = models.Role
        app_model_name =(self.mcls._meta.app_label,self.mcls._meta.model_name,)
        patterns = [
            url(r'^$', self.changelist_view,name='%s_%s_changelist' %app_model_name),
            url(r'^add/$', self.add_view,name='%s_%s_add' %app_model_name),
            url(r'^(\d+)/change/$', self.changet_view,name='%s_%s_change' %app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view,name='%s_%s_delete' %app_model_name),
        ]
        patterns.extend(self.extra_url())
        return patterns

    ##################反向生成url##########################
    def get_edit_url(self,pk):
        # /stark/app01/userinfo/1/change/
        # /stark/app02/userinfo/1/change/
        app_model_name = (self.mcls._meta.app_label, self.mcls._meta.model_name,)
        name ="stark:%s_%s_change" %app_model_name
        url_path = reverse(name,args=(pk,))
        return url_path

    def get_delede_url(self,pk):
        # /stark/app01/userinfo/1/delete/
        # /stark/app02/userinfo/1/delete/
        app_model_name = (self.mcls._meta.app_label, self.mcls._meta.model_name,)
        name ="stark:%s_%s_delete" %app_model_name
        url_path = reverse(name,args=(pk,))
        return url_path

    def get_changelist_url(self):
        # /stark/app01/userinfo/
        # /stark/app02/userinfo/
        app_model_name = (self.mcls._meta.app_label, self.mcls._meta.model_name,)
        name ="stark:%s_%s_changelist" %app_model_name
        url_path = reverse(name)
        return url_path

    ##################反向生成url##########################

    def extra_url(self):
        """
        钩子函数
        :return:
        """
        return []

    def multi_install(self,request):
        pk_list = request.POST.getlist('pk')
        print('装机')
        return HttpResponse('装机中...')

    def multi_molitor(self,request):
        pk_list = request.POST.getlist('pk')
        print('监控')

    def get_key_search_condtion(self,request):
        """
        关键字搜索功能
        :param request:
        :return:
        """
        from django.db.models import Q
        search_list = ['username', 'email', 'gender', ]
        key = request.GET.get('key')  # 小红
        con = Q()  # 实例化对象
        con.connector = 'OR'
        if key:
            for name in self.search_list:
                con.children.append((name, key,))
        return con

    def get_comb_filter_condition(self,request):
        """
        组合搜索
        :param request:
        :return:
        """
        # comb_filter = ['gender', 'status', 'dp']
        # gender=1&status=2&dp=1
        comb_condition = {}
        for name in self.comb_filter:
            val = request.GET.get(name)
            if not val:
                continue
            comb_condition[name] = val
            # print(name, val)
        return comb_condition

    def changelist_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        # self.action_list #自己，action_list = [multi_install，multi_molito] 基类 attion_list = []

        if request.method == "POST":
            action = request.POST.get('xxxx')  # multi_install，multi_molito
            func_name = getattr(self,action,None)  # 去self取action
            if func_name:
                response = func_name(request)
                if response:
                    return response

        result_list = self.mcls.objects.filter(self.get_key_search_condtion(request)).filter(**self.get_comb_filter_condition(request))
        # self.comb_filter # ['gender','status','dp']
        # self 要么指StarkConfig，UserInfoConfig的对象
        cl = ChangeList(self,result_list,request)
        return render(request, 'stark/changelist.html', {'cl':cl})

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """
        # self.mcls # models.UserInfo
        model_form_class  = self.get_model_form_cls()
        if request.method == "GET":
            form = model_form_class()
            return render(request, "stark/add_view.html", {'form':form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                # 跳转到列表页面
                app_model_name = (self.mcls._meta.app_label, self.mcls._meta.model_name,)
                name = "stark:%s_%s_changelist" % app_model_name
                list_url = reverse(name)
                return redirect(list_url)
            return render(request, "stark/add_view.html", {'form': form})

    def changet_view(self, request, nid):
        """
        编辑页面
        :param request:
        :param nid:
        :return:
        """
        obj = self.mcls.objects.filter(pk=nid).first()
        if not obj:
            return HttpResponse('别闹，不存在')

        model_form_cls = self.get_model_form_cls()
        if request.method == "GET":
            form = model_form_cls(instance=obj)
            return render(request, 'stark/change_view.html', {'form':form})
        else:
            form = model_form_cls(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_changelist_url())
            return render(request, 'stark/change_view.html', {'form': form})

    def delete_view(self, request, nid):
        self.mcls.objects.filter(id=nid).delete()
        path = self.get_changelist_url()
        return redirect(path)

class StarkSite(object):
    """
       用于封装所有的 数据库操作类
    """
    def __init__(self):
        self._registry = {}

    def register(self,model_class,config_cls=None):
        if not config_cls:
            config_cls = StarkConfig
        self._registry[model_class] = config_cls(model_class)
        # print(self._registry)

    @property
    def urls(self):
        from django.conf.urls import url
        pts = [
            url(r'^login/',self.login),
        ]
        """
        _registry = {
            models.UserInfo: StarkConfig(models.UserInfo),  # UserInfo:对象
            models.Role: StarkConfig(models.Role),  # Role:对象
        }
        
        # /admin//app01/userinfo/           查看列表页面
        # /admin/app01/userinfo/add/        添加页面
        # /admin/app01/userinfo/1/change/   修改页面
        # /admin/app01/userinfo/1/delete/   删除页面
               
        /stark/   ->  ([
                        /login/
                        /app01/userinfo/  --> ([
                                                    /                    查看列表
                                                    add/                 添加
                                                    (\d+)/change/        修改
                                                    (\d+)/delete/        删除
                                                ])
                        /app01/role/
                                            --> ([
                                                    /                   查看列表
                                                    add/                添加
                                                    (\d+)/change/        修改
                                                    (\d+)/delete/        删除
                                                ])
                    ])

        """
        for model_class,config_obj in self._registry.items():
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            temp = url(r'^%s/%s/' %(app_label,model_name),(config_obj.urls,None,None))
            # app_label,model_name  打印结果 app01 userinfo
            # (config_obj.urls,None,None)是再一次分发，原([],None,None)[]可以是函数或者方法，返回的时候是列表，列表可以写增删改查
            pts.append(temp)

        return pts,None,"stark"

    def login(self,request):
        return HttpResponse('登录界面')

site = StarkSite()
