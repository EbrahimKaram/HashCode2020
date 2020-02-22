files=['a_example.txt','b_read_on.txt','c_incunabula.txt','d_tough_choices.txt','e_so_many_books.txt','f_libraries_of_the_world.txt']
filename=files[0]

file = open(filename,'r')

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


# Sort by Highest Number of Books: Secondary Sort
libraries_sorted=sorted(df['Libraries'].items(), key=lambda item: item[1]['BooksPerDay'],reverse=True)

# Sort by lowest NUmber of Days to Sign Up: Primary Sort
libraries_sorted=sorted(libraries_sorted, key=lambda item: item[1]['SignupDays'])

outputfile="output_"+filename

libraries = []
for lib in libraries_sorted:
    cumSum = 0
    if(cumSum < df['TotalDays']):
        cumSum += lib[1]['SignupDays']
        libraries.append(lib[0])
booksToSend = []
libBooks = []
for lib in libraries:
    booksToSend.append(df['Libraries'][lib]['BookCount'])
    libBooks.append(df['Libraries'][lib]['Books'])

output = {'LibCount':len(libraries),'Libraries':libraries,'NumberOfBooks':set(booksToSend),
          'BooksToSend':set(libBooks)}

with open(outputfile,'w') as file:
    file.write(str(output['LibCount'])+'\n')
    for (i,lib) in enumerate(output['Libraries']):
        file.write(str(output['Libraries'][i])+" "+str(output['NumberOfBooks'][i])+'\n')
        file.write(' '.join(str(book) for book in output['BooksToSend'][i]) +"\n")