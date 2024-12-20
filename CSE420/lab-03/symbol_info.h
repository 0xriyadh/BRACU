#include <iostream>
#include <string>
#include <vector>
#include <list>

using namespace std;

class symbol_info
{
private:
    string name;
    string type;
    symbol_info *next;

public:
    symbol_info(string name, string type)
    {
        this->name = name;
        this->type = type;
        next = NULL;
    }

    string getname() { return name; }
    string gettype() { return type; }
    symbol_info *getnext() { return next; }

    void setname(string name) { this->name = name; }
    void settype(string type) { this->type = type; }
    void setnext(symbol_info *next) { this->next = next; }

    ~symbol_info()
    {
        if (next)
            delete next;
    }
};