"""import hashlib
m = hashlib.md5()
m.update(b"abhi12")
print (m.hexdigest())
"""
list_element=input('Enter the element of list')
print(list_element)
list_1=list_element.split(",")
print(list_1)
cols_1=",".join([str(i) for i in list_element])
print(cols_1)
for i in range(0,len(list_1)):
    if list_1[i].isdigit():
        list_1[i]=int(list_1[i])

