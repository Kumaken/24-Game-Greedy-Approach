import time
import copy
import itertools
def numTypeMatch(n1,n2):
    #return match results of even/odd-ness of n1 and n2.
    return n1&1 == n2&1

def bestOperator(n1,n2,prevOP,str_result,target):
    #pick best operator which results closest to 24:
    if(n1 <= target and n2 <= target):
        if abs(target-(n1+n2)) <= abs(target-(n1*n2)):
            op='+'
            num_result= n1+n2
        else:
            op='*'
            num_result= n1*n2
    else:
        if abs(target-(n1-n2)) <= abs(target-(n1/n2)):
            op='-'
            num_result= n1-n2
        else:
            op='/'
            num_result= n1//n2
    str_result,prevOP = addtoSols(n1,n2,op,prevOP,str_result)
    return prevOP,str_result,num_result

def bestOperator2(n1,numbers,prevOP,str_result,target):
    #pick best operator which results closest to 24:
    #print(n1)
    stop=False
    numbers.remove(n1)
    currentbest = 999
    bestn2 = 999
    op="Z"
    num_result=0
    reversal = False
    #numbers.sort(reverse=True)
    for n2 in numbers:
        if(n1 <= target and n2 <= target):
            if(abs(target-(n1+n2)) < currentbest or abs(target-(n1*n2)) < currentbest):
                if abs(target-(n1+n2)) <= abs(target-(n1*n2)):
                    op='+'
                    num_result= n1+n2
                else:
                    op='*'
                    num_result= n1*n2
                currentbest = abs(target-num_result)
                bestn2 = n2
        else:
            if n1>n2:
                if(abs(target-(n1-n2)) < currentbest or abs(target-(n1/n2)) < currentbest):
                    if abs(target-(n1-n2)) <= abs(target-(n1/n2)):
                        op='-'
                        num_result= n1-n2
                    else:
                        op='/'
                        num_result= n1//n2
                    currentbest = abs(target-num_result)
                    bestn2 = n2
            else:
                if(abs(target-(n2-n1)) < currentbest or abs(target-(n2/n1)) < currentbest):
                    if abs(target-(n2-n1)) <= abs(target-(n2/n1)):
                        op='-'
                        num_result= n2-n1                    
                    else:
                        op='/'
                        num_result= n2//n1
                    currentbest = abs(target-num_result)    
                    bestn2 = n2
                    reversal = True
    #SPECIAL CASE (__)o(__)
    if len(numbers)==2:
        #print(n1,numbers)
        lspecial =[]
        lspecial.append((numbers[0]+numbers[1], '+', 'n'))
        lspecial.append((numbers[0]-numbers[1], '-', 'n'))
        lspecial.append((numbers[1]-numbers[0], '-', 'r'))
        lspecial.append((numbers[0]*numbers[1], '*', 'n'))
        lspecial.append((numbers[0]/numbers[1], '/', 'n'))
        lspecial.append((numbers[1]/numbers[0], '/', 'r'))
        lspecial2=[]
        for x in lspecial:
            lspecial2.append((abs(target-(n1+x[0])),x[1],x[2],'+'))
            lspecial2.append((abs(target-(n1-x[0])),x[1],x[2],'-'))
            lspecial2.append((abs(target-(n1*x[0])),x[1],x[2],'*'))
            if not x[0] ==0:
                lspecial2.append((abs(target-(n1/x[0])),x[1],x[2],'/'))
        #print(lspecial2)
        bestpick= min(lspecial2,key=lambda i:i[0])
        #print(bestpick, num_result)
        if bestpick[0]< currentbest:
            #print('aaa')
            if bestpick[3] =='n':
                str_temp=str(numbers[0])+bestpick[1]+str(numbers[0])
            else:
                str_temp=str(numbers[1])+bestpick[1]+str(numbers[0])
            str_result+=bestpick[3]
            if opPrec(bestpick[1])<opPrec(bestpick[3]):
                str_result+='('+str_temp+')'
            else:
                str_result+=str_temp
            stop = True
    if not stop:
        #print(str_result)
        if reversal:
            str_result += str_result[:-3]+str(n2)+op+str_result[-3:]
        else:
            str_result,prevOP = addtoSols(n1,bestn2,op,prevOP,str_result)

    return bestn2,prevOP,str_result,num_result,stop

def addtoSols(n1,n2,op,prevOP,str_result):
    #{Membangun string ekspresi matematika yang sesuai dengan penggunaan tanda kurung yang tidak redundan}    
    opval= opPrec(op)
    if(opval > prevOP):
        str_result = '(' + str_result + ')'
    if prevOP == 999:
        str_result += str(n1)+op+str(n2)
    else:
        str_result += op+str(n2)
    prevOP = opval
    return str_result,prevOP

def opPrec(x):
    #{Menghasilkan nilai yang sesuai dengan precedence/urutan operator}
    if (x == "*" or x == "/"):
        return 2
    else:
        return 1

