#include <iostream>
#include<vector>
#include<stdexcept>
#include<string>
using namespace std;
int main() {
    cout << "Hello GitHub!" << endl;
    return 0;
}
class real {
public:
    int fric_n = 1000;
    int integer;
    vector<int>frictional={0};
    //int numerator=
    real(int _1, char _tip , int _2 = 1) {
        if (_2 == 0) {
            cerr << "the _2 in real::real(int _1, /,int _2) isn't be allow to be 0";
            throw runtime_error("denominator cannot be zero");
        }
        else if (_1 % _2 == 0)integer = _1 % _2;
        else {
            integer = _1 / _2; _1 -= _2 * (_1 / _2);
            for (int i = 1; i < fric_n + 1; i++) {
                int a = 0; _1 *= 10;
                while (_1 > _2) {
                    _1 -= _2; a++;
                }
                frictional.push_back(a);
            }
        }
        

        }
    int getintreal(int n) {
        return integer;
    }
};