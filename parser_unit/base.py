from contextlib import contextmanager

def pl_or(f1,f2):
 def ret(text):
  return f1(text) or f2(text)
 return ret

def pl_orn(*fn):
 def ret(text):
  for fi in fn:
   tmp= fi(text)
   if tmp!=None: return tmp
  return None
 return ret

def pl_may(fn):
 def ret(text):
  rf= fn(text)
  if rf==None:
   return (tuple(),text)
  else:
   return rf
 return ret

def pl_not(fn):
 def ret(text):
  if fn(text)==None:
   return (tuple(),text)
  else:
   return None
 return ret

def pl_not_zero(fn):
 def ret(text):
  tmp= fn(text)
  if tmp==None or len(tmp[0])==0:
   return None
  else:
   return tmp
 return ret

def pl_until(fn):
 def ret(text):
  cut=0
  while cut<=len(text):
   if fn(text[cut:])!=None:
    return (text[:cut],text[cut:])
   cut+=1
  return None
 return ret

def pl_mult_until(fmult,funtil):
 def ret(text):
  collect=[]
  tmptxt=text
  while True:
   rfu= funtil(tmptxt)
   if rfu!=None:
    return (tuple(collect),tmptxt)
   '''iter next'''
   rfm= fmult(tmptxt)
   if rfm==None: return None
   collect.append(rfm[0])
   tmptxt= rfm[1]
  return None
 return ret

def pl_link(*fn):
 def ret(text):
  rfn=[]
  txttail=text
  for fi in fn:
   rfi= fi(txttail)
   if rfi==None: return None
   rfn.append(rfi[0])
   txttail= rfi[1]
  return (tuple(rfn),txttail)
 return ret

def pl_mult(fn):
 def ret(text):
  rfn=[]
  txttail=text
  while True:
   rfi= fn(txttail)
   if rfi==None: break
   rfn.append(rfi[0])
   txttail= rfi[1]
  return (tuple(rfn),txttail)
 return ret

def pl_const(token):
 def ret(text):
  if text.startswith(token):
    return (token,text[len(token):])
  else:
    return None
 return ret

def pl_any_char(chars=None):
 if chars==None:
  def ret(text):
   if len(text)==0: return None
   return (text[0],text[1:])
  return ret
 else:
  def ret(text):
   if len(text)==0: return None
   elif text[0] not in chars: return None
   else: return (text[0],text[1:])
  return ret

def pl_ignore_data(fn):
 def ret(text):
  tmp= fn(text)
  return tmp and ((),tmp[1])
 return ret


class Space(str): pass
class Comment(Space): pass
class Stmt(tuple):pass
class Namespace(Stmt):
 def name(self):
  return self[1]
 def bloc(self):
  return self[2]

class ClassDecl(tuple):
 args=('class','name','base','bloc')
 def decl(self):
  return 'class '+self.__dict__.get('prefix','')+self.class_name();
 def class_name(self):
  return self[self.args.index('name')]
 def bloc(self):
  return self[self.args.index('bloc')]
 
class TemplateClassDecl(Stmt):
 name=None
 tmp=None
 spe=None
 def decl(self):
  return 'class '+str(self.templates())+' '+self.__dict__.get('prefix','')+self.class_name()+' '+str(self.specialized())
 def class_name(self):
  if self.name==None: 
   self.name= self[self.index('class')+1]
  return self.name
 def templates(self):
  if self.tmp==None:
   self.tmp= self[self.index('template')+1]
  return self.tmp
 def specialized(self):
  if self.spe==None:
   self.spe= self[self.index('class')+2]
  return self.spe
 def bloc(self):
  return self[self.index('class')+4]

def _link_str(tuple_):
 if isinstance(tuple_,(tuple,list)):
  ret=''
  for iter in tuple_:
   ret+=_link_str(iter) 
  return ret
 else:
  return tuple_

def _prettyprint(rf):
 if rf==None:
  return None
 else:
  return (_link_str(rf[0]),rf[1])

def _remove_empty_node(tuple_):
 return tuple(i for i in tuple_ if i!=())

'''token'''

def token_comment_c(text):
 cs='/*'
 ce='*/'
 if text.startswith(cs):
  end= 2+text[2:].find(ce);
  if end==-1:
   return (Comment(text),'')
  else:
   cut= end+len(ce)
   return (Comment(text[:cut]),text[cut:])
 else:
  return None

def token_comment_cxx(text):
 cs='//'
 ce='\n'
 if text.startswith(cs):
  end= text.find(ce);
  if end==-1:
   return (Comment(text),'')
  else:
   cut= end+len(ce)
   return (Comment(text[:cut]),text[cut:])
 else:
  return None

token_comment= pl_or(token_comment_c,token_comment_cxx)

