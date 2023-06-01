#include "database_client.hpp"

DatabaseClient::DatabaseClient(
  const std::string& db_name, 
  const std::string& user,
  const std::string& password, 
  const std::string& host,
  const std::string& port) : connection("dbname=" + db_name + " user=" + user + " password=" + password + " host=" + host + " port=" + port) {
  // TODO: connection depends on the ORM we choose
  if (connection.is_open()) {
    std::cout << "Connected :D" << std::endl;
  } else {
    std::cerr << "Failed >:(" << std::endl;
  }
}

// TODO: create a general structure for Analytics data

// TODO: methods for inserting data

// TODO: methods for fetching data

// TODO: methods for updating data

// TODO: methods for deleting data

// TODO: methods for creating/dropping tables

// TODO: methods for creating/dropping indexes