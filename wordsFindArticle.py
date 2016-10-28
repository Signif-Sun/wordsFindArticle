# encoding: UTF-8
# author:signif_sun
# version:1.0

import os
import re

class find_repeat_words(object):

#------------------------将文章的字幕库存到该表中--------------------------------------------------
    all_list = []
#------------------------将文章的名字与对应的单词构成字典--------------------------------------------------
    all_dic = {}

    def find_words(self, article_path):
#--------------------------------检查文安路径是否合法，采取正则------------------------------------------

        if not os.path.exists(r'%s'%article_path):
            print ("文章库文件夹不存在")
#-----------------------os中文件是否存在的判断---------------------------------------------------------

        #file_name = os.listdir(r'%s'%article_path)
        file_name = os.listdir(article_path)
        print ("file_name:",file_name)
#------------------------不重复单词表--------------------------------------------------
        words_ku_not_repeat = []
#-------------------------不重复单词出现次数的字典-------------------------------------------------
        words_ku_not_repeat2 = {}
        i = 0
        for temp in file_name:
            if re.search('.txt$',temp):
                print ("check article:", temp)
#-------------------------将寻找路径改为当前工作路径-------------------------------------------------
#                os.chdir(r"%s"%article_path)
                file_name_tmp = open(article_path+temp,"r",encoding='utf-8')
#-------------------------读取每篇文章中的所有内容存到表中-------------------------------------------------
                content = file_name_tmp.readlines()
                print ("about content:", content)
                for line in content:
#--------------------------将每一行单词分隔开形成孤立单词------------------------------------------------
                    words = line.split(' ')
#-------------------------循环去掉单词中的'.;,:?"('字符-------------------------------------------------
                    for word in words:
                        word = word.strip('.;,:?"(')
#--------------------------单词不在表中添加到表中，并用正则去掉分单词部分------------------------------------------------
                        if word not in words_ku_not_repeat:
                            if re.search('^[a-zA-Z]{1,10}$',word):
                                words_ku_not_repeat.append(word)
#---------------------------单词不再字典中添加，并且计数-----------------------------------------------
                        if re.search('^[a-zA-Z]{1,10}$',word):
                            if word in words_ku_not_repeat2:
                                words_ku_not_repeat2[word] = words_ku_not_repeat2[word] + 1
                            else:
                                words_ku_not_repeat2[word] = i + 1

#-----------------------------此处必须进行浅复制，因为py是动态数据类型，引用与数据分开的特点---------------------------------------------
                list_copy = words_ku_not_repeat.copy()

                self.all_list.append(list_copy)
#------------------------------字典key为文章名字，向字典中添加单词库作为value--------------------------------------------
                self.all_dic[temp] = list_copy
#-------------------------------删除档次的库，否则会在微端继续添加导致库累加重复而失败-------------------------------------------
                words_ku_not_repeat.clear()

                #测试程序
                print("self.all_list:", self.all_list)
                print("self.all_dic:", self.all_dic)
                #print(len(self.all_list))
                #self.all_dic.append(words_ku_not_repeat2)

            #print(words_ku_not_repeat)

#------------------------------函数返回值是单词库的表和字典--------------------------------------------
        #print(self.all_dic)   #打印形成单词库的字典
        return self.all_list,self.all_dic

#-------------------------------该函数是为了获取到不同文章出现次数，暂时留用-------------------------------------------
    def find_word_weigh(self):
        [words_repeat_dic,all_topic_dic] = self.find_words()
        #print(type(all_topic_dic))
        find_list = []
        input_k = input('请输入需要索引的单词，结束输入输入quit结束！\n')
        while input_k.isalpha() and input_k != 'quit':
            find_list.append(input_k)
            input_k = input('请输入需要索引的单词，结束输入输入quit结束！\n')
        qzzhi = [0 for x in range(len(words_repeat_dic))]
        #print(qzzhi)
        for j in range(len(words_repeat_dic)):
            for i in range(len(find_list)):
                try:
                 if words_repeat_dic[j].index(find_list[i]):
                        qzzhi[j] = qzzhi[j] + 1
                except:
                    qzzhi[j] = qzzhi[j]
        print(qzzhi)
        return qzzhi

#----------------------------找出权重值比较高的文章----------------------------------------------
    def find_weigh_topic(self):
        find_list = []
#-----------------------------输入的单词放入表中方便比对---------------------------------------------
        input_k = input('请输入需要索引的单词，结束输入输入quit结束！\n')
#------------------------------判断是否是单词，或者quit退出，非单词一样退出，健壮性暂时未补全--------------------------------------------
        while input_k.isalpha() and input_k != 'quit':
            find_list.append(input_k)
            input_k = input('请输入需要索引的单词，结束输入输入quit结束！\n')
        topic_qz = {}

        #print(qzzhi)  #测试打印

        times = 0
#------------------------------遍历词库字典，该次数也是需要找到的文章--------------------------------------------
        for (j,k) in self.all_dic.items():
            for i in range(len(find_list)):
#------------------------------初始化字典的value（出现个数）都为0--------------------------------------------
                if i == 0:
                    topic_qz[j] =  times
#-------------------------------索引利用tryexcept模式，避免索引不到抛出异常，再多引不到时候保持值不变-------------------------------------------
                try:
                 if self.all_dic[j].index(find_list[i]):
                        topic_qz[j] =  topic_qz[j] + 1
                except:
                    topic_qz[j] = topic_qz[j]
#-------------------------------从字典中检出value最大的key也就是文章名字-------------------------------------------
        res =  max(topic_qz, key=topic_qz.get)
#--------------------------------打印字典并且选出文章，为0时候随意索引，之后修改增强健壮性------------------------------------------
        print(topic_qz)
        print(res)
        return res




if __name__ == '__main__':
    find_rw = find_repeat_words()
    find_rw.find_words("./Articles/")
    find_rw.find_weigh_topic()
