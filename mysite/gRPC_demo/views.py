from django.shortcuts import render
import grpc

# import your generated stubs from the local rpc folder
from .rpc import calculator_pb2
from .rpc import calculator_pb2_grpc

# Create your views here.
def gRPC_view(request):
    # Default context to pass to the HTML template
    context = {
        'a': '',
        'b': '',
        'result': None,
        'error': None
    }

    if request.method == 'POST':
        try:
            # 1. Grab the inputs from the HTML form
            a_val = int(request.POST.get('num_a', 0))
            b_val = int(request.POST.get('num_b', 0))
            
            # Save them in context so the form doesn't clear after clicking submit
            context['a'] = a_val
            context['b'] = b_val

            # 2. Open the gRPC channel to your C++ server
            # (Assuming your C++ server is running locally on port 50051)
            with grpc.insecure_channel('localhost:50051') as channel:
                # 3. Create the Stub (the diplomat)
                stub = calculator_pb2_grpc.CalculatorServiceStub(channel)

                # 4. Build the payload using the Protobuf classes
                grpc_request = calculator_pb2.MultiplyRequest(a=a_val, b=b_val)

                # 5. Execute the remote procedure call!
                response = stub.Multiply(grpc_request, timeout=3.0)

                # 6. Extract the result
                context['result'] = response.result

        except ValueError:
            context['error'] = "Please enter valid whole numbers."
        except grpc.RpcError as e:
            # Catches issues like the C++ server being offline
            context['error'] = f"Backend Connection Failed: {e.details()}"

    # Render the template and pass the context data
    return render(request, 'gRPC_demo/gRPC_demo.html', context)


