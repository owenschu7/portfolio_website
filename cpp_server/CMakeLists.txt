# ==============================================================================
# 1. Project Setup
# ==============================================================================
cmake_minimum_required(VERSION 3.15)
project(PortfolioGrpcServer CXX)

# for lsp to not throw a bunch of errors
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

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
set(PROTOS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../protos")
set(GEN_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
file(MAKE_DIRECTORY ${GEN_DIR})

# Add ALL your proto files to this list (no extensions needed here)
set(PROTO_NAMES
    "calculator"
    "baccaratSim"
)

# Initialize empty lists to hold the generated file paths
set(PROTO_SRCS "")
set(PROTO_HDRS "")

# ==============================================================================
# 4. Generate C++ Stubs from .proto
# ==============================================================================
foreach(PROTO_NAME IN LISTS PROTO_NAMES)
    set(PROTO_FILE "${PROTOS_DIR}/${PROTO_NAME}.proto")
    
    set(CC_FILE "${GEN_DIR}/${PROTO_NAME}.pb.cc")
    set(GRPC_CC_FILE "${GEN_DIR}/${PROTO_NAME}.grpc.pb.cc")
    set(H_FILE "${GEN_DIR}/${PROTO_NAME}.pb.h")
    set(GRPC_H_FILE "${GEN_DIR}/${PROTO_NAME}.grpc.pb.h")

    # Append to the master lists
    list(APPEND PROTO_SRCS ${CC_FILE} ${GRPC_CC_FILE})
    list(APPEND PROTO_HDRS ${H_FILE} ${GRPC_H_FILE})

    # Tell CMake how to generate these specific files
    add_custom_command(
        OUTPUT ${CC_FILE} ${GRPC_CC_FILE} ${H_FILE} ${GRPC_H_FILE}
        COMMAND protobuf::protoc
        ARGS --grpc_out=${GEN_DIR}
             --cpp_out=${GEN_DIR}
             -I ${PROTOS_DIR}
             --plugin=protoc-gen-grpc=$<TARGET_FILE:gRPC::grpc_cpp_plugin>
             ${PROTO_FILE}
        DEPENDS ${PROTO_FILE}
        COMMENT "Generating C++ gRPC stubs from ${PROTO_NAME}.proto"
    )
endforeach()

# ==============================================================================
# 5. Define the Executable
# ==============================================================================
# Tell CMake to compile your main server logic AND the auto-generated stubs
add_executable(my_grpc_server
    src/main.cpp
    include/baccarat_table.cpp
    include/baccarat_hand.cpp
    include/deck.cpp
    include/card.cpp
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
