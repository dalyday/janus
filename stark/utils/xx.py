from types import FunctionType

def header_list(config):
    header_list = []
    # ['id', 'name', 'email',display_edit,display_del]
    # header_list.extend(self.list_display)
    # 反向查找字段 --> verbose_name属性
    from types import FunctionType
    for n in config.get_list_display():
        if isinstance(n, FunctionType):
            # 执行list_display中的函数
            val = n(config, is_header=True)
        else:
            val = config.mcls._meta.get_field(n).verbose_name
        # print(self.mcls)
        header_list.append(val)

body_list = []


