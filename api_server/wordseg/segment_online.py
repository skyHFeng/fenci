import jieba
import json
from urllib.parse import unquote

if __name__ == '__main__':
    # 获取用户输入的句子
    sen = input()
    # 对句子进行解码
    sen = unquote(sen)

    # 对句子进行分词
    words = jieba.cut(sen)
    # 将分词结果拼接为字符串
    result = {"result": ' '.join(words)}

    # 输出以json格式表示的字符串
    print(json.dumps(result))
