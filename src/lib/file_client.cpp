#include "file_client.hpp"

using namespace std;

FileClient::FileClient() { start_write_stream(PENDING_FILE); }

FileClient::~FileClient() {
  // TODO: Close files here
}

void FileClient::start_write_stream(string fname) {
  m_write_stream.close();
  m_write_stream.open(fname);
}

Status FileClient::write(string body) { return Status(); }

FileIterator FileClient::read() {
  start_write_stream(TEMP_PENDING_FILE);
  return FileIterator();
}
