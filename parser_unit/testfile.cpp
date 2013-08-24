#include<typeinfo>
#include<iostream>
#include<string>
using namespace std;

/*//comment//*/
/*commen
comment
//comment*/
//comment/*

template<typename T>
class my_hello{
public:
 my_hello(const T& _nm):name(_nm){}
 virtual string get(){return typeid(name).name();}
 operator const string&(){return get();}
 T name;
};
template<>
class my_hello<string>{
public:
 my_hello(const string& _nm):name(_nm){}
 virtual const string& get(){return name;}
 operator const string&(){return get();}
 string name;
};
class my_hello_123: public my_hello<string>{
public:
 my_hello_123():my_hello("world"){}
 virtual const string& get(){
  return string("hello ")+my_hello::get();
 }
 static my_hello_123* instance(){
  static my_hello_123* _ins=0;
  if(!_ins){ins=new my_hello_123();}
  return _ins;
 }
};

int main(int argc, char** argv){
 cout<< *my_hello_123::instance()<< endl;
 return 0;
}
