from rest_framework import serializers
from app.models import Rubric


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = (
            "id",
            "name",
        )
