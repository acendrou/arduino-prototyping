cmake_minimum_required(VERSION 3.25)
project(dummy_for_tests_c)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_EXE_LINKER_FLAGS "--static -static-libgcc -static-libstdc++")

add_executable(dummy_for_tests_c main.cpp)
