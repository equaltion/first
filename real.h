#ifndef REAL_H
#define REAL_H

#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
using namespace std;
extern int realpercision;
class real {
public:
    int frac_n ;           // 最大精度（小数位数）
    int integer = 0;             // 整数部分
    vector<int> fractional = {0}; // 小数部分（索引0为占位符）

    // 构造函数
    real(int a);                 // 整数构造，如 real(5)
    real(int a, int b);          // 小数构造，如 real(3, 14) 表示 3.14
    real(int numerator, char _tip, int denominator = 1); // 分数构造，如 real(1,'/',3)

    // 核心功能函数
    void fractionalreal(int numerator, int denominator); // 分数转小数
    void addreal(int integerPart, int fractionalPart);   // 整数+小数构造
    void clear();                // 重置对象
    void normalize();            // 进位/借位归一化

    // 运算符重载
    real operator+(real other);
    real operator-(real other);

    // 辅助函数
    string to_string() const;   // 转为字符串，如 "3.14"
    int getintreal(int n);      // 获取整数部分（参数未使用，可保留）

protected:
    // 受保护的构造函数（供运算符重载内部使用，用于创建临时结果）
    real(int integer, const vector<int>& fractional);
};

#endif