# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return "Hello from flask"

# app.run(host="0.0.0.0", port=8500)
import sys
import json
def main(var_a):
    a = var_a
    # print(a[2])
    # print("var_a",var_a is list)
    re = {"process": a[0]}
    sys.stdout.write(json.dumps(re))
    # print(re)
if __name__ == '__main__':
    x = input()
    y = json.loads(x)
    # print(type(y[1]))
    b = main(y)

# import sys

# # รับข้อมูลที่ส่งมาจาก Django ผ่าน command line arguments
# data_from_django = sys.argv[1]

# # ประมวลผลข้อมูลตามที่ต้องการ (ตัวอย่างเพียงแสดงผลข้อมูล)
# result = f"Processed data from Django: {data_from_django}"

# # ส่งผลลัพธ์นี้กลับไปยัง Django โดยพิมพ์ไปที่ stdout
# print(result)