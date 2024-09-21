from rest_framework import serializers
from .models import Program, Choice, Results, ConsiderationRequest, Placement


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('id', 'program_type', 'major', 'second_major', 'minor', 'program')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['program_type'] = instance.get_program_type_display()
        return representation


class ChoiceSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    class Meta:
        model = Choice
        fields = ('student', 'first_choice', 'second_choice', 'third_choice', 'email')

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = ('student', 'students_id', 'results', 'CGPA')


class ConsiderationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsiderationRequest
        fields = ('student', 'Results', 'CGPA', 'choice', 'explanation')


class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = ('student', 'placement')
