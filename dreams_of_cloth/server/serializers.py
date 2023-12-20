from rest_framework import serializers

class PointSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()

class PointsSerializer(serializers.Serializer):
    pos_points = PointSerializer(many=True)
    neg_points = PointSerializer(many=True)

class BoxSerializer(serializers.Serializer):
    point1 = PointSerializer()
    point2 = PointSerializer()

class MaskPredictInputsSerializer(serializers.Serializer):
    points = PointsSerializer(required=False)
    box = BoxSerializer(required=False)

class FilesForMaskSerializer(serializers.Serializer):
    json = serializers.FileField(allow_empty_file=False, required=True)
    image = serializers.ImageField()