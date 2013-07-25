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

def pl_until(fn):
 def ret(text):
  cut=0
  while cut<=len(text):
   if fn(text[cut:])!=None:
    return (text[:cut],text[cut:])
   cut+=1
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

'symbol:[_a-zA-Z][_a-zA-Z0-9]*'
_token_symbol_unprettyprint= pl_link(pl_any_char(_symbol_char_start),pl_mult(pl_any_char(_symbol_char_start+_symbol_num)))
r'num:[0-9]*\.[0-9]*(e|E)[0-9]*'
_token_num_unprettyprint= pl_link(pl_any_char(_symbol_num),pl_any_char('.'),pl_any_char(_symbol_num),pl_any_char('eE'),pl_any_char(_symbol_num))
def token_symbol(text):
 return _prettyprint(_token_symbol_unprettyprint(text))

ln_define= pl_link(pl_const('#define'),token_space,token_symbol,pl_may(pl_until(pl_any_char('\n'))),pl_any_char('\n'))
'#define symbol( exp)? newline'
 

if __name__=='__main__':
 '''test case'''
 match_123= pl_const('123')
 print('123%123',match_123('123'))
 match_123_or_456= pl_or(match_123,pl_const('456'))
 print('456%123|456',match_123_or_456('456'))
 print('comment',token_comment('/*123*/456'))
 print('comment',token_comment('//123\n456'))
 print('space',token_space(' //line1\n \t\t/*line2*/ 456'))
 print('n*',pl_mult(match_123)("123123123456"))
 print('symbol',token_symbol("_as012df=self"))
 print('until',pl_until(pl_const('456'))("123456"))
 print('#define',ln_define("#define D\n456"))
 print('#define',ln_define("#define A 20\n456"))
 