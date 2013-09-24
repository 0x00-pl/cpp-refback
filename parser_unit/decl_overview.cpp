#include <iostream>
#include <string>
#include <typeinfo>
using namespace std;

class a{
public: 
 int b;
 int f(){return 0;}
};

template<typename T>
class ta{
public: 
 T b;
 T f(){return T();}
};



template<typename R, typename T>
R force_cast(T v){
 return *(R*)(&v);
}
template<typename T>
class refback{
public:
 template<typename Tret>
 static Tret T::* get(string name){
  return 0;
 }
};


template<>
class refback<a>{
public:
 template<typename Tret>
 static Tret a::* get(string name){
  if(name=="b"){
   return force_cast<Tret a::*>(&a::b);
  }else if(name=="f"){
   return force_cast<Tret a::*>(&a::f);
  }
  return 0;
 }
};


template<typename... T>
class refback<ta<T...> >{
public:
 template<typename Tret>
 static Tret ta<T...>::* get(string name){
  if(name=="b"){
   return force_cast<Tret ta<T...>::*>(&ta<T...>::b);
  }else if(name=="f"){
   return force_cast<Tret ta<T...>::*>(&ta<T...>::f);
  }
  return 0;
 }
};

int main(){
 cout<<typeid(&a::b).name()<<refback<a>::get<int>("b")<<endl;
 cout<<typeid(&a::f).name()<<refback<a>::get<int()>("f")<<endl;
 cout<<typeid(&a::b).name()<<refback<ta<a> >::get<a>("b")<<endl;
 cout<<typeid(&a::f).name()<<refback<ta<a> >::get<a()>("f")<<endl;
 cout<<typeid(&a::f).name()<<refback<a>::get<int()>("fe")<<endl;
}
