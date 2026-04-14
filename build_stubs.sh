#!/bin/bash

echo "Starting gRPC Python stub generation..."

# 1. Target the gRPC_demo app
PROTOS_DIR="./protos"
TARGET_DIR="./mysite/gRPC_demo/rpc"

# 2. Define the exact path to your virtual environment's Python executable
# (Change 'venv' to whatever your virtual environment folder is actually named, like '.venv' or 'env')
PYTHON_EXEC="./mysite/venv/bin/python"

# 3. Ensure the destination directory exists
echo "Creating target directory at $TARGET_DIR if it doesn't exist..."
mkdir -p "$TARGET_DIR"
touch "$TARGET_DIR/__init__.py"

# 4. Check if the venv python actually exists
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Error: Could not find Python executable at $PYTHON_EXEC."
    echo "Make sure your virtual environment is set up correctly."
    exit 1
fi

# 5. Run the protoc compiler using the VENV's Python!
echo "Compiling calculator.proto..."
$PYTHON_EXEC -m grpc_tools.protoc \
    -I"$PROTOS_DIR" \
    --python_out="$TARGET_DIR" \
    --grpc_python_out="$TARGET_DIR" \
    "$PROTOS_DIR/calculator.proto"

# 6. THE PATCH: Fix the broken gRPC import
# This finds the bad import line and adds the "." for a relative import
echo "Patching generated stubs for relative imports..."

# For Linux (Arch/Ubuntu)
sed -i 's/import calculator_pb2 as calculator__pb2/from . import calculator_pb2 as calculator__pb2/' "$TARGET_DIR/calculator_pb2_grpc.py"


echo "Success! Python stubs have been generated in $TARGET_DIR."
echo "(Remember: The C++ stubs are handled automatically by CMake when you build the server)"
