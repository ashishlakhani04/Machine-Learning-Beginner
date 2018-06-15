class A(): 
	x=1
a = A()
print a.x
b = [A()] * 10
for ix in b:
    print ix.x
b[2].x = 5
for ix in b:
    print ix.x