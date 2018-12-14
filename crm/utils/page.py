"""
    分页组件：
        视图函数：
            from utils.page import Pagination
            from django.utils.safestring import mark_safe
            def host(request):
                #创建数据库：
                # for i in range(200):
                #     dic = { 'hostname':'c%s'%(i,),'ip':'1.1.1.1','port':'500'}
                #     models.Host.objects.create(**dic)
                # return HttpResponse('创建成功')

                # 数据总条数
                total_count = models.Host.objects.count()

                # 当前页
                # page_obj = Pagination(request.GET.get('page'),total_count,'/host/')
                # 三个参数（当前页，数据总个数，request.path_info URL 部分被分成脚本前缀部分和路径信息部分）
                page_obj = Pagination(request.GET.get('page'), total_count, request.path_info)

                # 第一页[0:10]  第二页[10:20]  第三页[20:30]
                # 下面的page_obj.start()如果想去掉括号，page.py文件函数def start(self):前面加个@property即可
                host_list = models.Host.objects.all()[page_obj.start():page_obj.end()]

                #方法一：
                # page_html = page_obj.page_html()
                # return render(request, 'host.html',{'host_list': host_list, 'page_html': mark_safe(page_html)})
                #方法二：
                return render(request, 'host.html', {'host_list': host_list, 'page_html': mark_safe(page_obj.page_html())})
        HTML;
            <style>
                .page a{                            /* a标签 */
                    display: inline-block;
                    padding: 2px 5px;
                    margin: 0px 3px;              /* 边距 */
                    border: 1px solid #9aafe5;   /* 边框*/
                    color: #333;
                }

                .page a.active{
                    background-color: #030217;
                    color: white;
                }
            </style>

            <div class="page" >
                {{ page_html }}
            </div>

"""
from django.utils.safestring import mark_safe
class Pagination(object):
    def __init__(self,current_page,total_count,base_url,per_page_count=10,max_page_num=7):
        """

        :param current_page: 用户请求的当前页
        :param per_page_count:每页显示的数据条数
        :param total_count:数据库中查询的数据总条数
        :param max_page_num:页面上最多的显示的页码
        """
        #总页数
        total_page_count, div = divmod(total_count, per_page_count)
        if div:
            total_page_count += 1

        #对当前页进行处理，当前页>1与大于总页码数
        self.total_page_count = total_page_count
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page > total_page_count:
            current_page = total_page_count

        self.current_page = current_page
        self.per_page_count = per_page_count
        self.base_url = base_url
        self.total_count = total_count
        self.max_page_num = max_page_num
        self.half_max_page_num = int(max_page_num/2)


    # 数据库切片的索引
    def start(self):
        return (self.current_page - 1) * self.per_page_count


    def end(self):
        return self.current_page * self.per_page_count


    # 页码
    def page_html(self):
        page_html_list = []
        # 上一页
        if self.current_page <= 1:
            prev = "<a href='#'>上一页</a>"
        else:
            prev = "<a href='%s?page=%s'>上一页</a>" % (self.base_url,self.current_page - 1,)
        page_html_list.append(prev)

        # 页面上最大显示页码个数
        max_page_num = 7
        half_max_page_num = int(max_page_num / 2)

        # 如果总页数小于7页
        if self.total_page_count <= max_page_num:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 起始页/结束页,数据比较多总页数已经超过7页
            # 如果当前页<= 3时(half_max_page_num),显示1:7
            if self.current_page <= half_max_page_num:
                start_page = 1
                end_page = max_page_num
            else:
                # 如果当前页 >= 总页数时(total_page_count),显示
                if self.current_page + 3 >= self.total_page_count:
                    start_page = self.total_page_count - max_page_num + 1
                    end_page = self.total_page_count
                else:
                    start_page = self.current_page - half_max_page_num
                    end_page = self.current_page + half_max_page_num

        for i in range(start_page, end_page + 1):
            if self.current_page == i:
                tag = "<a class='active' href='%s?page=%s'>%s</a>" % (self.base_url,i, i)
            else:
                tag = "<a href='%s?page=%s'>%s</a>" % (self.base_url,i, i)
            page_html_list.append(tag)

        # 下一页
        if self.current_page >= self.total_page_count:
            nex = "<a href='#'>下一页</a>"
        else:
            nex = "<a href='%s?page=%s'>下一页</a>" % (self.base_url,self.current_page + 1,)
        page_html_list.append(nex)

        page_html = "".join(page_html_list)

        return mark_safe(page_html)