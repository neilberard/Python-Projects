"""Error handling"""
try:
    var = 'this'
    f = open('testfile.txt')

    if f.name == 'currupt_file.txt':
        raise Exception  # Manually raise an exception
except IOError:
    print("Sorry. Can't find file")

except NameError:
    print 'bad name'
else:
    print 'no exception found, I will run this block'
# This will continue to execute code even if an exception is thrown
finally:
    print 'I will run this block no matter what'

