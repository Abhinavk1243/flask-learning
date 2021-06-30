"""import pandas as pd

data={
    "student":
    [
        {         
            "name": 'abhinav',
            "id":2,
            "age":22
        },
        {  
            "name": 'abhishek',
            "id":3,
            "age":23
        },
        {  
            "name": 'aakash',
            "id":4,
            "age":22
        }
    ],
    "teacher":[
            {         
            "name": 'abhinav',
            "id":5,
            "age":22
        },
        {  
            "name": 'abhishek',
            "id":6,
            "age":23
        },
        {  
            "name": 'aakash',
            "id":7,
            "age":22
        }

        ]
}
content_data={}
content_data["student_data"]=t=data["student"]

for i in t:
    print(i['name'])
    print(i["id"])
    print(i["age"])
    print("======")"""


import os

print(os.path.join(os.path.expanduser("~"),'config\\credential.cfg'))