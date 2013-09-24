import base
import uuid

def get_decl(text):
 return ()

def gen_file(filename):
 file_analize=None
 with open(filename,mode='r') as fin:
  text= fin.read()
  file_analize= base.bloc('{\n'+text+'\n}')[0]
 with open('decl'+filename,mode='w') as fout:
  fout.write(file_head(filename))
  [fout.write(gen_class(i)+'\n') for i in base.get_classdecl(file_analize)]
  fout.write(file_tail(filename))
 
def gen_class(decl):
 if type(decl)==base.TemplateClassDecl:
  return gen_template_class(decl)
 if type(decl)!=base.ClassDecl:
  return ''

 class_name= decl.class_name()
 classtext='''
template<>
class refback<{class_name}>{{  
public:  
 template<typename Tret>  
 static Tret {class_name}::* member(string name){{  
  {select_mem}
 }}  
}};
'''.format(class_name=class_name, select_mem=gen_member(decl.bloc(),class_name))

 return classtext


def gen_template_class(decl):
 if len(decl.specialized())!=0:
  return ''
 class_name= decl.class_name()+'<Ts...> '
 classtext='''
template<typename... Ts>
class refback<{class_name}>{{  
public:  
 template<typename Tret>  
 static Tret {class_name}::* member(string name){{  
{select_mem}
 }}  
}};
'''.format(class_name=class_name, select_mem=gen_member(decl.bloc(),class_name))
 return classtext


def gen_member(decl,class_name):
 ret=''
 for i in base.get_bloc_mem_name(decl):
  ret+='''
   if(name=="{mem_name}"){{
    return force_cast<Tret {class_name}::*>(&{class_name}::{mem_name});
   }}else '''.format(mem_name=i,class_name=class_name)
 
 ret+='''return 0;'''
 return ret


'''---'''

def file_head(base_file_name):
 return '''
#ifndef {file_uuid}
#define {file_uuid}
#include <typeinfo>
#include "{base_file_name}"
#include "decl.h"
'''.format(base_file_name=base_file_name,file_uuid='UUID_'+str(uuid.uuid4()).replace('-','_'))

def file_tail(base_file_name):
 return '''
#endif
'''


if __name__=='__main__':
 import sys
 file_name= len(sys.argv)>=2 and sys.argv[1] or 'testfile.cpp'
 print(file_name)
 gen_file(file_name)
