from rbac import models as rbac_model
from django.db import models

class Department(models.Model):
    """
    部门表
    市场部
    销售
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)
    depart_code = models.IntegerField(verbose_name='部门编码')

    def __str__(self):
        return self.title

class UserInfo(rbac_model.User):
    """
    用户表
    """
    # username = models.CharField(verbose_name='用户名', max_length=32)
    # password = models.CharField(verbose_name='密码', max_length=64)
    # roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role)
    # session_key = models.CharField(verbose_name='当前登录用户的session_key', max_length=40, null=True, blank=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    number = models.IntegerField(verbose_name='工号')
    email = models.CharField(max_length=32)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    status_choice = (
        (1, '本科'),
        (2, '专科'),
        (3, '高中'),
        (4, '初中')
    )
    status = models.IntegerField(verbose_name='学历', choices=status_choice, default=1)
    depart = models.ForeignKey(verbose_name='部门', to="Department", default=1)

class Device(models.Model):
    device_name = models.CharField(verbose_name='设备名称', max_length=32)
    device_class = models.CharField(verbose_name='设备类别', max_length=32)
    device_group = models.CharField(verbose_name='设备组', max_length=32)
    device_course = models.CharField(verbose_name='品牌', max_length=32)
    device_ip = models.GenericIPAddressField(verbose_name='ip地址', protocol='both')
    start_date = models.DateField(verbose_name='启用时间',null=True, blank=True)
    end_date= models.DateField(verbose_name='报废时间', null=True, blank=True)
    device_status_choices =[
        (1, '开机'),
        (2, '待料'),
        (3, '报警'),
        (4, '待维修'),
    ]
    device_status = models.IntegerField(verbose_name='设备状态',null=True, blank=True,choices=device_status_choices)
    use_status_choices = [
        (1, 'ON'),
        (2, 'OFF'),
    ]
    use_status= models.IntegerField(verbose_name='使用状态', null=True, blank=True,choices=use_status_choices)

class Product(models.Model):
    material_code = models.IntegerField(verbose_name='物料编码')
    material_name= models.CharField(verbose_name='物料名称', max_length=32)
    product_type = models.CharField(verbose_name='规格型号', max_length=32)
    unit = models.CharField(verbose_name='单位', max_length=32)
    workorder_code = models.IntegerField(verbose_name='工单编码')
    product_order = models.IntegerField(verbose_name='生产订单数')
    workorder_startdate = models.DateField(verbose_name='工单日期' ,null=True, blank=True)
    workorder_status_choices =[
        (1, '开立'),
        (2, '关闭'),
    ]
    workorder_status = models.IntegerField(verbose_name='工单状态',null=True,blank=True,choices=workorder_status_choices)
    depart = models.ForeignKey(verbose_name='部门名称', to='Department',default=1)

    def __str__(self):
        return self.material_name

class Warehouse(models.Model):
    # 仓库
    title = models.CharField(verbose_name='仓库名称', max_length=32)
    def __str__(self):
        return self.title

class Tools(models.Model):
    warehouse = models.ForeignKey(verbose_name='仓库名称',to=Warehouse,default=3)
    material_code = models.IntegerField(verbose_name='物料编码')
    material_name = models.CharField(verbose_name='物料名称',max_length=32)
    tool_top = models.IntegerField(verbose_name='刀柄长/mm')
    tool_butoom  = models.IntegerField(verbose_name='刀刃长/mm')
    diameter = models.IntegerField(verbose_name='直径/mm')
    unit = models.CharField(verbose_name='单位', max_length=32)
    number = models.IntegerField(verbose_name='使用寿命')
    depart= models.ForeignKey(verbose_name='物料名称', to=Department, default=1)

class WorkInProduct(models.Model):
    material_code = models.IntegerField(verbose_name='物料编码')
    material_name= models.CharField(verbose_name='物料名称', max_length=32)
    product_type = models.CharField(verbose_name='规格型号', max_length=32)
    unit = models.CharField(verbose_name='单位', max_length=32)
    early_balance = models.IntegerField(verbose_name='前期结存')
    incoming_material = models.IntegerField(verbose_name='来料数量')
    job_booking = models.IntegerField(verbose_name='报工数量')
    wip = models.IntegerField(verbose_name='生产在制数量')
    putinstorage = models.IntegerField(verbose_name='入库数')
    unputinstorage = models.IntegerField(verbose_name='未入库数')
    good_products = models.IntegerField(verbose_name='良品数')
    bad_products = models.IntegerField(verbose_name='不良品数')
    depart = models.ForeignKey(verbose_name='部门名称', to='Department',default=1)