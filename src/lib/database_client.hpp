#include <iostream>

class DatabaseClient {
public:
    DatabaseClient(
        const std::string& db_name, 
        const std::string& user,
        const std::string& password, 
        const std::string& host,
        const std::string& port);
};