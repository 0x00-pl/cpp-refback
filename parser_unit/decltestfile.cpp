
#ifndef UUID_aee0cba7_fab4_4071_82a1_dde2abb69e01
#define UUID_aee0cba7_fab4_4071_82a1_dde2abb69e01
#include <typeinfo>
#include "testfile.cpp"
#include "decl.h"

template<typename... Ts>
class refback<my_hello<Ts...> >{  
public:  
 template<typename Tret>  
 static Tret my_hello<Ts...> ::* member(string name){  

   if(name=="get"){
    return force_cast<Tret my_hello<Ts...> ::*>(&my_hello<Ts...> ::get);
   }else 
   if(name=="name"){
    return force_cast<Tret my_hello<Ts...> ::*>(&my_hello<Ts...> ::name);
   }else return 0;
 }  
};



template<>
class refback<my_hello_123>{  
public:  
 template<typename Tret>  
 static Tret my_hello_123::* member(string name){  
  
   if(name=="get"){
    return force_cast<Tret my_hello_123::*>(&my_hello_123::get);
   }else 
   if(name=="mystring"){
    return force_cast<Tret my_hello_123::*>(&my_hello_123::mystring);
   }else 
   if(name=="instance"){
    return force_cast<Tret my_hello_123::*>(&my_hello_123::instance);
   }else return 0;
 }  
};


#endif
