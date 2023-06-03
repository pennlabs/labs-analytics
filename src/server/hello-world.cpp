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

  // Writes 2 transactions to file
  FileClient fc;
  fc.write("transaction\nnumber one\nextra line");
  fc.write("transaction\nnumber two\nanother line");
  fc.force_flush();

  FileIterator fi1;

  cout << "Should have next" << endl;
  cout << fi1.has_next() << endl;
  cout << fi1.has_next() << endl;

  cout << "Should return the same" << endl;
  cout << fi1.get_next() << endl;
  cout << fi1.get_next() << endl;

  // Now moves to second transaction
  fi1.commit(Status::Ok());

  // This shouldn't affect anything
  fi1.restart_stream();

  cout << "Committed, should be next" << endl;
  cout << fi1.get_next() << endl;
  cout << fi1.get_next() << endl;

  // Now moves to third transaction
  fi1.commit(Status::Ok());

  fc.write("transaction\nnumber three\nthird line");
  fc.force_flush();

  cout << "Should return false because ifstream does not have updated file"
       << endl;
  cout << fi1.has_next() << endl;

  FileIterator fi2;

  cout << "Should pick up on transaction 3" << endl;
  cout << fi2.has_next() << endl;
  cout << fi2.has_next() << endl;

  cout << fi2.get_next() << endl;
  cout << fi2.get_next() << endl;

  fi2.commit(Status::Ok());

  cout << "Should be false" << endl;
  cout << fi2.has_next() << endl;

  return 0;
}
