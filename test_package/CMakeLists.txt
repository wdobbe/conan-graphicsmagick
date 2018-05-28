project(test_package)
cmake_minimum_required(VERSION 3.9.0)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB SOURCE_FILES *.c)
include_directories(${CONAN_INCLUDE_DIRS_GRAPHICSMAGICK}/GraphicsMagick)
add_executable(${PROJECT_NAME} ${SOURCE_FILES})
message("conan libs: ${CONAN_LIBS}")
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})

