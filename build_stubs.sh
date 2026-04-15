#!/bin/bash

echo "Starting gRPC Python stub generation..."

# 1. Target directories
PROTOS_DIR="./protos"
TARGET_DIR="./mysite/gRPC_demo/rpc"

# 2. Python executable
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

# ==============================================================================
# THE UPGRADE: Loop through ALL .proto files in the protos directory
# ==============================================================================
for PROTO_FILE in "$PROTOS_DIR"/*.proto; do
    # Skip if no proto files are found (prevents bash errors)
    [ -e "$PROTO_FILE" ] || continue 

    # Extract just the filename without the .proto extension (e.g., "calculator")
    BASENAME=$(basename "$PROTO_FILE" .proto)

    echo "----------------------------------------"
    echo "Processing $BASENAME.proto..."
    
    # 5. Compile the specific proto file
    $PYTHON_EXEC -m grpc_tools.protoc \
        -I"$PROTOS_DIR" \
        --python_out="$TARGET_DIR" \
        --grpc_python_out="$TARGET_DIR" \
        "$PROTO_FILE"

    # 6. Apply the relative import patch dynamically
    echo "Patching $BASENAME generated stubs for relative imports..."
    sed -i "s/import ${BASENAME}_pb2 as ${BASENAME}__pb2/from . import ${BASENAME}_pb2 as ${BASENAME}__pb2/" "$TARGET_DIR/${BASENAME}_pb2_grpc.py"

done

echo "----------------------------------------"
echo "Success! All Python stubs have been generated and patched in $TARGET_DIR."
