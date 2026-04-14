# ==============================================================================
# 1. Project Setup
# ==============================================================================
cmake_minimum_required(VERSION 3.15)
project(PortfolioGrpcServer CXX)

# gRPC heavily utilizes modern C++ features. C++17 is recommended.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# ==============================================================================
# 2. Find Dependencies (Protobuf and gRPC)
# ==============================================================================
# These assume you installed gRPC and Protobuf on your system/Docker builder
find_package(Threads REQUIRED)
find_package(Protobuf CONFIG REQUIRED)
find_package(gRPC CONFIG REQUIRED)

# ==============================================================================
# 3. Monorepo Paths Configuration
# ==============================================================================
# Point to the shared protos directory at the root of the monorepo
set(PROTOS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../protos")
set(PROTO_FILE "${PROTOS_DIR}/calculator.proto")

# We will generate the .pb.cc and .pb.h files into the build directory
# so we don't clutter our source tree.
set(GEN_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
file(MAKE_DIRECTORY ${GEN_DIR})

set(PROTO_SRCS "${GEN_DIR}/calculator.pb.cc" "${GEN_DIR}/calculator.grpc.pb.cc")
set(PROTO_HDRS "${GEN_DIR}/calculator.pb.h" "${GEN_DIR}/calculator.grpc.pb.h")

# ==============================================================================
# 4. Generate C++ Stubs from .proto
# ==============================================================================
# This tells CMake exactly how to run the 'protoc' compiler automatically
# every time you build, so you don't have to run it manually.
add_custom_command(
    OUTPUT ${PROTO_SRCS} ${PROTO_HDRS}
    COMMAND protobuf::protoc
    ARGS --grpc_out=${GEN_DIR}
         --cpp_out=${GEN_DIR}
         -I ${PROTOS_DIR}
         --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
         ${PROTO_FILE}
    DEPENDS ${PROTO_FILE}
    COMMENT "Generating C++ gRPC stubs from service.proto"
)

# ==============================================================================
# 5. Define the Executable
# ==============================================================================
# Tell CMake to compile your main server logic AND the auto-generated stubs
add_executable(my_grpc_server
    src/main.cpp
    # src/casino_logic.cpp  <-- Add your other source files here
    ${PROTO_SRCS}
)

# ==============================================================================
# 6. Include Directories & Linking
# ==============================================================================
# Tell the compiler where to find headers (both yours and the generated ones)
target_include_directories(my_grpc_server PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${GEN_DIR}
)

# Link the gRPC, Protobuf, and Threading libraries to your executable
target_link_libraries(my_grpc_server PRIVATE
    gRPC::grpc++
    gRPC::grpc++_reflection
    protobuf::libprotobuf
    Threads::Threads
)
