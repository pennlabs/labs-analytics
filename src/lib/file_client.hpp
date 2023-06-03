#include "file_serializer.hpp"
#include <fstream>
#include <string>

#define DELIMITER "ඞ"

#define WRITE_LOG "./logs/write_log"
#define ERROR_LOG "./logs/error_log"

#define BUFFER_SIZE 4096;

class Status {
public:
  Status(std::string detail);

  std::string detail();

  static Status Ok(std::string detail = "success") { return Status(detail); }
  static Status Error(std::string detail = "error") { return Status(detail); }

private:
  std::string m_detail;
};

class FileIterator {
public:
  FileIterator();

  ~FileIterator();

  bool has_next();
  std::string get_next();
  Status commit(Status status);

private:
  bool m_checked_has_next;
  bool m_has_next;

  bool m_checked_get_next;
  std::string m_next_body;
  std::streampos m_end_pos;

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

  Status force_flush();

private:
  int m_curr_buf_size;

  std::ofstream m_write_stream;

  FileIterator m_iterator;
};
