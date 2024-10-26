from flask import Flask,render_template
import csv
# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)

def read_txt_file(file_path):
    data = []

    ignore_chars = {'\u200b'}
    # 创建一个翻译表，用于删除非法字符
    translation_table = str.maketrans('', '', ''.join(ignore_chars))

    with open(file_path, 'r', encoding='utf-8') as file:
        # 逐行读取文件
        lines = file.readlines()  
        # 处理每行
        for line in lines:
            # 去除行尾的换行符
            line = line.rstrip()
            line = line.translate(translation_table)
            # 按空格分割元素，并忽略空格
            if line:
                elements = line.split()
                data.append(elements)
    return data


@app.route("/")
def index():
    data=read_txt_file('book.txt')
    return render_template('page.html',data=data)



# 启动一个本地开发服务器，激活该网页
if __name__=='__main__':
    app.run(debug=True)

