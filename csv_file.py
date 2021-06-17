import hashlib
m = hashlib.md5()
m.update(b"abhi12")
print (m.hexdigest())

