#!/usr/bin/env python3
import grpc
from concurrent import futures
import logging
import signal
import sys
import time

# Import the generated gRPC stubs (ensure these are generated in your python_server directory)
import text_processor_pb2_grpc

# Import your actual business logic
from services.text_service import TextServiceServicer

def serve():
    # 1. Setup logging so you can see what's happening in your terminal
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # 2. Create the gRPC server with a thread pool
    # 10 workers is plenty for most standard AI generation queues
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # 3. Attach your specific text processing service to the server
    text_processor_pb2_grpc.add_TextServiceServicer_to_server(TextServiceServicer(), server)
    
    # 4. Bind to a port
    port = '[::]:50051'
    server.add_insecure_port(port)
    
    # 5. Start the server
    server.start()
    logging.info(f"Python gRPC Server listening on {port}...")
    
    # 6. Graceful shutdown handler for when you hit Ctrl+C (SIGINT)
    def handle_sigterm(*args):
        logging.info("Received shutdown signal. Stopping server gracefully...")
        # Give active requests 5 seconds to finish before killing the process
        done_event = server.stop(5)
        done_event.wait()
        logging.info("Server stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)

    # 7. Keep the main thread alive
    try:
        # Sleep loop prevents the main thread from exiting
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        handle_sigterm()

if __name__ == '__main__':
    serve()
