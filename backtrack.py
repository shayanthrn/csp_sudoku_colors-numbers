import copy




class sodotable:
    def __init__(self,table,n,colors):
        self.table=table
        self.n=n
        self.colors=colors
    def iscomplete(self):
        for i in range(self.n):
            for j in range(self.n):
                if(self.table[i][j].number=="*"):
                    return False
                if(self.table[i][j].color=="#"):
                    return False
        return True
    def isconsistent(self,i,j,value,mtype):
        newcell=copy.deepcopy(self.table[i][j])
        if(mtype=="number"):
            newcell.number=value
        else:
            newcell.color=value
        if(mtype=="color"):  #check color differece
            if(i-1>=0): #up
                if(self.table[i-1][j].color==value):
                    return False
            if(i+1<len(self.table)): #bot
                if(self.table[i+1][j].color==value):
                    return False
            if(j-1>=0): #left
                if(self.table[i][j-1].color==value):
                    return False
            if(j+1<len(self.table)): #right
                if(self.table[i][j+1].color==value):
                    return False
        if(mtype=="number"):
            for k in range(len(self.table)):
                if(self.table[k][j].number==value and k!=i):
                    return False
                if(self.table[i][k].number==value and k!=j):
                    return False
        #check color priority
        if(newcell.color!="#" and newcell.number!="*"):
            if(i-1>=0): #up
                if(self.table[i-1][j].assigned==True and self.table[i-1][j].number>newcell.number and self.colors.index(self.table[i-1][j].color)>self.colors.index(newcell.color)):
                    return False
                if(self.table[i-1][j].assigned==True and self.table[i-1][j].number<newcell.number and self.colors.index(self.table[i-1][j].color)<self.colors.index(newcell.color)):
                    return False
            if(i+1<len(self.table)): #bot
                if(self.table[i+1][j].assigned==True and self.table[i+1][j].number>newcell.number and self.colors.index(self.table[i+1][j].color)>self.colors.index(newcell.color)):
                    return False
                if(self.table[i+1][j].assigned==True and self.table[i+1][j].number<newcell.number and self.colors.index(self.table[i+1][j].color)<self.colors.index(newcell.color)):
                    return False
            if(j-1>=0): #left
                if(self.table[i][j-1].assigned==True and self.table[i][j-1].number>newcell.number and self.colors.index(self.table[i][j-1].color)>self.colors.index(newcell.color)):
                    return False
                if(self.table[i][j-1].assigned==True and self.table[i][j-1].number<newcell.number and self.colors.index(self.table[i][j-1].color)<self.colors.index(newcell.color)):
                    return False
            if(j+1<len(self.table)): #right
                if(self.table[i][j+1].assigned==True and self.table[i][j+1].number>newcell.number and self.colors.index(self.table[i][j+1].color)>self.colors.index(newcell.color)):
                    return False
                if(self.table[i][j+1].assigned==True and self.table[i][j+1].number<newcell.number and self.colors.index(self.table[i][j+1].color)<self.colors.index(newcell.color)):
                    return False
        return True


        



class cell:
    def __init__(self,el):
        self.color=el[1]
        self.number=el[0]
        if(el[0]!="*"):
            self.number=int(self.number)
        if(el[1]!="#" and el[0]!="*"):
            self.assigned=True
        else:
            self.assigned=False
        if(el[1]=="#"):
            self.colorassigned=False
        else:
            self.colorassigned=True
        if(el[0]=="*"):
            self.numberassigned=False
        else:
            self.numberassigned=True
    def __str__(self):
        return str(self.number)+self.color

def printtable(table,n):
    for i in range(n):
        for j in range(n):
            print(table[i][j],end=" ")
        print("")

def index_in_list(a_list, index):
    return (index < len(a_list))

def degreecalculate(table,indexes):
    i,j=indexes
    degree=0
    #effect of color
    if(table[i][j].colorassigned==False):
        if(i-1>=0): #up
            if(table[i-1][j].colorassigned==False):
                degree+=1
        if(i+1<len(table)): #bot
            if(table[i+1][j].colorassigned==False):
                degree+=1
        if(j-1>=0): #left
            if(table[i][j-1].colorassigned==False):
                degree+=1
        if(j+1<len(table)): #right
            if(table[i][j+1].colorassigned==False):
                degree+=1
    #effect of number
    if(table[i][j].numberassigned==False):
        for k in range(len(table)): #numbers in same column and row
            if(table[k][j].numberassigned==False and k!=i):
                degree+=1
            if(table[i][k].numberassigned==False and k!=j):
                degree+=1
    return degree

