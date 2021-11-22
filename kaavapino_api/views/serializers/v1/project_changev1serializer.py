from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
            Example 09100399030101 is
            """,
            value={"datanomistaja": "Helsinki/Kami"},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class ProjectChangeV1Serializer(serializers.Serializer):
    Identifier = serializers.CharField(max_length=255)
    Changed = serializers.DateField()


class ProjectChangesV1Serializer(serializers.Serializer):
    Changes = ProjectChangeV1Serializer(read_only=True, many=True)