def isFactor(n1,n2):
    #{Menghasilkan boolean apakah n1,n2}
    return n2%n1==0

def arithmeticBasic(numbers, str_result, target):
    """{Fungsi aritmatika yang mengecek dengan cara cepat apakah suatu angka dapat
    didapat dengan hanya menggunakan operator basic plus dan minus. Logika yang
    digunakan meliputi perbandingan ganjil dan genap dari sum angka yang tersedia
    dan nilai target.}"""
    success=False
    _sum = sum(numbers)
    temps = ""
    if _sum == target:
        str_result+='+'.join(str(x) for x in numbers)
        success=True
    elif _sum <target:
        pass
    else: #sum >24 -> VALID
        if(not numTypeMatch(_sum,target)):
            pass
        else:
            temp=(_sum-target)//2
            for x in numbers:
                if x==temp:
                    success=True
                    if x == numbers[0]:
                        temps='-'+str(numbers[0])
                        for y in numbers[1:]:
                            temps += '+' + str(y)
                    else:
                        temps=str(numbers[0])
                        for y in numbers[1:]:
                            if y == x:
                                temps += '-' + str(y)
                                x=999
                            else:
                                temps += '+' + str(y)
            if not success:
                numtemp=[]
                for x in numbers:
                    if x<temp:
                        numtemp.append(x)
                if(len(numtemp)==2):
                    if(numtemp[0]+numtemp[1] == temp):
                        success=True
                        for x in numbers:
                            if ((x == numtemp[0] or x == numtemp[1]) and x== numbers[0]):
                                temps='-'+str(numbers[0])
                                for y in numbers[1:]:
                                    temps += '+' + str(y)
                            else:
                                temps=str(numbers[0])
                                for y in numbers[1:]:
                                    if y == numtemp[0] or y == numtemp[1]:
                                        temps += '-' + str(y)
                                    else:
                                        temps += '+' + str(y)

            str_result += temps
            if success:
                numbers.clear()
                numbers.append(target)
    return numbers,str_result,success

def arithmeticFactor(numbers,str_result,target):
    """{Menggunakan prinsip pemfaktoran dari angka target untuk membentuk angka
    target. Mengaplikasikan juga fungsi arithmeticBasic,arithmeticDivision1,dan
    arithmeticDivision2.}"""
    success = False
    success2 = False
    intialnums = copy.deepcopy(numbers)
    for i in range(len(numbers)):
        x= numbers[i]
        if isFactor(x,target):
            factornum = target//x
            numbers.remove(x)
            numbers,str_temp,success = arithmeticBasic(numbers,str_result,factornum)
            if not success:
                numbers,str_temp2,success2 = arithmeticDivision1(numbers,str_result,factornum)
                #print(success)
            if not success2 and not success:
                numbers,str_temp2,success2 = arithmeticDivision2(numbers,str_result,factornum)
            if not success2 and not success:
                numbers,str_temp,success = arithmeticApproximate(numbers,str_result,factornum)
            
            if success:
                #print('a')
                str_result += str(x)+'*'+'('+str_temp+')'
                break
            elif success2:
                #print('b')
                str_result += str(x)+'*'+str_temp2
                success = True
                numbers.clear()
                numbers.append(target)
                break
            else:
                str_result = ""
                numbers.clear()
                numbers=copy.deepcopy(intialnums)
                #numbers.insert(0,x)
    return numbers,str_result, success

def doubleParentheses(numbers,str_result,target):
    #SPECIAL CASE (__)o(__)
    l=list(itertools.combinations(numbers,2))
    l2 = []
    for x in l:
        if(target % (x[0]+x[1]) ==0 ):
            l2.append((x[0],x[1],'+',x[0]+x[1]))
        if(x[0]-x[1] !=0 ):
            if(target % (x[0]-x[1]) ==0 ):
                l2.append((x[0],x[1],'-',x[0]-x[1]))
        if(x[1]-x[0] !=0 ):
            if(target % (x[1]-x[0]) ==0 ):
                l2.append((x[1],x[0],'-',x[1]-x[0]))
        if(target % (x[0]*x[1]) ==0 ):
            l2.append((x[0],x[1],'*',x[0]*x[1]))
        if(target % (x[0]/x[1]) ==0 ):
            l2.append((x[0],x[1],'/',x[0]/x[1]))
        if(target % (x[1]/x[0]) ==0 ):
            l2.append((x[1],x[0],'/',x[1]/x[0]))
    for x in l2:
        numbers.remove(x[0])
        numbers.remove(x[1])
        target2 = target / x[3]
        found=False
        rev=False
        if target2 <= numbers[0]+numbers[1]:
            if(numbers[0]+numbers[1] == target2) :
                found=True
                op = '+'
            elif(numbers[0]*numbers[1] == target2) :
                found = True
                op = '*'
        else:
            if(numbers[0]-numbers[1] == target2) :
                found=True
                op = '-'
            elif(numbers[0]/numbers[1] == target2) :
                found = True
                op = '/'
            if(numbers[1]-numbers[0] == target2) :
                found=True
                op = '-'
                rev=True
            elif(numbers[1]-numbers[0] == target2) :
                found = True
                op = '/'
                rev=True
        
        if found:
            if not rev:
                str_result += '('+str(x[0])+x[2]+str(x[1])+')*('+str(numbers[0])+op+str(numbers[1])+')'
            else:
                str_result += '('+str(x[0])+x[2]+str(x[1])+')*('+str(numbers[1])+op+str(numbers[0])+')'
            break
        else:
            numbers.append(x[0])
            numbers.append(x[1])
    return numbers,str_result,found

