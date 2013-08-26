
#include "testfile.cpp"

template<typename T>  
class refback{  
public:  
 template<typename Tret>  
 static Tret T::* member(string){  
  return 0;  
 }  
};

template<typename T> class my_hello<>
template<> class my_hello<string>
class my_hello_123
