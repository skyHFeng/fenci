import os
import re
import csv
import jieba
import jieba.analyse
import uuid
import json
import xlrd
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
from pyecharts.render import make_snapshot


""" 1 接收来自 Node.js 的信息 """
column = int(input())


""" 2 获取指定文件夹中最新修改的文件的完整路径 """
def getNewFile(str):
    # 获取 当前文件上上一级目录 的绝对路径
    upupPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 设置文件夹路径
    path = upupPath + str
    # 获取文件夹中的所有文件名，以列表形式返回
    lists = os.listdir(path)
    # 根据文件的最后修改日期，对文件名进行排序
    lists.sort(key=lambda x: os.path.getmtime((path + "\\" + x)))
    lists.reverse()
    # 获取最新文件的相对路径，列表中第一个
    new_file = os.path.join(path, lists[0])
    return new_file


""" 3 读取文件，进行分词 """
vocab = {}
text = ''

# (1) 读取待分词文件
target_file = getNewFile("\\uploads")
with open(target_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    column = [row[column] for row in reader]
    for line in column:
        line = line.strip()
        text += line

# (2) 读取停用词文件
upPath = os.path.dirname(__file__)
with open(upPath + '\\stop_words.txt', 'r', encoding='utf-8') as sw:
    stop_words_list = [word.strip('\n') for word in sw.readlines()]

# (3) 读取部分保留词文件（词长度为1和2）
with open(upPath + '\\some_stay_words.txt', "r", encoding="utf-8") as sw:
    some_stay_words_list = [word.strip("\n") for word in sw.readlines()]

# (4) 添加自定义词典
jieba.load_userdict(upPath + '\mydict.txt')

# (5) 分词、过滤、创建词汇表
for word in jieba.cut(text):
    # 过滤数字和特殊字符，以及停用词（逻辑运算符优先级：not > and > or）
    if not re.match(r"(\d+(\.)?(\d+)?(.+)?)|\W+", word) and word not in stop_words_list and len(word) > 2 or word in some_stay_words_list:
        vocab[word] = vocab.get(word, 0) + 1

# (6) 同义词合并
sym_dic = {}

# 读取同义词文件
sym = open(upPath + '\\synonym.txt', encoding='utf-8').read()
symStr = sym.split("\n")

# 转换为同义词字典，以待替换词为key，保留词为value
for line in symStr:
    sym_line_list = line.split(" ")
    for i in range(1, len(sym_line_list)):
        sym_dic[sym_line_list[i]] = sym_line_list[0]

# 同义词字典的key列表
sym_list = list(sym_dic.keys())

# 同义词合并
for key in list(vocab.keys()):
    if key in sym_list:
        vocab[sym_dic[key]] += vocab[key]
        vocab.pop(key)

# (7) 字典按value排序，得到词汇列表
list_vocab = sorted(vocab.items(), key=lambda d: d[1], reverse=True)

# 生成一个包含数字和字母的随机字符串
randomStr = uuid.uuid4().hex
# (8) 导出列表结果
upupPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(upupPath + '\\result_files\\' + randomStr + '.txt', 'w', encoding='utf-8') as rs:
    for i in range(len(list_vocab)):
        rs.write(list_vocab[i][0] + ' ' + str(list_vocab[i][1]) + '\n')
    # print("分词完成！")


""" 4 可视化 """
# 打开工作簿
workbook = xlrd.open_workbook(upPath + '\\tech_classify.xls')

# 获取sheet表
table_AI = workbook.sheet_by_index(0)
table_frame = workbook.sheet_by_index(1)
table_language = workbook.sheet_by_index(2)

def remove_empty(s):
    while '' in s:
        s.remove('')
    return s

# 获取“AI”类别
class_AI = table_AI.row_values(0)

# 获取“机器学习”类别
class_ML = table_AI.col_values(0, 1)
remove_empty(class_ML)
# 获取“CV”类别
class_CV = table_AI.col_values(1, 1)
remove_empty(class_CV)
# 获取“NLP”类别
class_NLP = table_AI.col_values(2, 1)

# 获取“机器学习框架”类别
class_MLframe = table_frame.col_values(0, 1)
# 获取“大数据框架”类别
class_BDframe = table_frame.col_values(1, 1)
remove_empty(class_BDframe)

# 获取“语言”类别
class_language = table_language.col_values(0, 1)

# (1) Top10
top10 = []
count = 0

for i in range(len(list_vocab)):
    if count == 10:
        break
    if list_vocab[i][0] not in class_MLframe and list_vocab[i][0] not in class_BDframe and list_vocab[i][0] not in class_language:
        top10.append((list_vocab[i][0], list_vocab[i][1]))
        count += 1

pie_top10 = (
    Pie()
    .add("", top10)
    .set_global_opts(title_opts=opts.TitleOpts(title="Top10"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
)
randomStr1 = uuid.uuid4().hex
pie_top10.render(upupPath + "\\result_imgs\\top10\\" + randomStr1 + ".html")

# (2) AI
AI = []
ML = []
CV = []
NLP = []
MLframe = []
BDframe = []
Language = []

for i in range(len(list_vocab)):
    if list_vocab[i][0] in class_AI:
        AI.append((list_vocab[i][0], list_vocab[i][1]))
    if list_vocab[i][0] in class_ML:
        ML.append((list_vocab[i][0], list_vocab[i][1]))
    if list_vocab[i][0] in class_CV:
        CV.append((list_vocab[i][0], list_vocab[i][1]))
    if list_vocab[i][0] in class_NLP:
        NLP.append((list_vocab[i][0], list_vocab[i][1]))

    if list_vocab[i][0] in class_MLframe:
        MLframe.append((list_vocab[i][0], list_vocab[i][1]))
    if list_vocab[i][0] in class_BDframe:
        BDframe.append((list_vocab[i][0], list_vocab[i][1]))

    if list_vocab[i][0] in class_language:
        Language.append((list_vocab[i][0], list_vocab[i][1]))

pie_AI = (
    Pie()
    .add("", AI)
    .set_global_opts(title_opts=opts.TitleOpts(title="AI"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
)
randomStr2 = uuid.uuid4().hex
pie_AI.render(upupPath + "\\result_imgs\\ai\\" + randomStr2 + ".html")

# (2.1) 机器学习
a, b = map(list, zip(*ML))

bar_ML = (
    Bar()
    .add_xaxis(a)
    .add_yaxis("频数", b)
    .set_global_opts(title_opts=opts.TitleOpts(title="机器学习"))
)
randomStr3 = uuid.uuid4().hex
bar_ML.render(upupPath + "\\result_imgs\\ai_ml\\" + randomStr3 + ".html")

# (2.2) CV
a, b = map(list, zip(*CV))

bar_CV = (
    Bar()
    .add_xaxis(a)
    .add_yaxis("频数", b)
    .set_global_opts(title_opts=opts.TitleOpts(title="CV"))
)
randomStr4 = uuid.uuid4().hex
bar_CV.render(upupPath + "\\result_imgs\\ai_cv\\" + randomStr4 + ".html")

# (2.2) NLP
a, b = map(list, zip(*NLP))

bar_NLP = (
    Bar()
    .add_xaxis(a)
    .add_yaxis("频数", b)
    .set_global_opts(title_opts=opts.TitleOpts(title="NLP"))
)
randomStr5 = uuid.uuid4().hex
bar_NLP.render(upupPath + "\\result_imgs\\ai_nlp\\" + randomStr5 + ".html")

# (3.1) 机器学习框架
a, b = map(list, zip(*MLframe))

bar_MLframe = (
    Bar()
    .add_xaxis(a)
    .add_yaxis("频数", b)
    .set_global_opts(title_opts=opts.TitleOpts(title="MLframe"))
)
randomStr6 = uuid.uuid4().hex
bar_MLframe.render(upupPath + "\\result_imgs\\frame\\ml_frame\\" + randomStr6 + ".html")

# (3.2) 大数据框架
a, b = map(list, zip(*BDframe))

bar_BDframe = (
    Bar()
    .add_xaxis(a)
    .add_yaxis("频数", b)
    .set_global_opts(title_opts=opts.TitleOpts(title="BDframe"))
)
randomStr7 = uuid.uuid4().hex
bar_BDframe.render(upupPath + "\\result_imgs\\frame\\bd_frame\\" + randomStr7 + ".html")

# (4) 语言
a, b = map(list, zip(*Language))

bar_Language = (
    Bar()
    .add_xaxis(a)
    .add_yaxis("频数", b)
    .set_global_opts(title_opts=opts.TitleOpts(title="Language"))
)
randomStr8 = uuid.uuid4().hex
bar_Language.render(upupPath + "\\result_imgs\\language\\" + randomStr8 + ".html")
# print("可视化完成")


""" 5 向 Node.js 发送信息 """
# 获取最新 结果文件和可视化数据 的完整路径，字符串格式
result = {
    "result_file": getNewFile("\\result_files"),
    "img_top10": getNewFile("\\result_imgs\\top10"),
    "img_ai": getNewFile("\\result_imgs\\ai"),
    "img_ai_ml": getNewFile("\\result_imgs\\ai_ml"),
    "img_ai_cv": getNewFile("\\result_imgs\\ai_cv"),
    "img_ai_nlp": getNewFile("\\result_imgs\\ai_nlp"),
    "img_fra_ml": getNewFile("\\result_imgs\\frame\\ml_frame"),
    "img_fra_bd": getNewFile("\\result_imgs\\frame\\bd_frame"),
    "img_language": getNewFile("\\result_imgs\\language")
}

# 转换为 JSON 格式发送给 Node.js
print(json.dumps(result))
