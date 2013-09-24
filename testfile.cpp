
#ifndef TEST_FILE_CPP
#define TEST_FILE_CPP
#include<typeinfo>
#include<iostream>
#include<string>
using namespace std;

#include"decl.h"

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
  mystring= string("hello ")+my_hello::get();
  return mystring;
 }
 string mystring;
 static my_hello_123* instance(){
  static my_hello_123* _ins=0;
  if(!_ins){_ins=new my_hello_123();}
  return _ins;
 }
};

#include"decltestfile.cpp"

int main(int argc, char** argv){
 cout<< string(*my_hello_123::instance())<< endl;
 cout<<(my_hello_123::instance())->*(refback<my_hello_123>::member<string>("mystring"))<<endl;
 return 0;
}

#endif