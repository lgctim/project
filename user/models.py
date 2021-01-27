from django.db import models
class User(models.Model):
    username=models.CharField(max_length=32,unique=True,verbose_name="账号")
    password=models.CharField(max_length=32,verbose_name="密码")
    phone=models.CharField(max_length=32,verbose_name="手机号码")
    name=models.CharField(max_length=32,verbose_name="名字",unique=True)
    address=models.CharField(max_length=32,verbose_name="地址")
    email=models.EmailField(verbose_name="邮箱")
    class Meta:
        verbose_name_plural="用户"
        verbose_name="用户"
    def __str__(self):
        return self.name
class Tags(models.Model):
    name=models.CharField(max_length=32,verbose_name="标签")
    class Meta:
        verbose_name="标签"
        verbose_name_plural="标签"
    def __str__(self):
        return self.name
class Book(models.Model):
    tags=models.ForeignKey(Tags,on_delete=models.CASCADE,verbose_name="标签",related_name="tags",blank=True,null=True)
    collect=models.ManyToManyField(User,verbose_name="收藏者",blank=True)
    sump=models.IntegerField(verbose_name="收藏人数",default=0)
    title=models.CharField(verbose_name="书名",max_length=32)
    author=models.CharField(verbose_name="作者",max_length=32)
    intro=models.TextField(verbose_name="描述")
    num=models.IntegerField(verbose_name="浏览量",default=0)
    pic=models.CharField(verbose_name="pic",max_length=64)
    jiang=(('诺贝尔文学奖','诺贝尔文学奖'),('茅盾文学奖','茅盾文学奖'),('None','None'),)
    good=models.CharField(verbose_name="获奖",max_length=32,default=None,choices=jiang)
    class Meta:
        verbose_name="图书"
        verbose_name_plural="图书"
    def __str__(self):
        return self.title
class Score(models.Model):
    book=models.OneToOneField(Book,on_delete=models.CASCADE,verbose_name="书籍")
    num=models.IntegerField(verbose_name="人数",default=0)
    com=models.IntegerField(verbose_name="评论人数",default=0)
    fen=models.FloatField(verbose_name="评分",default=0)
    class Meta:
        verbose_name="评分"
        verbose_name_plural="评分"
class Rate(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,blank=True, null=True, verbose_name='图书id')
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True, verbose_name='用户id')
    mark=models.FloatField(verbose_name='评分')
    addtime = models.DateTimeField(verbose_name='发布时间',auto_now_add=True)
    class Meta:
        verbose_name = '评分信息'
        verbose_name_plural = verbose_name
class Commen(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    content=models.CharField(max_length=64,verbose_name="内容")
    addtime=models.DateTimeField(auto_now_add=True)
    good=models.IntegerField(verbose_name="点赞",default=0)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name="书籍")
    class Meta:
        verbose_name="评论"
        verbose_name_plural=verbose_name
class Action(models.Model):
    user=models.ManyToManyField(User,verbose_name="参加用户",blank=True)
    new=models.ManyToManyField(User,verbose_name="审核用户",related_name="newuser",blank=True)
    num=models.IntegerField(verbose_name="参与人数",default=0)
    one=models.ImageField(upload_to='media',verbose_name="第一")
    two=models.ImageField(upload_to='media',verbose_name="第二",null=True)
    three=models.ImageField(upload_to='media',verbose_name="第三",null=True)
    title=models.CharField(verbose_name="活动标题",max_length=64)
    content=models.TextField(verbose_name="活动内容")
    status=models.BooleanField(verbose_name="状态")
    class Meta:
        verbose_name="活动"
        verbose_name_plural=verbose_name
class ActionCommen(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    action=models.ForeignKey(Action,on_delete=models.CASCADE,verbose_name="活动")
    commen=models.CharField(max_length=64,verbose_name="活动评论")
    addtime=models.DateTimeField(auto_now_add=True)
class Liuyan(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    title=models.CharField(max_length=64,verbose_name="标题")
    num=models.IntegerField(verbose_name="回帖数",default=0)
    content=models.TextField(verbose_name="内容")
    addtime=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="留言"
        verbose_name_plural=verbose_name
class Liuyanson(models.Model):
    liuyan=models.ForeignKey(Liuyan,on_delete=models.CASCADE,verbose_name="留言")
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户",related_name='user')
    content=models.CharField(max_length=32,verbose_name="内容")
    addtime=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="子留言"
        verbose_name_plural=verbose_name
class Num(models.Model):
    users=models.IntegerField(verbose_name="用户数量",default=0)
    books=models.IntegerField(verbose_name="书本数量",default=0)
    commens=models.IntegerField(verbose_name="评论数量",default=0)
    rates=models.IntegerField(verbose_name="评分汇总",default=0)
    actions=models.IntegerField(verbose_name="活动汇总",default=0)
    liuyans=models.IntegerField(verbose_name="留言汇总",default=0)
    class Meta:
        verbose_name="数据统计"
        verbose_name_plural=verbose_name

