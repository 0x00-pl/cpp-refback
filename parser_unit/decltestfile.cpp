
#include "testfile.cpp"

template<typename T>  
class refback{  
public:  
 template<typename Tret>  
 static Tret T::* member(string){  
  return 0;  
 }  
};

