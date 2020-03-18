from flask import Flask, render_template

app = Flask(__name__)  # 默认省略了三个参数,static_url_path, static_folder, template_folder


@app.route('/')
def hello_world():
    # 定义函数，整数，字符串，元组，列表，字典
    num = 10
    str = 'hello  马丁'
    tuple = (1, 2, 3, 4)
    list = [5, 6, 7, 8]
    dict = {
        "name": "陈怡坤",
        "age": 23
    }

    return render_template('file01.html', my_num=num, my_str=str, my_tuple=tuple, my_list=list, my_dict=dict)


if __name__ == "__main__":
    app.run()





























