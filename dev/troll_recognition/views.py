from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .recognition_core import predict_is_troll


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import time

class TrollPredictionView(APIView):

    @swagger_auto_schema(
        operation_description="Check if a list of text messages are from troll accounts",
        operation_id="predict_get",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'account': openapi.Schema(type=openapi.TYPE_STRING, description='Account name'),
                    'tweet': openapi.Schema(type=openapi.TYPE_STRING, description='Text of the tweet')
                },
                required=['account', 'tweet']
            )
        ),
        responses={
            200: openapi.Response(
                description="Prediction results",
                examples={
                    "application/json": {
                        "is_troll": True,
                        "confidence": 0.87
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request. Less than 10 tweets specified."
            )
        }
    )
    def post(self, request):
        from .apps import TrollRecognitionConfig
        input_data = request.data
        
        if not input_data:
            return Response({"error": "No input data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        start_time = time.time()
        result = predict_is_troll(TrollRecognitionConfig.model, input_data)
        execution_time = round(time.time() - start_time, 4)
        
        response_object = {"is_troll": None, "confidence": None, "elapsed_time": None}

        if result is not None:
            response_object["is_troll"], response_object['confidence'], response_object["elapsed_time"] = result

        #print("RESPONSE")
        #print(response_object)

        return Response(response_object, status=status.HTTP_200_OK if result is not None else status.HTTP_400_BAD_REQUEST)
    