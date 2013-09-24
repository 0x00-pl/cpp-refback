
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
string strnone;

template<typename T>
class my_hello{
public:
 my_hello(const T& _val):name(_val){}
 virtual string get(){return typeid(name).name();}
 operator const string&(){return strnone;}
 T name;
};
template<>
class my_hello<string>{
public:
 my_hello(const string& _nm):name(_nm){name+=" @my_hello<string>";}
 virtual string get(){return name;}
 operator const string&(){return name;}
 string name;
};
class my_hello_123: public my_hello<int>{
public:
 my_hello_123():my_hello(123){mystring= string("hello 123");}
 virtual string get(){
  mystring= string("hello 123");
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
 cout<<(my_hello_123::instance())->*(refback<my_hello_123>::member<string>("mystring"))<<endl;
 my_hello<string> obj("hello ");
 cout<<(obj.*(refback<my_hello<string> >::member<string()>("get")))()<<endl;
 return 0;
}

#endif