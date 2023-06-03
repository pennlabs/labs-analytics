#include "file_client.hpp"
#include <iostream>
#include <sstream>

using namespace std;

Status::Status(string detail) : m_detail(detail) {}

string Status::detail() { return m_detail; }

FileClient::FileClient() : m_curr_buf_size(0) {
  m_write_stream.open(WRITE_LOG);
}

FileClient::~FileClient() { m_write_stream.close(); }

FileIterator& FileClient::iterator() { return m_iterator; }

Status FileClient::write(string transaction) {
  if (transaction.length() == 0) {
    return Status::Error("Empty transactions are not allowed.");
  }

  stringstream ss;
  ss << DELIMITER << "\n" << transaction << "\n";

  int num_bytes = ss.str().length();

  if (num_bytes > BUFSIZ) {
    return Status::Error("Transaction exceeds capacity.");
  }

  // Flush if capacity is reached
  if (num_bytes + m_curr_buf_size > BUFSIZ) {
    m_write_stream.flush();
    m_curr_buf_size = 0;
  }

  m_write_stream << ss.str();
  m_curr_buf_size += num_bytes;

  return Status::Ok();
}

Status FileClient::force_flush() {
  m_write_stream.flush();
  return Status::Ok();
}

FileIterator::FileIterator()
    : m_checked_has_next(false), m_checked_get_next(false), m_next_body("") {
  // get last transaction id (position in the read file)
  ifstream error_log_reader(ERROR_LOG);
  error_log_reader.seekg(-1, ios_base::end);
  if (error_log_reader.peek() == '\n') {
    error_log_reader.seekg(-1, ios_base::cur);
    for (int i = error_log_reader.tellg(); i > 0; i--) {
      if (error_log_reader.peek() == '\n') {
        // found beginning of last line
        error_log_reader.get();
        break;
      }
      // move backwards
      error_log_reader.seekg(i, ios_base::beg);
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

string FileIterator::get_next() {

  // Return if there does not exist next
  if ((m_checked_has_next && !m_has_next) || !this->has_next()) {
    // TODO: Should throw useful error here
    // Or even better, make a well structured Status class and return Status
    // here
    return "";
  }

  if (m_checked_get_next) {
    return m_next_body;
  }

  m_checked_get_next = true;

  stringstream ss;
  string line;

  streampos pos = m_read_stream.tellg();

  // Read the first delimiter
  m_read_stream >> line;

  streampos curr_pos;
  // NOTE: This produces an extra whitespace for the last line.
  // Hopefully when we move to JSON this shouldn't be a problem
  while ((m_read_stream >> line) && line != DELIMITER) {
    curr_pos = m_read_stream.tellg();
    ss << line << "\n";
  }

  m_read_stream.seekg(pos, ios_base::beg);

  m_end_pos = curr_pos;
  m_next_body = ss.str();

  return ss.str();
}

bool FileIterator::has_next() {

  if (m_checked_has_next) {
    return m_has_next;
  }

  m_checked_has_next = true;

  string token;

  streampos pos = m_read_stream.tellg();

  if ((m_read_stream >> token) && token == DELIMITER) {
    m_read_stream.seekg(pos, ios_base::beg);
    m_has_next = true;
    return true;
  }

  m_has_next = false;
  return false;
}

Status FileIterator::commit(Status status) {
  if (!m_checked_get_next || this->get_next().length() == 0) {
    return Status::Error("Nothing to Commit");
  }

  // TODO: Write to error log here

  m_read_stream.seekg(m_end_pos, ios_base::beg);

  // Invalidate cached data
  m_checked_has_next = false;
  m_checked_get_next = false;

  return Status::Ok();
}
