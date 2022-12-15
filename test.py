def test():
    dict_2={}
    dict_2["name"]="abhinav"
    dict_2['roll']=2
    return dict_2
    





dict_1={"A":1,"B":"C"}
dict_1.update(test())
print(dict_1)
