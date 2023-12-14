import base64
import io
import json
import numpy as np

from image_upload_processing.image_upload import UploadedImage

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers import PointsSerializer, FilesForMaskSerializer

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
    def post(self, request):
        files_serializer = FilesForMaskSerializer(data=request.data)
        if not files_serializer.is_valid():
            return Response(files_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = files_serializer.validated_data['image']
        print(f"Got image: {image.name}")
        json_file = files_serializer.validated_data['json']
        print(f"Got json file: {json_file.name}")
        json_data = json_file.read().decode('utf-8')

        try:
            parsed_json = json.loads(json_data)
        except:
            response_data = {"message": "Invalid json file"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        json_serializer = PointsSerializer(data=parsed_json)
        if not json_serializer.is_valid():
            return Response(json_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        positive_points = json_serializer.validated_data['pos_points']
        positive_points_array = np.array([[point['x'], point['y']] for point in positive_points])
        print(f"Pos points: {positive_points_array}")
        negative_points = json_serializer.validated_data['neg_points']
        negative_points_array = np.array([[point['x'], point['y']] for point in negative_points])
        print(f"Neg points: {negative_points_array}")

        try:
            image_byte_stream = io.BytesIO(image.read())
            uploaded_image = UploadedImage(image_byte_stream, positive_points_array, negative_points_array)
            uploaded_image.createImageEmbedding()
            uploaded_image.predictMasks()
            mask_byte_stream = uploaded_image.getMaskByteStream()
        except Exception as e:
            print("Error in image processing: ", str(e))
            response_data = {"message": "Error in image processing"}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    
        # Could use FileResponse (no json) instead to return smaller file and not have to encode
        encoded_mask = base64.b64encode(mask_byte_stream.read()).decode('utf-8')
        response_data = {
            "message": "Image mask",
            "image_data": encoded_mask,
        }
        return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')

