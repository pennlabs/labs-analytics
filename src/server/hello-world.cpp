#include "src/lib/hello-time.hpp"
#include "hello-greet.hpp"
#include <iostream>
#include <string>
#include <boost/algorithm/string.hpp>

using namespace std;

int main(int argc, char** argv) {
  string who = "world";
  if (argc > 1) {
    who = argv[1];
  }

  auto test_string = "test_string";

  auto greet = get_greet(who);

  cout << greet << endl;

  // Check if the string starts with "Hello"
  bool startsWithHello = boost::algorithm::starts_with(greet, "Hello");
  cout << "Starts with \"Hello\": " << (startsWithHello ? "Yes" : "No") << endl;

  print_localtime();

  return 0;
}
