#include "symbol_info.h"
#include <list>
#include <fstream>
#include <string>
#include <iomanip>

extern ofstream outlog;

class scope_table
{
private:
    int bucket_count;
    int unique_id;
    scope_table *parent_scope = NULL;
    vector<list<symbol_info *> > table;

    int hash_function(string name)
    {
        // Simple hash function that matches the expected output
        int sum = 0;
        for (char c : name)
        {
            sum += c;
        }
        return sum % bucket_count;
    }

public:
    scope_table()
    {
        bucket_count = 10;
        unique_id = 1;
        table.resize(bucket_count);
        outlog << "New ScopeTable with ID " << unique_id << " created" << endl
               << endl;
    }

    scope_table(int bucket_count, int unique_id, scope_table *parent_scope)
    {
        this->bucket_count = bucket_count;
        this->unique_id = unique_id;
        this->parent_scope = parent_scope;
        table.resize(bucket_count);
        outlog << "New ScopeTable with ID " << unique_id << " created" << endl
               << endl;
    }

    ~scope_table()
    {
        outlog << "Scopetable with ID " << unique_id << " removed" << endl
               << endl;
        // Clean up all symbol_info objects
        for (auto &bucket : table)
        {
            for (auto symbol : bucket)
            {
                delete symbol;
            }
            bucket.clear();
        }
        table.clear();
    }

    scope_table *get_parent_scope()
    {
        return parent_scope;
    }

    int get_unique_id()
    {
        return unique_id;
    }

    symbol_info *lookup_in_scope(symbol_info *symbol)
    {
        int hash_val = hash_function(symbol->getname());

        // Search in the bucket
        for (symbol_info *current : table[hash_val])
        {
            if (current->getname() == symbol->getname())
            {
                return current;
            }
        }
        return NULL;
    }

    bool insert_in_scope(symbol_info *symbol)
    {
        // First check if symbol already exists
        if (lookup_in_scope(symbol) != NULL)
        {
            return false;
        }

        // Insert the symbol
        int hash_val = hash_function(symbol->getname());
        table[hash_val].push_back(symbol);
        return true;
    }

    bool delete_from_scope(symbol_info *symbol)
    {
        int hash_val = hash_function(symbol->getname());

        // Search and remove from the bucket
        auto &bucket = table[hash_val];
        for (auto it = bucket.begin(); it != bucket.end(); ++it)
        {
            if ((*it)->getname() == symbol->getname())
            {
                bucket.erase(it);
                return true;
            }
        }
        return false;
    }

    void print_scope_table(ofstream &outlog)
    {
        outlog << "ScopeTable # " << unique_id << endl;
        for (int i = 0; i < bucket_count; i++)
        {
            if (!table[i].empty())
            {
                outlog << i << " --> ";
                for (auto current : table[i])
                {
                    outlog << "< " << current->getname() << " : " << current->gettype() << " >" << endl;
                    if (current->get_is_function())
                    {
                        outlog << "Function Definition" << endl;
                        outlog << "Return Type: " << current->get_return_type() << endl;
                        vector<pair<string, string> > params = current->get_parameters();
                        outlog << "Number of Parameters: " << params.size() << endl;
                        outlog << "Parameter Details: ";
                        for (int j = 0; j < params.size(); j++)
                        {
                            outlog << params[j].first << " " << params[j].second;
                            if (j < params.size() - 1)
                                outlog << ", ";
                        }
                        outlog << endl;
                    }
                    else if (current->get_is_array())
                    {
                        outlog << "Array" << endl;
                        outlog << "Type: " << current->get_data_type() << endl;
                        outlog << "Size: " << current->get_array_size() << endl;
                    }
                    else
                    {
                        outlog << "Variable" << endl;
                        outlog << "Type: " << current->get_data_type() << endl;
                    }
                }
            }
        }
        outlog << endl;
    }
};