import re

def remove_comment(text)->str:
 '''remove comment in text'''
 text,_=re.subn('/\*.*\*/',' ',text,flags=re.S)
 text,_=re.subn('//.*','',text)
 return text



def unit_test():
 with open('testfile.cpp','r') as fin:
  print(remove_comment(fin.read()))

if __name__=='__main__':
 unit_test()