def arithmeticApproximate(numbers,str_result,target):
    """{Aritmatika dengan tujuan utama mengaproksimasi ekspresi aritmatika hingga mendekati nilai
    tujuan dengan cara memilih 2 angka terbesar dari pool angka lalu memilih operator yang tepat
    yaitu operator yang akan menghasilkan hasil terdekat dengan nilai target}"""
    prevOP=999
    initialnums = copy.deepcopy(numbers)
    success=False
    prevn1 = max(numbers)
    num_result=0
    numbers.sort(reverse=True)
    stop=False
    for i in range(len(numbers)-1) :
        if stop:
            break
        n2,prevOP,str_result,num_result,stop = bestOperator2(prevn1,numbers,prevOP,str_result,target)
        numbers.remove(n2)
        numbers.insert(0,num_result)
        prevn1 =num_result
    if num_result==target and len(numbers)==1:
        success = True
    else:
        numbers = initialnums 
    return numbers,str_result,success

def arithmeticDivision1(numbers,str_result,target):
    """{Algoritma untuk mencari ekspresi aritmatika pembagian yang menggunakan strategi
    faktor dari angka target dan aritmatika dasar dari angka genap dan ganjil. Fungsi
    Division 1 memiliki pembilang bilangan komposit dan penyebut bilangan atomik }"""
    success = False
    str_temp =""
    for x in numbers:
        if target%x==0:
            factor=x
            target2=factor*target
            numbers.remove(x)
            numbers,str_temp,success= arithmeticBasic(numbers,str_temp,target2)
            if success:
                str_result += '('+str_temp+')/'+str(factor)
                numbers.clear()
                numbers.append(target)
                break
            else:
                numbers.insert(0,x)
    return numbers,str_result,success

def arithmeticDivision2(numbers,str_result,target):
    """{Algoritma untuk mencari ekspresi aritmatika pembagian yang menggunakan strategi
    faktor dari angka target dan aritmatika dasar dari angka genap dan ganjil. Fungsi
    Division 1 memiliki pembilang bilangan atomik dan penyebut bilangan komposit }"""
    success = False
    str_temp=""
    for x in numbers:
        if x%target==0:
            target2=x//target
            numbers.remove(x)
            numbers,str_temp,success=arithmeticBasic(numbers,str_temp,target2)
            if success:
                str_result+=str(x)+'/('+str_temp+')'
                numbers.clear()
                numbers.append(target)
                break
            else:
                numbers.insert(0,x)
    return numbers,str_result,success

def permutation_Repetition(n,*inputlist):
    pools = [tuple(pool) for pool in inputlist] * n
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
        
    for element in result:
        yield tuple(element)
       
def algorithmChecker():
    l=[]
    l.extend(range(1,14))
    l2=list(set(permutation_Repetition(4,l)))
    str_result = ""
    count = 0
    sample_num = len(l2)
    for x in l2:
       #dummyies (d):
       x = list(x)
       #tempx = copy.deepcopy(x)
       x,d2,success = arithmeticBasic(x,str_result,24)
       if not success:
            #x = copy.deepcopy(tempx)
            x,d2,success = arithmeticFactor(x,str_result,24)
            if not success:
                x,d2,success = doubleParentheses(x,str_result,24)
                if not success:
                #x=tempx
                    x,d2,success = arithmeticApproximate(x,str_result,24)
       if success:
           count+=1
    print(str(count)+" out of "+str(sample_num)+ " PERCENTAGE : " + str(count/sample_num * 100))


#algorithmChecker()
str_result = "" 
strnum = input('Input 4 numbers separated by spaces:\n')
numbers = list(map(int, strnum.split()))
numbers.sort(reverse=True)

numbers,str_result,success = arithmeticBasic(numbers,str_result,24)
if not success:
    numbers,str_result,success = arithmeticFactor(numbers,str_result,24)
    if not success:
        numbers,str_result,success = doubleParentheses(numbers,str_result,24)
        if not success:
            numbers,str_result,success = arithmeticApproximate(numbers,str_result,24)
print(str_result)
"""
numbers,str_result,success = arithmeticFactor([4,2,4,2],"",24)
print(str_result)"""
