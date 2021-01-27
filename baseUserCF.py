#-*-coding:utf-8-*-
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'book.settings'
import django
django.setup()
from user.models import *
from math import sqrt,pow
import operator
class UserCf():

    #获得初始化数据
    def __init__(self,data):
        self.data=data;

    #通过用户名获得商品列表，仅调试使用
    def getItems(self,username1,username2):
        return self.data[username1],self.data[username2]

    #计算两个用户的皮尔逊相关系数
    def pearson(self,user1,user2):#数据格式为：商品id，浏览此
        sumXY=0.0;
        n=0;
        sumX=0.0;
        sumY=0.0;
        sumX2=0.0;
        sumY2=0.0;
        try:
            for movie1,score1 in user1.items():
                if movie1 in user2.keys():#计算公共的商品浏览次数
                    n+=1;
                    sumXY+=score1*user2[movie1]
                    sumX+=score1;
                    sumY+=user2[movie1]
                    sumX2+=pow(score1,2)
                    sumY2+=pow(user2[movie1],2)
            if n==0:
                return 0
            molecule=sumXY-(sumX*sumY)/n;
            denominator=sqrt((sumX2-pow(sumX,2)/n)*(sumY2-pow(sumY,2)/n))
            if denominator==0:
                return 0
            r=molecule/denominator
        except:
            print("hello")
            return None
        return r

    #计算与当前用户的距离，获得最临近的用户
    def nearstUser(self,username,n=1):
        distances={};#用户，相似度
        for otherUser,items in self.data.items():#遍历整个数据集
            if otherUser not in username:#非当前的用户
                distance=self.pearson(self.data[username],self.data[otherUser])#计算两个用户的相似度
                distances[otherUser]=distance
        sortedDistance=sorted(distances.items(),key=operator.itemgetter(1),reverse=True);#最相似的N个用户
        print(sortedDistance[:n])
        return sortedDistance[:n]


    #给用户推荐商品
    def recomand(self,username,n=1):
        recommand={};#待推荐的电影
        for user,score in dict(self.nearstUser(username,n)).items():#最相近的n个用户
            for movies,scores in self.data[user].items():#推荐的用户的商品列表
                if movies not in self.data[username].keys():#当前username没有看过
                    if movies not in recommand.keys():#添加到推荐列表中
                        recommand[movies]=scores

        return sorted(recommand.items(),key=operator.itemgetter(1),reverse=True);#对推荐的结果按照商品浏览次数排序
def rec(user_id):
    nowuser=User.objects.get(id=user_id)
    users=User.objects.all()
    alluser={}
    for user in users:
        rates=user.rate_set.all()
        rate={}
        if rates:
            for i in rates:
                rate.setdefault(str(i.book.id),i.mark)
            alluser.setdefault(user.username,rate)
    print(alluser)
    userCf=UserCf(data=alluser)
    recommandList=userCf.recomand(nowuser.username, 15)
    print(recommandList)
    goodid=[]
    for i in recommandList:
        goodid.append(i[0])
    return goodid
rec(1)
