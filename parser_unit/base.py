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

def pl_const(token):
 def ret(text):
  if text.startswith(token):
    return (token,text[len(token):])
  else:
    raise MisMatch
 return ret
  


if __name__=='__main__':
 '''test case'''
 match_123= pl_const('123')
 print('123%123',match_123('123'))
 #print('456%123',match_123('456'))
 match_123_or_456= pl_or(match_123,pl_const('456'))
 print('456%123|456',match_123_or_456('456'))