def token_space_only(text):
 def _isspace(text,n):
  return text.startswith(' ',n) or\
         text.startswith('\t',n)
 cut=0
 while _isspace(text,cut):
  cut+=1
 if cut==0:
  return None
 else:
  return (Space(text[:cut]),text[cut:])

token_space_once= pl_or(token_space_only,token_comment_c)

def token_space(text):
 r'match [space \t \n comment]*'
 rfn=''
 txttail=text
 while True:
  rfi= token_space_once(txttail)
  if rfi==None: break
  rfn+=rfi[0]
  txttail=rfi[1]
 if len(rfn)==0: 
  return None
 else: 
  return (rfn,txttail)

token_newline= pl_or(pl_const('\n'),token_comment_cxx)

def token_spacen(text):
 tmp= pl_mult(pl_or(token_space,token_newline))(text)
 return tmp and (_link_str(tmp[0]),tmp[1])

_EN_set= 'abcdefghijklmnopqrstuvwxyz'
_symbol_char_start= '_'+_EN_set+_EN_set.upper()
_symbol_num= '0123456789'
_symbol_num_0x= _symbol_num+_EN_set[:6]+_EN_set[:6].upper()

_token_symbol_unprettyprint= pl_link(pl_any_char(_symbol_char_start),pl_mult(pl_any_char(_symbol_char_start+_symbol_num)))
_token_symbol_unprettyprint.__doc__='symbol:[_a-zA-Z][_a-zA-Z0-9]*'

_token_num_dec_dot= pl_link(pl_any_char('.'),pl_mult(pl_any_char(_symbol_num)))
_token_num_dec_e= pl_link(pl_any_char('eE'),pl_mult(pl_any_char(_symbol_num)))
_token_num_dec_unprettyprint= pl_link(pl_any_char(_symbol_num),pl_mult(pl_any_char(_symbol_num)),pl_may(_token_num_dec_dot),pl_may(_token_num_dec_e))
_token_num_dec_unprettyprint.__doc__=r'num-dec:[0-9]+(\.[0-9]*)?((e|E)[0-9]*)?'

_token_num_hex_unprettyprint= pl_link(pl_const('0x'),pl_mult(pl_any_char(_symbol_num_0x)))
_token_num_hex_unprettyprint.__doc__=r'num-hex:0x[0-9a-fA-F]*'

_token_num_unprettyprint= pl_or(_token_num_hex_unprettyprint,_token_num_dec_unprettyprint)

def token_symbol(text):
 return _prettyprint(_token_symbol_unprettyprint(text))

def token_num(text):
 return _prettyprint(_token_num_unprettyprint(text))

token_op= pl_any_char('()[]{}<>=+-*/%!~^&|?:,.')

def token_char(text):
 if not text.startswith("'"): return None
 try:
  if text[1]=='\\':
   if text[3]=="'": return (text[:4],text[4:])
   else: return None
  else:
   if text[2]=="'": return (text[:3],text[3:])
   else: return None
 except IndexError:
  return None

def token_str(text):
 if not text.startswith('"'): return token_char(text)
 cut=1
 while cut<=len(text):
  if text.startswith('"',cut):
   cut+=1
   return (text[:cut],text[cut:])
  elif text.startswith('\\',cut):
   cut+=2
  else:
   cut+=1
 return None

token= pl_orn(pl_ignore_data(pl_not_zero(token_spacen)),token_str,token_op,token_num,token_symbol)


def lexpl(text):
 if not text.startswith('('): return None
 collect=[]
 iter=text[1:]
 while True:
  rfmu= pl_mult_until(token,pl_any_char('();'))(iter)
  if rfmu==None: return None
  collect+=rfmu[0]
  iter=rfmu[1]
  if iter.startswith(';'): return None
  elif iter.startswith('('):
   tmp= lexpl(iter)
   if tmp==None:
    return None
   collect.append(tmp[0])
   iter=tmp[1]
  elif iter.startswith(')'):
   return (tuple(collect),iter[1:])
  else: print('ERROR: you may never go here')


def token_type(text):
 nm= token_symbol(text)
 if nm==None: return None
 tp= typelist(nm[1])
 if tp==None: return (nm[0],nm[1])
 return ((nm[0],tp[0]),token_spacen(tp[1])[1])

''' not use
def typelist(text):
 if not text.startswith('<'): return None
 ret=[]
 iter=text[1:]
 while True:
  tp= token_type(iter)
  if tp==None: return None
  ret+= tp[0]
  iter= token_spacen(tp[1])[1]
  if iter.startswith(','):
   iter= token_spacen(iter[1:])[1]
  else:
   break
 if not iter.startswith('>'): return None
 iter= token_spacen(iter[1:])[1]
 return (tuple(ret),iter)
'''

