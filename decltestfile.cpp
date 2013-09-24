
#ifndef UUID_3ccc4e85_1a9f_4fd0_a2fa_77adcfb356c2
#define UUID_3ccc4e85_1a9f_4fd0_a2fa_77adcfb356c2
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
