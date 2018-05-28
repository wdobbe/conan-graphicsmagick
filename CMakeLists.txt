PROJECT(conan-cpprestsdk)

MESSAGE(WARNING "Conan CppRestSDK Wrapped CMake")
cmake_minimum_required(VERSION 3.10.0)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

## Find Boost and zlib 
#if (WIN32)
#    if (NOT CPPREST_EXCLUDE_WEBSOCKETS)
#        find_package(Boost 1.66 COMPONENTS system date_time regex REQUIRED)
#    endif()

#    set(ZLIB_ROOT ${CONAN_ZLIB_ROOT})
#    set(ZLIB_LIBRARYDIR ${CONAN_LIB_DIRS_ZLIB})
#    find_package(ZLIB REQUIRED)
#endif(WIN32)

add_subdirectory("cpprestsdk-${CPPRESTSDK_VERSION}/Release")
