#read remove_list.txt
remove_list=[]

with open("remove_list.txt", "r") as f:
    for line in f:
        if line=='\n':
            pass
        remove_list.append(line.strip())
        #if line has '-' then remove
        if '-' in line:
            A=line.split('-')[0]
            B=line.split('-')[1]
            print("A: ",A,"B: ",B)
            for i in range(int(A),int(B)+1):
                remove_list.append(str(i))
        
            
        


str=''
for i in range(len(remove_list)):
    str+='Remove-item ./'
    str+=remove_list[i].zfill(5)
    str+='.png'
    if i!=len(remove_list)-1:
        str+='; '
    
print(str)

#write remove_command.txt
with open("remove_command.txt", "w") as f:
    f.write(str)
