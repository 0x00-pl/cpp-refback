#ifndef DECL_H
#define DECL_H

#include<string>

template<typename R, typename T>
R force_cast(T v){
 return *(R*)(&v);
}

template<typename T>  
class refback{  
public:  
 template<typename Tret>  
 static Tret T::* member(std::string){
  throw "undifine you need #include \"decl+YOUR_FILE_NAME\"";
  return 0;  
 }  
};

#endif
