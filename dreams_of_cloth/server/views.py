from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers import UploadedImageSerializer

class PrintMessageView(APIView):
    """
    Print a message to the server terminal
    """
    def get(self, request, format=None):
        print("Server was pinged by client")
        response_data = {
            "message": "Message printed"
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class TemporaryImageView(APIView):
    """
    Receive an image from client for processing without persisting
    """
    def post(self, request, format=None):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            image_name = serializer.validated_data['image'].name
            print(f"Received image: {image_name}")
            response_data = {
                "message": "Image received"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

