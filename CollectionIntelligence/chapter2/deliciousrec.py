#coding=utf-8
from pydelicious import get_popular,get_userposts, get_urlposts

def initializeUserDict(tag,count = 5):
    user_dict = {}
    #获取前count个最受欢迎的链接张贴记录
    for p1 in  get_popular(tag=tag)[0:count]:
        #查找所有张贴记录的用户
        for p2 in get_urlposts(p1['url']):
            user = p2['user']
            user_dict[user] = {} #得到一个包含用户的空字典
    return  user_dict

# 填充所有用户评价的函数
def fillItems(user_dict):
    all_items = {}
    #查找所有用户都提交过的链接
    for user in user_dict:
        for i in range(3):#阻塞时候代码会重试最多3次
            try:
                posts = get_userposts(user)
                break
            except:
                print "Failed user"+user+", retyring"
                time.sleep(4)
        for post in posts:
            url = post['url']
            user_dict[user][url]=1.0
            all_items[url]=1

    # 用0填充缺失的
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item]=0.0


if __name__ == '__main__':
    initializeUserDict('programming')

