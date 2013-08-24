import base


def get_decl(text):
 return ()

def gen_file(filename):
 file_analize=None
 with open(filename,mode='r') as fin:
  text= fin.read()
  file_analize= base.bloc('{'+text+'}')[0]
 with open('decl'+filename,mode='w') as fout:
  fout.write(file_head(filename))
  [gen_class(i.decl()) for i in base.get_classdecl(file_analize)]
 
def gen_class(decl):
 if type(decl)==ClassDecl:
  return 'class '+decl.class_name();
 if type(decl)==TemplateClassDecl:
  return 'template<'+decl.templates()+'> class '+decl.class_name()+'<'+decl.specialized()+'>'
 return 'Error: not class'
 
def gen_func(decl):
 return 'void func();'

def gen_member(decl):
 return 'int a';


'''---'''

def file_head(base_file_name):
 return '''
#include "{base_file_name}"

template<typename T>  
class refback{{  
public:  
 template<typename Tret>  
 static Tret T::* member(string){{  
  return 0;  
 }}  
}};

'''.format(base_file_name=base_file_name)

if __name__=='__main__':
 import sys
 file_name= len(sys.argv)>=2 and sys.argv[1] or 'testfile.cpp'
 print(file_name)
 gen_file(file_name)