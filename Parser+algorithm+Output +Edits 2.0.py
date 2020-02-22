input_Directory = 'Inputs/'
output_Directory = 'Outputs/'
files = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt',
         'd_tough_choices.txt', 'e_so_many_books.txt', 'f_libraries_of_the_world.txt']

filename = files[0]
inputPath = input_Directory + filename
print(inputPath)
file = open(inputPath, 'r')

df = {'BookCount': 0, 'LibraryCount': 0,
      'TotalDays': 0, 'BookScores': {}, 'Libraries': {}}
libId = 0

for (i, line) in enumerate(file):
    if (line == '\n'):
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
        df['Libraries'][libId] = {'BookCount': int(line.split(' ')[0]),
                                  'SignupDays': int(line.split(' ')[1]), 'BooksPerDay': int(line.split(' ')[2]), 'Books': []}
    elif((i % 2) == 1):
        df['Libraries'][libId]['Books'] = list(map(int, line.split(' ')))
        libId += 1

#Sort By Highest Number of books: 4th Sort
libraries_sorted=sorted(df['Libraries'].items(),key=lambda item: item[1]['BookCount'], reverse=True)
# Sort by Highest Number of Books per Day: 3rd Sort
libraries_sorted = sorted(libraries_sorted, key=lambda item: item[1]['BooksPerDay'], reverse=True)

# Sort By least Number of Days to finish uploading all its Books: 2nd Sort
# libraries_sorted = sorted(libraries_sorted, key=lambda item: (item[1]['BookCount'])/(item[1]['BooksPerDay']))
# Jad's SUggestion: If it takes longer to send books its fine. As long as it's first. Highest number of Days to finish
libraries_sorted = sorted(libraries_sorted, key=lambda item: (item[1]['BookCount'])/(item[1]['BooksPerDay']),reverse=True)
# Sort by lowest NUmber of Days to Sign Up: Primary Sort
libraries_sorted = sorted(
    libraries_sorted, key=lambda item: item[1]['SignupDays'])


# Get the Unique Books in the list
# The first one sends all the books what ever is different from what was sent
# The second one sends the what hasn't been done
libraries = []
booksToSend = []
libBooks = []
books_already_sent = []
for lib in libraries_sorted:
    cumSum = 0
    if(cumSum < df['TotalDays']):
        books_in_library = df['Libraries'][lib[0]]['Books']
        distint_books_in_library = list(
            set(books_in_library) - set(books_already_sent))
        # Only if the library has distinctbooks we send
        if(len(distint_books_in_library) > 0):
            distint_books_in_library = sorted(
                distint_books_in_library, key=lambda k: df['BookScores'][k], reverse=True)
            books_already_sent = books_already_sent + distint_books_in_library
            cumSum += lib[1]['SignupDays']
            libraries.append(lib[0])
            booksToSend.append(len(distint_books_in_library))
            libBooks.append(distint_books_in_library)




output = {'LibCount': len(libraries), 'Libraries': libraries, 'NumberOfBooks': booksToSend,
          'BooksToSend': libBooks}

print('Writing File')
outputfile = output_Directory + "output_" + filename
with open(outputfile, 'w') as file:
    file.write(str(output['LibCount']) + '\n')
    for (i, lib) in enumerate(output['Libraries']):
        file.write(str(output['Libraries'][i]) + " " +
                   str(output['NumberOfBooks'][i]) + '\n')
        file.write(' '.join(str(book)
                            for book in output['BooksToSend'][i]) + "\n")