def selectvariable(table,domains):
    #mrv
    lens=[]
    indexes=[]
    for i in range(len(table)):
        for j in range(len(table)):
            if(table[i][j].assigned==False):
                temp=0
                if(table[i][j].numberassigned==False):
                    temp+=len(domains[i][j]["number"])
                if(table[i][j].colorassigned==False):
                    temp+=len(domains[i][j]["color"])
                lens.append(temp)
                indexes.append((i,j))
    #sort lens
    for i in range(len(lens)):
        for j in range(i,len(lens)):
            if(lens[i]>lens[j]):
                lens[i],lens[j]=lens[j],lens[i]
                indexes[i],indexes[j]=indexes[j],indexes[i]
    if(len(lens)>1):
        if(lens[0]<lens[1]):
            return indexes[0]
        else:
            #mrv faild so we go for degree
            candidates=[indexes[0]]
            degrees=[]
            l=1
            while(lens[0]==lens[l]):
                candidates.append(indexes[l])
                l+=1
                if(index_in_list(lens,l)==False):
                    break
            for i in candidates:
                degree=degreecalculate(table,i)
                degrees.append(degree)
            #sort degree
            for i in range(len(degrees)):
                for j in range(i,len(degrees)):
                    if(degrees[i]<degrees[j]):
                        degrees[i],degrees[j]=degrees[j],degrees[i]
                        candidates[i],candidates[j]=candidates[j],candidates[i]
            return candidates[0]
    else:
        return indexes[0]


def forwardchecking(domains,table,i,j,colors):
    newdomain=copy.deepcopy(domains)
    #remove same numbers in row and column
    if(table[i][j].number!="*"):
        for k in range(len(table)):
            if(k!=i and table[i][j].number in newdomain[k][j]["number"]):
                newdomain[k][j]["number"].remove(table[i][j].number)
            if(k!=j and table[i][j].number in newdomain[i][k]["number"]):
                newdomain[i][k]["number"].remove(table[i][j].number)
    # #remove same color around
    if(table[i][j].color!="#"):
        if(i-1>=0): #up
            if(table[i][j].color in newdomain[i-1][j]["color"] and table[i-1][j].assigned==False):
                newdomain[i-1][j]["color"].remove(table[i][j].color)
        if(i+1<len(table)): #bot
            if(table[i][j].color in newdomain[i+1][j]["color"] and table[i+1][j].assigned==False):
                newdomain[i+1][j]["color"].remove(table[i][j].color)
        if(j-1>=0): #left
            if(table[i][j].color in newdomain[i][j-1]["color"] and table[i][j-1].assigned==False):
                newdomain[i][j-1]["color"].remove(table[i][j].color)
        if(j+1<len(table)): #right
            if(table[i][j].color in newdomain[i][j+1]["color"] and table[i][j+1].assigned==False):
                newdomain[i][j+1]["color"].remove(table[i][j].color)
    #check color priority
        if(table[i][j].color!="#" and table[i][j].number!="*"):
            if(i-1>=0): #up
                if(table[i-1][j].colorassigned==False and table[i-1][j].numberassigned==True):
                    if(table[i][j].number>table[i-1][j].number):
                        for k in newdomain[i-1][j]["color"]:
                            if(colors.index(k)<colors.index(table[i][j].color)):
                                newdomain[i-1][j]["color"].remove(k)
                if(table[i-1][j].colorassigned==True and table[i-1][j].numberassigned==False):
                    if(colors.index(table[i-1][j].color)>colors.index(table[i][j].color)):
                        for k in newdomain[i-1][j]["number"]:
                            if(k>table[i][j].number):
                                newdomain[i-1][j]["number"].remove(k)
            if(i+1<len(table)): #bot
                if(table[i+1][j].colorassigned==False and table[i+1][j].numberassigned==True):
                    if(table[i][j].number>table[i+1][j].number):
                        for k in newdomain[i+1][j]["color"]:
                            if(colors.index(k)<colors.index(table[i][j].color)):
                                newdomain[i+1][j]["color"].remove(k)
                if(table[i+1][j].colorassigned==True and table[i+1][j].numberassigned==False):
                    if(colors.index(table[i+1][j].color)>colors.index(table[i][j].color)):
                        for k in newdomain[i+1][j]["number"]:
                            if(k>table[i][j].number):
                                newdomain[i+1][j]["number"].remove(k)
            if(j-1>=0): #left
                if(table[i][j-1].colorassigned==False and table[i][j-1].numberassigned==True):
                    if(table[i][j].number>table[i][j-1].number):
                        for k in newdomain[i][j-1]["color"]:
                            if(colors.index(k)<colors.index(table[i][j].color)):
                                newdomain[i][j-1]["color"].remove(k)
                if(table[i][j-1].colorassigned==True and table[i][j-1].numberassigned==False):
                    if(colors.index(table[i][j-1].color)>colors.index(table[i][j].color)):
                        for k in newdomain[i][j-1]["number"]:
                            if(k>table[i][j].number):
                                newdomain[i][j-1]["number"].remove(k)
            if(j+1<len(table)): #right
                if(table[i][j+1].colorassigned==False and table[i][j+1].numberassigned==True):
                    if(table[i][j].number>table[i][j+1].number):
                        for k in newdomain[i][j+1]["color"]:
                            if(colors.index(k)<colors.index(table[i][j].color)):
                                newdomain[i][j+1]["color"].remove(k)
                if(table[i][j+1].colorassigned==True and table[i][j+1].numberassigned==False):
                    if(colors.index(table[i][j+1].color)>colors.index(table[i][j].color)):
                        for k in newdomain[i][j+1]["number"]:
                            if(k>table[i][j].number):
                                newdomain[i][j+1]["number"].remove(k)
    return newdomain

