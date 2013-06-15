
from os import listdir;
import re;

def moveFiles(file_dir_path):
    FILE_NAME_REGREP = re.compile(r'spring-[a-z]+-(?:[a-z]+-)*3.2.2.RELEASE.jar');
    lstF = listdir(file_dir_path);
    print (lstF);
    print ('Number of files %d' % len(lstF));
    
    jarF = [f for f in listdir(file_dir_path) if FILE_NAME_REGREP.match(f)];
    print (jarF);
    print ('Number of files %d' % len(jarF));
    
moveFiles("~/spring-framework-3.2.2.RELEASE/libs");


