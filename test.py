def test():
    dict_2={}
    dict_2["name"]="abhinav"
    return dict_2
    





dict_1={"A":1,"B":"C"}
dict_1.update(test())
print(dict_1)