def checkconsistent(domains):
    for i in range(len(domains)):
        for j in range(len(domains)):
            if(len(domains[i][j]["number"])==0 or len(domains[i][j]["color"])==0):
                return False
    return True

def backtrack(table,domains):
    if(table.iscomplete()):
        return table
    i,j=selectvariable(table.table,domains)
    # print("selected: "+str((i,j)))
    if(table.table[i][j].numberassigned==False):   #assign number
        for value in domains[i][j]["number"]:
            if table.isconsistent(i,j,value,"number"):
                table.table[i][j].number=value
                table.table[i][j].numberassigned=True
                if(table.table[i][j].colorassigned==True):
                    table.table[i][j].assigned=True
                newdomain=forwardchecking(domains,table.table,i,j,table.colors)
                if(checkconsistent(newdomain)):
                    result=backtrack(table,newdomain)
                    if result:
                        return result
                table.table[i][j].number="*"
                table.table[i][j].numberassigned=False
                table.table[i][j].assigned=False
    else:          #assign color
        for value in domains[i][j]["color"]:
            if table.isconsistent(i,j,value,"color"):
                table.table[i][j].color=value
                table.table[i][j].colorassigned=True
                if(table.table[i][j].numberassigned==True):
                    table.table[i][j].assigned=True
                newdomain=forwardchecking(domains,table.table,i,j,table.colors)
                if(checkconsistent(newdomain)):
                    result=backtrack(table,newdomain)
                    if result:
                        return result
                table.table[i][j].color="#"
                table.table[i][j].colorassigned=False
                table.table[i][j].assigned=False
    return False



m,n=input("").split(" ")
m,n=int(m),int(n)
colors=input("").split(" ")
table=[[] for i in range(n)]
for i in range(n):
    table[i]=input("").split(" ")
for i in range(n):
    for j in range(n):
        table[i][j]=cell(table[i][j])
table=sodotable(table,n,colors)
domains=[[] for i in range(n)]
for i in range(n):
    for j in range(n):
        domains[i].append({"color":copy.deepcopy(colors),"number":list(range(1,n+1))})
#fix init domain
for i in range(n):
    for j in range(n):
        if(table.table[i][j].color!="#"):
            value=table.table[i][j].color
            domains[i][j]["color"]=[value]
        if(table.table[i][j].number!="*"):
            value=table.table[i][j].number
            domains[i][j]["number"]=[value]
#fix init domain
result=backtrack(table,domains)
print("the answer is:")
if(result):
    printtable(result.table,n)
else:
    print("Fail")