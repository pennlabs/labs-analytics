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

  FileClient fc;
  fc.write("hello\ntest\nyes sir");
  fc.write("another\nyou know\n how it goes");

  fc.force_flush();

  FileIterator fi;

  fi.has_next();
  fi.has_next();
  fi.has_next();
  fi.has_next();

  cout << fi.get_next() << endl;
  cout << fi.get_next() << endl;

  fi.commit(Status::Ok());

  cout << fi.get_next() << endl;
  cout << fi.get_next() << endl;

  fi.commit(Status::Ok());

  cout << fi.has_next() << endl;

  return 0;
}