def typelist(text):
 if not text.startswith('<'): return None
 ret=[]
 iter=text[1:]
 while True:
  dc= token_type(iter)
  if dc==None: break
  iter= token_spacen(dc[1])[1]
  tp= token_type(iter)
  if tp!=None:
   ret+= (dc[0],tp[0])
   iter= token_spacen(tp[1])[1]
  else:
   ret+= [dc[0]]
   iter= token_spacen(dc[1])[1]
  if iter.startswith(','):
   iter= token_spacen(iter[1:])[1]

 if not iter.startswith('>'): return None
 iter= token_spacen(iter[1:])[1]
 return (tuple(ret),iter)


'''stmt'''

_stmt_define_unprettyprint= pl_link(pl_const('#define'),token_space,token_symbol,pl_may(pl_until(pl_any_char('\n'))),pl_any_char('\n'))
_stmt_define_unprettyprint.__doc__=r'#define symbol( exp)?\n'
def stmt_define(text):
 tmp= _stmt_define_unprettyprint(text)
 return tmp and (('#define',tmp[0][2],token_space(' '+tmp[0][3])[1]),tmp[1])

_stmt_include_unprettyprint= pl_link(pl_const('#include'),pl_until(token_newline),token_newline)
_stmt_include_unprettyprint.__doc__=r'#include .* newline'
def stmt_include(text):
 tmp= _stmt_include_unprettyprint(text)
 return tmp and (('#include',token_space(' '+tmp[0][1])[1]or''),tmp[1])


_stmt_usingnamespace= pl_link(pl_const('using namespace'),pl_until(pl_any_char(';')),pl_any_char(';'),token_spacen)
def stmt_usingnamespace(text):
 'using-namespace:using namespace .* ; SPACEN'
 tmp= _stmt_usingnamespace(text)
 return tmp and (('using namespace',token_space(' '+tmp[0][1])[1]),tmp[1])

def stmt_class_protect(text):
 tmp= pl_link(pl_orn(pl_const('public'),pl_const('private'),pl_const('protected')),token_spacen,pl_any_char(':'),token_spacen)(text)
 return tmp and (tmp[0][0]+':',tmp[1])

def stmt_dowhile(text):
 tmp= pl_link(\
       pl_const('do'),\
       pl_may(token_spacen),\
       bloc,\
       pl_may(token_spacen),
       pl_const('while'),\
       lexpl,\
       pl_may(pl_any_char(';')),\
       pl_may(token_spacen))(text)
 return tmp

def stmt_class_decl(text):
 t1= pl_const('class')(text)
 if t1==None: return None
 t2= token_symbol(token_spacen(t1[1])[1])
 if t2==None: return None
 t3= pl_mult_until(token,pl_any_char('{'))(t2[1])
 if t3==None: return None
 t4= bloc(t3[1])
 if t4==None: return None
 t5= pl_any_char(';')(token_spacen(t4[1])[1])
 if t5==None: return None
 return (ClassDecl(('class',t2[0],_remove_empty_node(t3[0]),t4[0])),token_spacen(t5[1])[1])


def stmt_template_class_decl(text):
 kw1= pl_const('template')(text)
 if kw1==None: return None
 Tlst1= typelist(token_spacen(kw1[1])[1])
 if Tlst1==None: return None
 kw2= pl_const('class')(token_spacen(Tlst1[1])[1])
 if kw2==None: return None
 clsname= token_symbol(token_spacen(kw2[1])[1])
 if clsname==None: return None
 Tlst2= typelist(token_spacen(clsname[1])[1])
 if Tlst2==None: Tlst2=((),token_spacen(clsname[1])[1])
 basecls= pl_mult_until(token,pl_any_char('{'))(Tlst2[1])
 if basecls==None: return None
 clsdef= bloc(basecls[1])
 if clsdef==None: return None
 kw3= pl_any_char(';')(token_spacen(clsdef[1])[1])
 if kw3==None: return None
 return (TemplateClassDecl(('template',Tlst1[0],'class',clsname[0],Tlst2[0],_remove_empty_node(basecls[0]),clsdef[0])),token_spacen(kw3[1])[1])

def stmt_other(text):
 tmp= pl_mult_until(token,pl_any_char(';{'))(text)
 if tmp==None: return None
 flitedtmp= tuple(i for i in tmp[0] if len(i)!=0)
 if tmp[1].startswith(';'):
  return (flitedtmp+(';',),tmp[1][1:])
 elif tmp[1].startswith('{'):
  rbloc= bloc(tmp[1])
  return rbloc and (flitedtmp+(rbloc[0],),token_spacen(' '+rbloc[1])[1])
 else:
  return None

