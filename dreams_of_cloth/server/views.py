import base64
import io

from image_upload_processing.image_upload import UploadedImage

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
        return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')
    
class TemporaryImageView(APIView):
    """
    Receive an image from client for processing without persisting
    """
    def post(self, request, format=None):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            image_name = serializer.validated_data['image'].name
            print(f"Received image: {image_name}")
            uploaded_image = serializer.validated_data['image']
            uploaded_image_byte_stream = io.BytesIO(uploaded_image.read())
            uploaded_image = UploadedImage(uploaded_image_byte_stream)
            uploaded_image.createImageEmbedding()
            uploaded_image.predictMasks()
            mask_byte_stream = uploaded_image.getMaskByteStream()
            # Could use FileResponse (no json) instead to return smaller file and not have to encode
            encoded_mask = base64.b64encode(mask_byte_stream.read()).decode('utf-8')
            response_data = {
                "message": "Image mask",
                "image_data": encoded_mask,
            }
            return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

