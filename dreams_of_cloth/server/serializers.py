from rest_framework import serializers

class UploadedImageSerializer(serializers.Serializer):
    image = serializers.ImageField()