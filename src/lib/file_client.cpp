#include "file_client.hpp"
#include <iostream>

using namespace std;

FileClient::FileClient() : m_curr_buf_size(0) {
  m_write_stream.open(WRITE_LOG);
}

FileClient::~FileClient() { m_write_stream.close(); }

FileIterator& FileClient::iterator() { return m_iterator; }

Status FileClient::write(string transaction) {
  // TODO: write deliminter
  int num_bytes = transaction.length();

  if (num_bytes > BUFSIZ) {
    return Status::Error("Transaction exceeds capacity.");
  }

  // Flush if capacity is reached
  if (num_bytes + m_curr_buf_size > BUFSIZ) {
    m_write_stream.flush();
    m_curr_buf_size = 0;
  }

  m_write_stream << transaction << "\n";
  m_curr_buf_size += num_bytes;

  return Status::Ok();
}

FileIterator::FileIterator() : m_has_commited(true), m_checked_next(false) {
  // get last transaction id (position in the read file)
  ifstream error_log_reader(ERROR_LOG);
  error_log_reader.seekg(-1, std::ios_base::end);
  if (error_log_reader.peek() == '\n') {
    error_log_reader.seekg(-1, std::ios_base::cur);
    for (int i = error_log_reader.tellg(); i > 0; i--) {
      if (error_log_reader.peek() == '\n') {
        // found beginning of last line
        error_log_reader.get();
        break;
      }
      // move backwards
      error_log_reader.seekg(i, std::ios_base::beg);
    }
    error_log_reader >> m_next_transaction_id;
  } else {
    m_next_transaction_id = 0;
  }
  error_log_reader.close();
  m_read_stream.open(WRITE_LOG);
  m_read_stream.seekg(m_next_transaction_id);
  m_commit_stream.open(ERROR_LOG, ios::app);
}

FileIterator::~FileIterator() {
  m_read_stream.close();
  m_commit_stream.close();
}

void FileIterator::restart_stream() {
  m_read_stream.close();
  m_read_stream.open(WRITE_LOG);
  m_read_stream.seekg(m_next_transaction_id);
}

std::string FileIterator::get_next() {

  // has_next

  /*
   ඞ\n
   {

   }
   ඞ\n
   {

   }
   ඞ\n
   {

   }
   ඞ\n
   {

   }

  */

  m_checked_next = false;
  m_has_commited = false;
  return "";
}

Status FileIterator::has_next() {
  if (m_checked_next && m_has_next) {
    return Status::Ok();
  } else if (m_checked_next && !m_has_next) {
    restart_stream();
    return Status::Ok();
  } else {
    char tmp[2];
    // TODO:

    // otherwise, move backwards
    return Status::Ok();
  }
}

Status FileIterator::commit(Status status) {
  if (!m_has_commited) {
    return Status::Error("Already commited for this transaction.");
  }
  m_has_commited = true;
  m_next_transaction_id = m_read_stream.tellg();
  m_commit_stream << m_next_transaction_id << " "
                  << "error";
  return Status::Ok();
}
