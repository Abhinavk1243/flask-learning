import hashlib
a=hashlib.md5()
b=b"abhi1243"
a.update(b)
password=a.hexdigest()
print(password)