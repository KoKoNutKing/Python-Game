f = open('tilemap.txt', 'w')
W,H = (101,101)
a = ''
# for i in range(25):
#     a = ''
#     for j in range(25):
#         a += '.'
#     f.write(f'\'{a}\',\n')
for i in range(W):
    a+='.'
f.write(f'\'{a}\',\n')
print(f'\'{a}\',\n')
for i in range(W-2):
    a = '.'
    for j in range(H-2):
        if i==j==((H-3)/2):
            a += 'P'
        else:
            a +='.'
    a +='.'
    f.write(f'\'{a}\',\n')
    print(f'\'{a}\',\n')
a=''
for i in range(W):
    a+='.'
f.write(f'\'{a}\',\n')
print(f'\'{a}\',\n')
f.close()



