file = open('c_incunabula.txt','r')

df = {'BookCount':0,'LibraryCount':0,'TotalDays':0,'BookScores':{},'Libraries':{}}
libId = 0

for (i,line) in enumerate(file):
    if (line=='\n'):
        break
    if(i == 0):
        df['BookCount'] = int(line.split(' ')[0])
        df['LibraryCount'] = int(line.split(' ')[1])
        df['TotalDays'] = int(line.split(' ')[2])
    elif (i == 1):
        scores = list(line.split(' '))
        for j in range(len(scores)):
            df['BookScores'][j] = int(scores[j])
        
    elif ((i % 2) == 0):
        # print(line.split(' '))
        df['Libraries'][libId] =  {'BookCount':int(line.split(' ')[0]),
         'SignupDays':int(line.split(' ')[1]),'BooksPerDay':int(line.split(' ')[2]),'Books':[]}
    elif((i%2)==1):
        df['Libraries'][libId]['Books']=list(map(int, line.split(' ')))    
        libId +=1

