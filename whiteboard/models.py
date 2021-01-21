from django.db import models

# Create your models here.
#http://ajing-notebook.blogspot.com/2019/03/python-djangoorm.html

class people(models.Model):
    user=models.CharField(max_length=150)
    employeeID=models.CharField(max_length=150)
    extension_num=models.CharField(max_length=150)
    created=models.DateTimeField(auto_now_add=True)
    cutline = models.BooleanField(default=False) #是否要插測
    done=models.BooleanField(default=False) #判斷是否已測
    line_num = models.IntegerField(default=0)
    STATUS_CHOICES=(('LTE','LTE'),('WiFi','WiFi'),('GPS','GPS'))
    frequent=models.CharField(max_length=10,choices=STATUS_CHOICES,default='LTE')
    circuleNum=models.IntegerField(default=0)
    DownTime=models.DateField(null=True,blank=True)

    #  create_time = models.DateTimeField(auto_now_add=datetime.datetime.now().replace(microsecond=0), verbose_name='创建时间')
    class Meta:
        ordering=('line_num',)

    def __str__(self):
        return self.user