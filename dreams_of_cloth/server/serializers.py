from rest_framework import serializers

class PointSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()

class PointsSerializer(serializers.Serializer):
    pos_points = PointSerializer(many=True)
    neg_points = PointSerializer(many=True)

class UploadedImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

class TestComplexSerializer(serializers.Serializer):
    json = serializers.FileField(allow_empty_file=False, required=True)
    image = serializers.ImageField()