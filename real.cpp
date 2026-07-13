#include <iostream>
#include<vector>
#include<stdexcept>
#include<string>
#include<cmath>
#include<algorithm>
#include "real.h"
using namespace std;
int realpercision=1000;
inline int power(int a,int n) {
    int _=1;
    for(int i=0;i<n;i++){
        _*=a;
    }
    return _;
}
class real {
public:
    int frac_n = realpercision;
    int integer=0;
    vector<int>fractional={0};
    string numerator;
    string denominator;
    //for make inedx be same to 10^index.
    
    real(int a);
    real(int a ,int b);
    real(int numerator, char _tip, int denominator = 1);
    void fractionalreal(int numerator, int denominator);
    void addreal(int integer,int fractional);
    int getintreal(int n);
    void clear();
    real operator+(real _);
    real operator-(real _);
    void normalize();
    string to_string ()const;
protected:
    real(int integer,vector<int>& fractional);
};
char realtipchar='.';
inline void real::clear(){
    integer=0;
    this->fractional.clear();
    this->fractional.push_back(0); 
}
real::real(int integer,vector<int>& fractional){
    this->integer=integer;
    for(int d:fractional){
        this->fractional.push_back(d);
    }
}
real::real(int a):real (a,'.',0){}
real::real(int a ,int b):real (a,realtipchar,b){}
real::real(int a, char _tip, int b ) {
    clear();
    if (_tip=='/'){
        fractionalreal(a,b);
    }
    else if(_tip=='.'){
        addreal(a,b);
    }else {cerr<<"The char in real(int a,char,int b) get an unvalid char,please try again .you might use real.help() for search vaild char ";
        addreal(0,0);
    }

    }

void real::fractionalreal(int numerator, int denominator){
    clear();
    if (denominator == 0) {
        cerr << "The denominator in real::real(int numerator, /,int denominator) isn't be allow to be 0";
        throw runtime_error("denominator cannot be zero");
     }
    else if (numerator % denominator == 0){
    integer = numerator / denominator;
    fractional.clear();
    fractional.push_back(0);
    }
    else {
        integer = numerator / denominator;
        int remainder = numerator - denominator * integer;
        for (int i = 1; i <= frac_n; i++) {
            if (remainder == 0) break;
            remainder *= 10;
            int digit = remainder / denominator;
            fractional.push_back(digit);
            remainder = remainder - denominator * digit;
            }
        }
    }
    void real::addreal(int integer,int fractional){
    clear();
    this->integer=integer;
    if (fractional == 0) {
        return;
    }

    int digits = 0;
{
    int temp = fractional;
    while (temp > 0) {
        temp /= 10;
        digits++;
    }
}
    int temp = fractional;
    
    for(int i = 1; i <= ((digits < frac_n) ? digits : frac_n); i++) {
        int exponent = digits - i;   
        int divisor = 1;
        for(int j = 0; j < exponent; j++) divisor *= 10; 
        int digit = (temp / divisor) % 10;
        this->fractional.push_back(digit);
}
}
int real::getintreal(int n) {
        return integer;
    }
real real::operator+(real _){
    int outinteger=this->integer+_.integer;
    vector<int> outfractional;
    for(int i=0;i<min(frac_n+1,max((int)this->fractional.size(),(int)_.fractional.size()));i++){
    int a,b;
    if(i<(int)this->fractional.size()) a=this->fractional[i];else a=0;
    if(i<(int)_.fractional.size())b=_.fractional[i];else b=0;
    outfractional.push_back((a+b));
    }
    real out(outinteger,outfractional);
    out.normalize();
    return out;
}
real real::operator-(real _){
    int outinteger=this->integer-_.integer;
    vector<int> outfractional;
    for(int i=0;i<min(frac_n+1,max((int)this->fractional.size(),(int)_.fractional.size()));i++){
    int a,b;
    if(i<(int)this->fractional.size()) a=this->fractional[i];else a=0;
    if(i<(int)_.fractional.size())b=_.fractional[i];else b=0;
    outfractional.push_back((a-b));
    }
    real out(outinteger,outfractional);
    out.normalize();
    return out;
}
void real::normalize() {
    // 1. 从最低位（索引最大）向最高位（索引0）处理
    int carry = 0;
    for (int i = (int)fractional.size() - 1; i >= 0; i--) {
        fractional[i] += carry;     // 加上低一位的进位
        carry = fractional[i] / 10; // 计算进位（正数整除）
        
        // 处理负数借位（例如 -7 -> 借1位变成 3，carry = -1）
        if (fractional[i] < 0) {
            int borrow = (-fractional[i] + 9) / 10; // 计算需要借的位数
            fractional[i] += borrow * 10;
            carry -= borrow;
        }
        
        fractional[i] %= 10; // 只留个位数
    }

    // 2. 把最后的进位加到 integer 上（无论正负）
    integer += carry;

    // 3. 清理 fractional 末尾多余的 0（例如 3.14000 -> 3.14）
    while (fractional.size() > 1 && fractional.back() == 0) {
        fractional.pop_back();
    }

    // 4. 如果 fractional 只剩下占位符 {0}，且 integer 是 0，那就保留 {0}
    //    否则如果 integer 不是 0，可以保留占位符不变
}
string real::to_string ()const {
    string result = std::to_string(integer);
    // 如果小数部分只有占位符0，说明没有小数
    if (fractional.size() <= 1) {
        return result;
    }
    result += '.';
    for (size_t i = 1; i < fractional.size(); ++i) {
        result.push_back('0' + fractional[i]); // 数字转字符
    }
    return result;
}