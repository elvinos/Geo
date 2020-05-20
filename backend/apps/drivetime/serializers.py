from rest_framework import serializers

STATUSES = (
    'New',
    'Ongoing',
    'Done',
)


class DriveTimeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=256)
#     owner = serializers.CharField(max_length=256)
#     status = serializers.ChoiceField(choices=STATUSES, default='New')