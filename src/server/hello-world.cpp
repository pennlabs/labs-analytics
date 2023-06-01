#include "hello-greet.hpp"
#include "src/lib/file_client.hpp"
#include "src/lib/hello-time.hpp"
#include <boost/algorithm/string.hpp>
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char** argv) {
  /*string who = "world";
  if (argc > 1) {
    who = argv[1];
  }

  auto test_string = "test_string";

  auto greet = get_greet(who);

  cout << greet << endl;

  // Check if the string starts with "Hello"
  bool startsWithHello = boost::algorithm::starts_with(greet, "Hello");
  cout << "Starts with \"Hello\": " << (startsWithHello ? "Yes" : "No") << endl;

  if (true) {
  }

  char* x;

  print_localtime();*/

  FileClient f;

  f.start_read_stream();
  cout << f.m_next_transaction_id << endl;

  return 0;
}
