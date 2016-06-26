'''
'''
import sys

try:
    #fout = open('blim.py', 'w')
    #fout.write('import this')
    with open('blim.py', 'w') as fout:
        fout.write('import this');
except IOError, e:
    print ("Error writing file: " + str(e));
finally:
    fout.close();
#    try:
#        fout.close()
#    except:
#        pass
print ("Continuing...")