from contextlib import contextmanager

def pl_or(f1,f2):
 def ret(text):
  return f1(text) or f2(text)
 return ret

''' not use
def pl_link(f1,f2):
 def ret(text):
  rf1= f1(text)
  if rf1==None: return None
  rf2= f2(rf1[1])
  if rf2==None: return None
  return ((rf1[0],rf2[0]),rf2[1])
 return ret
'''

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
         text.startswith('\t',n) or\
         text.startswith('\n',n)
 cut=0
 while _isspace(text,cut):
  cut+=1
 if cut==0:
  return None
 else:
  return (Space(text[:cut]),text[cut:])

token_space_once= pl_or(token_space_only,token_comment)

''' not use
def token_space(text):
 'match [space \t \n comment]*'
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
'''
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
