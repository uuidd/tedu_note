from django.db import models

# Create your models here.
from user.models import User


class Note(models.Model):
    title = models.CharField('笔记标题', max_length=100)
    content = models.TextField('笔记内容')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('是否活跃', default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
