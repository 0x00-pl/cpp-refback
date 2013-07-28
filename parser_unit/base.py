from contextlib import contextmanager

def pl_or(f1,f2):
 def ret(text):
  return f1(text) or f2(text)
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

def pl_any_char(chars):
 def ret(text):
  if len(text)==0: return None
  elif text[0] not in chars: return None
  else: return (text[0],text[1:])
 return ret


class Space(str): pass
class Comment(Space): pass

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

'''token'''

def token_comment_c(text):
 cs='/*'
 ce='*/'
 if text.startswith(cs):
  end= text.find(ce);
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

token_spacen= pl_or(token_space,token_newline)

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

token_op= pl_any_char('()[]{}<>=+-*/%!~^&|?:,')

token= pl_or(token_op,pl_or(token_num,token_symbol))


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

'''TODO
def bloc(text):
 if not text.startswith('{'): return None
 tmp= pl_mult(stmt)(text[1:])
 if not text.startswith('}'): return None
 return tmp and (tmp[0],tmp[1][1:])

def stmt_if(text):
 if not text.startswith('if'): return None
 tmp= pl_link(token_spacen)
'''
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
 print('space*',pl_mult(token_spacen)(' //line1\n \t\t/*line2*/ 456'))
 print('symbol',token_symbol('_as012df=self'))
 print('number',token_num('12.34e56E456'))
 print('number',token_num('0x123x456'))
 print('number',token_num('123-456'))
 print('#define',stmt_define('#define D\n456'))
 print('#define',stmt_define('#define A 20\n456'))
 print('#include',stmt_include('#include<iostream>/*TODO fix*/ //123\n456'))
 print('#include',stmt_include('#include /*000*/"stdio.h"//123\n456'))
 print('using-namespace',stmt_usingnamespace('using namespace std;\n456'))
 print('token',pl_mult(token)('(a+b*(1e3+(1-2))%c/d^(0.5*e))456'))
 print('(exp)',lexpl('(a+b*(1e3+(1-2))%c/d^(0.5*e))456'))
 