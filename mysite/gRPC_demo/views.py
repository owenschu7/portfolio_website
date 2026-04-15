from django.shortcuts import render
import grpc

# import your generated stubs from the local rpc folder
from .rpc import calculator_pb2
from .rpc import calculator_pb2_grpc
from .rpc import baccaratSim_pb2
from .rpc import baccaratSim_pb2_grpc

# init the gRPC channel once at the module level
grpc_channel = grpc.insecure_channel('localhost:50051')

# init the stubs for both services
calculator_stub = calculator_pb2_grpc.CalculatorServiceStub(grpc_channel)
baccarat_stub = baccaratSim_pb2_grpc.BaccaratEngineStub(grpc_channel)

# Create your views here.
def gRPC_view(request):
    context = {}

    if request.method == 'POST':
        # Check which button was actually pressed
        action = request.POST.get('action')

        if action == 'calculate':
            try:
                # Get and cast the data to the correct type
                num_a = int(request.POST.get('num_a', 0))
                num_b = int(request.POST.get('num_b', 0))
                context['a'] = num_a
                context['b'] = num_b

                # Build the payload
                grpc_request = calculator_pb2.MultiplyRequest(a=num_a, b=num_b)

                # Execute the call with error handling
                response = calculator_stub.Multiply(grpc_request, timeout=3.0)
                context['calc_result'] = response.result

            except ValueError:
                context['calc_error'] = "Invalid input. Please enter numbers."
            except grpc.RpcError as e:
                # Catch gRPC specific errors (e.g., server offline, timeout)
                context['calc_error'] = f"gRPC Error: {e.code().name} - {e.details()}"

        elif action == 'deal':
            try:
                # Get and cast data
                num_hands = int(request.POST.get('num_hands', 0))
                context['num_hands'] = num_hands

                # Build payload
                grpc_request = baccaratSim_pb2.SimRequest(number_of_hands=num_hands)

                # Execute call
                response = baccarat_stub.SimulateBaccarat(grpc_request, timeout=10.0)
                # Extract the result
                # Format into a multiline string for the template's {{ result|linebreaksbr }}
                context['deal_result'] = (
                    f"Player Wins: {response.player_wins}\n"
                    f"Banker Wins: {response.banker_wins}\n"
                    f"Ties: {response.ties}\n"
                    f"Pandas: {response.pandas}\n"
                    f"Dragons: {response.dragons}\n"
                    f"Execution Time: {response.execution_time_ms} ms"
                )

            except ValueError:
                context['deal_error'] = "Invalid input. Please enter a whole number."
            except grpc.RpcError as e:
                context['deal_error'] = f"gRPC Error: {e.code().name} - {e.details()}"
        #add other button actions here

    return render(request, 'gRPC_demo/gRPC_demo.html', context)