def stmt_namespace(text):
 tmp= pl_link(pl_const('namespace'),token_spacen,token_symbol,token_spacen,bloc)(text)
 return tmp and (Namespace(('namespace',str(tmp[0][2]),tmp[0][4])),tmp[1])

def bloc(text):
 if not text.startswith('{'): return None
 tmp= pl_mult_until(stmt,pl_any_char('}'))(text[1:])
 if tmp==None: return None
 nln= pl_link(pl_any_char('}'),pl_ignore_data(token_spacen))(tmp[1])
 return nln and (tuple(i for i in tmp[0] if len(i)!=0),nln[1])

'''TODO
def stmt_if(text):
 if not text.startswith('if'): return None
 tmp= pl_link(token_spacen)
'''
stmt= pl_orn(\
  pl_ignore_data(pl_not_zero(token_spacen)),\
  stmt_define,\
  stmt_include,\
  stmt_class_protect,\
  stmt_dowhile,\
  stmt_namespace,\
  stmt_class_decl,\
  stmt_template_class_decl,\
  stmt_other,\
  bloc)


def pretty_print(*node,prefix=''):
 prev=0
 if not isinstance(node,(tuple,list,map)): 
  print(type(node),node) 
  raise TypeError
 print('(',end='')
 for i in node:
  if isinstance(i,(tuple,list,map)):
   if prev!=0:
     print('\n'+prefix,end='')
   prev=2
   pretty_print(*i,prefix=prefix+' ')
  else:
   if prev==2:
    print('\n'+prefix,end='')
   elif prev==1:
    print(' ',end='')
   prev=1
   print(i,end='')
 print(')',end='')

def get_classdecl(file_root,prefix='::'):
 ret=[]
 for iter in file_root:
  if type(iter) == Namespace:
   ret+=get_classdecl(iter.bloc(),prefix+iter.name()+'::')
  if type(iter) in (ClassDecl,TemplateClassDecl):
   iter.prefix=prefix
   ret+=[iter]
   ret+=get_classdecl(iter.bloc(),prefix+iter.class_name()+'::')
 return tuple(ret)

if __name__=='__main__':
 '''test case'''
 match_123= pl_const('123')
 print('123%123',match_123('123'))
 match_123_or_456= pl_or(match_123,pl_const('456'))
 print('456%123|456',match_123_or_456('456'))
 print('until',pl_until(pl_const('456'))('123456'))
 print('n*',pl_mult(match_123)('123123123456'))
 print('mult-until',pl_mult_until(pl_any_char('123'),pl_const('456'))('123321456'))
 print('comment',token_comment('/*123*/456'))
 print('comment',token_comment('//123\n456'))
 print('space*',token_spacen(' //line1\n \t\t/*line2*/ 456'))
 print('symbol',token_symbol('_as012df=self'))
 print('number',token_num('12.34e56E456'))
 print('number',token_num('0x123x456'))
 print('number',token_num('123-456'))
 print('char',token_str(r"'\''456"))
 print('str',token_str(r'"12\"3"456'))
 print('#define',stmt_define('#define D\n456'))
 print('#define',stmt_define('#define A 20\n456'))
 print('#include',stmt_include('#include<iostream>/*TODO fix*/ //123\n456'))
 print('#include',stmt_include('#include /*000*/"stdio.h"//123\n456'))
 print('using-namespace',stmt_usingnamespace('using namespace std;\n456'))
 print('token',pl_mult(token)('(abc+42)'))
 print('(exp)',lexpl('(abc+42)456'))
 print('stmt',stmt('#include<iostream> \n int a=0;'))
 print('type',token_type('vector<map<int,int>> 456'))
 final_test= bloc(r'''{
#include<typeinfo>
#include<iostream>
#include<string>
using namespace std;

/*//comment//*/
/*commen
comment
//comment*/
//comment/*
namespace my{
template<typename T>
class my_hello{
public:
 my_hello(const T& _nm):name(_nm){}
 virtual string get(){return typeid(name).name();}
 operator const string&(){return get();}
 T name;
};
template<>
class my_hello<string>{
public:
 my_hello(const string& _nm):name(_nm){}
 virtual const string& get(){return name;}
 operator const string&(){return get();}
 string name;
};
class my_hello_123: public my_hello<string>{
public:
 my_hello_123():my_hello("world"){}
 virtual const string& get(){
  return string("hello ")+my_hello::get();
 }
 static my_hello_123* instance(){
  static my_hello_123* _ins=0;
  if(!_ins){ins=new my_hello_123();}
  return _ins;
 }
};

int main(int argc, char** argv){
 cout<< *my_hello_123::instance()<< endl;
 return 0;
}
}
 }''')
 pretty_print('final-test',final_test)
 print('classes:')
 [print('+++',i.decl()) for i in get_classdecl(final_test[0])]

 