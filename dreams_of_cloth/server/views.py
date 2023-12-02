import base64
import io
import json
import numpy as np

from image_upload_processing.image_upload import UploadedImage

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers import UploadedImageSerializer, PointsSerializer, TestComplexSerializer
from rest_framework.parsers import MultiPartParser

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
    
class GetObjectMaskView(APIView):
    """
    Receive an image, positive points and negative points from client and return mask of object
    """
    def post(self, request, format=None):
        serializer = UploadedImageSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            # Getting image data
            image_name = serializer.validated_data['image'].name
            uploaded_image = serializer.validated_data['image']
            uploaded_image_byte_stream = io.BytesIO(uploaded_image.read())
            print(f"Got image: {image_name}")
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
    
class TestNestedJSONView(APIView):
    def post(self, request):
        print(request.data)
        serializer = PointsSerializer(data=request.data)
        if serializer.is_valid():
            response_data = {
                "message": "test"
            }
            return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TestComplexView(APIView):
    def post(self, request):
        files_serializer = TestComplexSerializer(data=request.data)
        if files_serializer.is_valid():
            image = files_serializer.validated_data['image']
            print(f"Got image: {image.name}")
            json_file = files_serializer.validated_data['json']
            print(f"Got json file: {json_file.name}")
            json_data = json_file.read().decode('utf-8')
            try:
                parsed_json = json.loads(json_data)
                json_serializer = PointsSerializer(data=parsed_json)
                if json_serializer.is_valid():
                    positive_points = json_serializer['pos_points']
                    # positive_points = np.array([[point['x'], point['y']] for point in positive_points])
                    print(f"Pos points: {positive_points}")
                    negative_points = json_serializer['neg_points']
                    print(f"Neg points: {negative_points}")
                else:
                    Response(json_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                response_data = {"message": "Invalid json file"}
                Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response_data = {"message": "test"}
        return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')

