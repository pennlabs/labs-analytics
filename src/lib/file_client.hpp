#include "file_serializer.hpp"
#include <fstream>
#include <string>

#define DELIMITER "ඞ"
#define PENDING_FILE "pending"
#define TEMP_PENDING_FILE "temp_pending"

class Status {
public:
  Status();
};

class FileIterator {
public:
  FileIterator();
};

class FileClient {
public:
  FileClient();

  ~FileClient();

  Status write(std::string body);

  FileIterator read();

private:
  std::string m_write_file;
  std::ofstream m_write_stream;
  std::ifstream m_read_stream;

  void start_write_stream(std::string fname);
};