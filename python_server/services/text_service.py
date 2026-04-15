import text_processor_pb2
import text_processor_pb2_grpc
import logging

class TextServiceServicer(text_processor_pb2_grpc.TextServiceServicer):
    def ProcessText(self, request, context):
        # request.input_text will contain the "genre" sent from your Django form
        genre = request.input_text
        logging.info(f"Received request to generate lyrics for genre: {genre}")
        
        try:
            # =========================================================
            # YOUR AI LOGIC GOES HERE
            # e.g., result = my_ai_client.generate(prompt=f"Write a {genre} song")
            # =========================================================
            
            # Placeholder logic until you hook up the real AI call
            mock_lyrics = f"(Verse 1)\nPlaying that {genre} rhythm all night long...\n(Chorus)\nYeah, this is the {genre} song!"
            
            logging.info("Successfully generated lyrics.")
            return text_processor_pb2.TextResponse(output_text=mock_lyrics)
            
        except Exception as e:
            # If the AI call fails, log it and return the error string back to Django
            logging.error(f"Failed to generate lyrics: {str(e)}")
            
            # You can use gRPC status codes to tell the client something went wrong
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"AI generation failed: {str(e)}")
            
            return text_processor_pb2.TextResponse(output_text="Error occurred during generation.")
