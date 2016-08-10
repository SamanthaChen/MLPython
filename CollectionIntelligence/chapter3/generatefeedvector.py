#coding=utf-8
import feedparser
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#返回一个rss订阅源的标题和包含单词计数情况的字典
def getwordcounts(url):
    # 解析订阅源
    d = feedparser.parse(url)
    # d = unicode(d,'GBK').encode('UTF-8') #解决中文的情况
    wc = {}

    #循环遍历所有的文章条目
    for e in d.entries:
        if 'summary' in e: summary = e.summary
        else: summary = e.description

        # 提取一个单词列表
        words=getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
    return d.feed.title, wc

#将一段标题和摘要的html代码转换为文本
def getwords(html):
    #去除所有html标记
    txt = re.compile(r'<[^>]+>').sub('',html)

    # 利用所有非字母字符拆分出单词
    words = re.compile(r'[^A-z^a-z]+').split(txt)

    # 转换为小写
    return [word.lower() for word in words if word!='']


if __name__ =='__main__':

    apcount = {} # 单词，博客数目
    wordcounts = {} #每篇文章的词频统计
    feedlist = [line for line in file('feedlist.txt')]
    for feedurl in feedlist:
        try:
            title,wc=getwordcounts(feedurl)
            wordcounts[title]=wc
            for word,count in wc.items():
                apcount.setdefault(word,0)
                if count>1:
                    apcount[word]+=1
        except:
            print 'Failed to parse feed %s' % feedurl

    #建立一个单词列表，筛掉一些普遍出现的单词
    wordlist = []
    for w,bc in apcount.items():
        frac = float(bc)/len(feedlist)
        if frac>0.1 and frac<0.5: wordlist.append(w)

    #建立一个文本文件，包含大矩阵记录每个博客所有单词的统计情况
    out=file('blogdata.txt','w')
    out.write('Blog')
    for word in wordlist: out.write('\t%s'%word)
    out.write('\n')
    for blog,wc in wordcounts.items():
        out.write(blog)
        for word in wordlist:
            if word in wc: out.write('\t%d'%wc[word])
            else: out.write('\t0')
        out.write('\n')