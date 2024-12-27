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

        // Print non-empty buckets
        for (int i = 0; i < bucket_count; i++)
        {
            if (!table[i].empty())
            {
                for (symbol_info *symbol : table[i])
                {
                    outlog << i << " --> " << endl;
                    outlog << "< " << symbol->getname() << " : ID >" << endl;
                    if (symbol->get_is_function())
                    {
                        outlog << "Function Definition" << endl;
                        outlog << "Return Type: " << symbol->get_return_type() << endl;
                        auto params = symbol->get_parameters();
                        outlog << "Number of Parameters: " << params.size() << endl;
                        outlog << "Parameter Details: ";
                        for (size_t j = 0; j < params.size(); j++)
                        {
                            if (j > 0)
                                outlog << ", ";
                            if (!params[j].second.empty())
                                outlog << params[j].first << " " << params[j].second;
                            else
                                outlog << params[j].first;
                        }
                        outlog << endl
                               << endl;
                    }
                    else if (symbol->get_is_array())
                    {
                        outlog << "Array" << endl;
                        outlog << "Type: " << symbol->get_data_type() << endl;
                        outlog << "Size: " << symbol->get_array_size() << endl
                               << endl;
                    }
                    else
                    {
                        outlog << "Variable" << endl;
                        outlog << "Type: " << symbol->get_data_type() << endl
                               << endl;
                    }
                }
            }
        }
    }
};