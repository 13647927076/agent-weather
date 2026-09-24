import json

text_2 = {
    "学生":
        [
            {'姓名': '小明', '性别': '男', '身高': 170, '体重': 160},
            {'姓名': '小红', '性别': '女', '身高': 150, '体重': 120}
        ]
}
s = json.dumps(text_2,ensure_ascii=False,indent=3)
print(s)