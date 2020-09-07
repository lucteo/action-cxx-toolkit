cmake_minimum_required(VERSION 3.0)

project(test_app)


add_executable(test_app main.cpp)

enable_testing()
add_test(NAME my_simple_test COMMAND test_app)