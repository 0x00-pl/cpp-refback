#include <iostream>
#include <string>
using namespace std;

class a{
public: 
 int b;
 int f(){return 0;}
};

template<typename R, typename T>
R force_cast(T v){
 return *(R*)(&v);
}

template<typename T>
T a::* get(string name){
 if(name=="b"){
  return force_cast<T a::*>(&a::b);
 }else if(name=="f"){
  return force_cast<T a::*>(&a::f);
 }
 return 0;
}

int main(){
 cout<<typeid(&a::b).name()<<get<int>("b")<<endl;
 cout<<typeid(&a::f).name()<<get<int()>("f")<<endl;
 cout<<typeid(&a::f).name()<<get<int()>("fe")<<endl;
}
