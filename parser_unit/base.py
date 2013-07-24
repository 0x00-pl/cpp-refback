from contextlib import contextmanager

class ValueWarning(Warning): pass
class MisMatch(ValueWarning): pass

@contextmanager
def try_match():
 try:
  yield
 except MisMatch:
  pass

def pl_or(f1,f2):
 def ret(text):
  with try_match():
   return f1(text)
  with try_match():
   return f2(text)
  raise MisMatch
 return ret

def pl_link(f1,f2):
 def ret(text):
  rf1,txttail1= f1(text)
  rf2,txttail2= f2(txttail1)
  return ((rf1,rf2),txttail2)
 return ret

''' not use :
def pl_mult(fn):
 def ret(text):
  col=[]
  cut=0
  with try_match():
   tail= text[cut:]
   tmp= fn(text)
   col.append(tmp[0])
   cut+=tmp[1]
  return (col,text[cut:])
 return ret
'''

def pl_mult(fn,cls=list):
 def token_fn(text):
  clo= cls()
  tmptxt= text
  with try_match():
   while True:
    tmpret= fn(tmptxt)
    clo.append(tmpret[0])
    tmptxt= tmpret[1]
  return (tuple(clo),tmptxt)
 return token_fn


def pl_const(token):
 def ret(text):
  if text.startswith(token):
    return (token,text[len(token):])
  else:
    raise MisMatch
 return ret
  
#def pl_any_char(chars):
# if len(chars)==0: raise MisMatch
# return pl_or(pl_const(chars[0]),pl_any_char(chars[1:]))

def pl_any_char(chars):
 def ret(text):
  if len(text)==0: raise MisMatch
  elif text[0] not in chars: raise MisMatch
  else: return (text[0],text[1:])
 return ret


class Space(str): pass
class Comment(Space): pass

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
 raise MisMatch

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
 raise MisMatch

token_comment= pl_or(token_comment_c,token_comment_cxx)

def _isspace(text,n):
 return text.startswith(' ',n) or\
        text.startswith('\t',n) or\
        text.startswith('\n',n)

def token_space_only(text):
 cut=0
 while _isspace(text,cut):
  cut+=1
 if cut==0:
  raise MisMatch
 else:
  return (Space(text[:cut]),text[cut:])

token_space_once= pl_or(token_space_only,token_comment)

def token_space(text):
 '''match [space \t \n comment]*'''
 cut=0
 with try_match():
  while True:
   tmptxt= text[cut:]
   tmpret= token_space_once(tmptxt)
   cut+= len(tmpret[0])
 if cut==0:
  raise MisMatch
 else:
  return (Space(text[:cut]),text[cut:])


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
