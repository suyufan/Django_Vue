from django.db import models

# Create your models here.
class Task_Info(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    task_name = models.CharField(max_length=32, verbose_name='任务名称')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    complete_time = models.DateTimeField(auto_now=True, verbose_name='完成时间')

class Image(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    image = models.CharField(max_length=255, verbose_name='图片路径')

class Checked_Image(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    # img_0 = models.FilePathField(path='static/pictures/')  # upload_to='static/pictures/'是指定图片存储的文件夹名称，上传文件之后会自动创建
    image = models.CharField(max_length=255, verbose_name='图片路径')
    task = models.ForeignKey(to="task_info", on_delete=models.CASCADE, verbose_name="任务")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='任务创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='任务更新时间')
    result = models.IntegerField(default=0000, verbose_name='检测结果') # 1000裂纹缺陷 0100压坑缺陷 0010腐蚀缺陷 0001划痕缺陷
    result_choices = (
        (0, "合格"),
        (1, '缺陷')
    )
    category = models.SmallIntegerField(choices=result_choices, verbose_name="分类",)
    trust = models.FloatField(max_length=4, verbose_name='精度')
    target = models.IntegerField(verbose_name='目标坐标')
    image_result = models.CharField(max_length=255, verbose_name='检测后图片')

class Login_Info(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.CharField(verbose_name="用户名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    logout_time = models.DateTimeField(auto_now=True, verbose_name='退出时间')


