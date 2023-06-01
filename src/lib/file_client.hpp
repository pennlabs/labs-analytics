#include "file_serializer.hpp"
#include <fstream>
#include <string>

#define DELIMITER "ඞ\n"

#define WRITE_LOG "./logs/write_log"
#define ERROR_LOG "./logs/error_log"

#define BUFFER_SIZE 4096;

class Status {
public:
  Status();

  std::string detail();

  static Status Ok(std::string detail = "success");
  static Status Error(std::string detail = "error");
};

class FileIterator {
public:
  FileIterator();

  ~FileIterator();

  Status has_next();
  std::string get_next();
  Status commit(Status status);

private:
  bool m_has_commited;
  bool m_checked_next;
  bool m_has_next;

  void restart_stream();

  std::ofstream m_commit_stream;
  std::ifstream m_read_stream;
  unsigned long m_next_transaction_id;
};

class FileClient {
public:
  FileClient();

  ~FileClient();

  FileIterator& iterator();

  Status write(std::string transaction);

private:
  int m_curr_buf_size;

  std::ofstream m_write_stream;

  FileIterator m_iterator;
};
