from stark.service import v1
from crm import models
# from rbac import models
from django.shortcuts import HttpResponse,render,redirect
from django.conf.urls import url
from django.forms import ModelForm
from django.forms import fields
from django.utils.safestring import mark_safe
from django.urls import reverse

# 将models中的UserInfo类注册到【某个地方】
"""
_registry = {
    model.UserInfo: StarkConfig(model.UserInfo)
    model.Role: StarkConfig(model.Role)
}

for k,v in _registry.items():
    print(v.mcls)
    
/stark/app01/userinfo/      执行StarkConfig(models.UserInfo).changelist_view()
/stark/app01/userinfo/add   执行StarkConfig(models.UserInfo).add_view()

/stark/app01/role/      执行StarkConfig(models.Role).changelist_view()
/stark/app01/role/add   执行StarkConfig(models.Role).add_view()

_registry = {
    model.UserInfo: UserInfoConfig(model.UserInfo)
    model.Role: StarkConfig(model.Role)
    model.Group: StarkConfig(model.Group)
}
"""
class UserInfoModelForm(ModelForm):
    # xx = fields.CharField()
    class Meta:
        model = models.UserInfo
        fields = "__all__"

"""
stark/app01/userinfo/,              现找自己的changelist_view,没有再找父类
stark/app01/userinfo/add,           现找自己的add_view,没有再找父类
stark/app01/userinfo/1/change/,     现找自己的change_view,没有再找父类
stark/app01/userinfo/delete/,       现找自己的delete_view,没有再找父类
"""

# UserInfoConfig继承StarkConfig类所有东西，此处如果重新自定义了/stark/app01/userinfo/... 增删改查的话，结果为子类定义的结果（也可以理解父类的被子类覆盖）
# 定制页面列
class UserInfoConfig(v1.StarkConfig):
    # 定制页面表头，页面内容
    def xxxx(self,is_header=False,row=None):
        if is_header:
            return "复合行"
        return "%s-%s" %(row.username,row.email,)

    def display_gender(self,is_header=False,row=None):
        if is_header:
            return "性别"
        return row.get_gender_display()     #对象.django固定搭配

    def display_status(self,is_header=False,row=None):
        if is_header:
            return "学历"
        if row.status == 1:
            return "本科"
        if row.status == 2:
            return "专科"
        if row.status == 3:
            return "高中"
        else:
            return "初中"

    def display_dp(self,is_header=False,row=None):
        if is_header:
            return "部门"
        return row.depart.title

    # def display_role(self,is_header=False,row=None):
    #     if is_header:
    #         return "角色名称"
    #     return row.roles.title

    # 函数/字符串（字符串去数据库取,如userimfo类中去取dp外键数据，页面会显示DepartMent object对象,自定制display_dp可以让页面显示中文）
    # 还有编辑，删除和chekbox函数
    list_display = ['id','number', 'username', 'email','nickname',display_dp,display_gender,display_status,xxxx,]


    # 定制ModelForm,可以从自定义页面显示标签
    model_form_cls = UserInfoModelForm


    # userinfo不仅有增删改查，还新增了xxxxxx网页
    def extra_url(self):
        patterns = [
            url(r'^xxxxxx', self.xxxxxx),
        ]
        return patterns

    # 上面写了url,接下来写视图函数 url:http://127.0.0.1:8015/stark/app01/userinfo/xxxxxx
    def xxxxxx(self,request):
        return HttpResponse('xxxxxx')

    # def changelist_view(self, request):
    #     return render(request,'userinfo_list.html')


    # 关键字搜索功能
    # __contains模糊匹配（不加__contains为精确匹配，精确匹配时搜索与被所搜的字要一致才行）
    search_list = ['username__contains','email__contains']


    # 批量操作
    def multi_install(self,request):
        pk_list = request.POST.getlist('pk')
        print('装机')
        return HttpResponse('装机中...')

    def multi_molitor(self,request):
        pk_list = request.POST.getlist('pk')
        print('监控')

    # action_list = [multi_install,multi_molitor]
    action_list = [{'name':'批量装机','funcname': 'multi_install'},{'name':'批量添加到监控','funcname': "multi_molitor"}]


    # 组合搜索
    comb_filter = ['gender','depart','status']

class DeviceConfig(v1.StarkConfig):
    def display_device_status(self,is_header=False,row=None):
        if is_header:
            return "设备状态"
        return row.get_device_status_display()  # 对象.django固定搭配

    def display_use_status(self,is_header=False,row=None):
        if is_header:
            return "使用状态"
        return row.get_use_status_display()     #对象.django固定搭配

    # 列表页面
    list_display = ['id','device_name', 'device_class','device_group','device_course','device_ip','start_date','end_date',display_device_status,display_use_status,]

    # 组合搜索
    comb_filter = ['device_status', 'use_status',]

class DepartmentConfig(v1.StarkConfig):

    list_display = ['id','title','depart_code']

class ProductConfig(v1.StarkConfig):
    def display_workorder_status(self,is_header=False,row=None):
        if is_header:
            return "工单状态"
        return row.get_workorder_status_display()  # 对象.django固定搭配

    def display_dp(self,is_header=False,row=None):
        if is_header:
            return "部门"
        return row.depart.title

    # 列表展示
    list_display = ['id','material_code','material_name','product_type','unit','workorder_code','product_order','workorder_startdate',display_workorder_status,display_dp]

    # 关键字搜索
    search_list = ['material_code__contains', 'workorder_code__contains']

    # 组合搜索
    comb_filter = ['depart','workorder_status']

class ToolsConfig(v1.StarkConfig):
    def display_title(self,is_header=False,row=None):
        if is_header:
            return "仓库名称"
        return row.warehouse.title

    def display_dp(self,is_header=False,row=None):
        if is_header:
            return "部门"
        return row.depart.title

    # 列表展示
    list_display = ['id',display_title, 'material_code', 'material_name', 'tool_top', 'tool_butoom', 'diameter', 'unit',
                    'number',display_dp]

    # 关键字搜索
    search_list = ['material_code__contains', 'material_name__contains','tool_top__contains', 'tool_butoom__contains', 'diameter__contains']

    # 组合搜索
    # comb_filter = ['depart', 'warehouse']

class WarehouseConfig(v1.StarkConfig):
    list_display = ['id','title']

class WorkInProductConfig(v1.StarkConfig):
    def display_dp(self,is_header=False,row=None):
        if is_header:
            return "部门"
        return row.depart.title
    # 列表展示
    list_display = ['id',  'material_code', 'material_name', 'product_type', 'unit', 'early_balance','incoming_material',
                    'job_booking','wip','putinstorage','unputinstorage','good_products','bad_products',display_dp]

    # 关键字搜索
    search_list = ['material_code__contains', 'material_name__contains']

v1.site.register(models.UserInfo,UserInfoConfig)
v1.site.register(models.Device,DeviceConfig)
v1.site.register(models.Department,DepartmentConfig)
v1.site.register(models.Product,ProductConfig)
v1.site.register(models.Tools,ToolsConfig)
v1.site.register(models.Warehouse,WarehouseConfig)
v1.site.register(models.WorkInProduct,WorkInProductConfig)