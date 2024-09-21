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
    email = serializers.CharField(write_only=True)
    class Meta:
        model = Choice
        fields = ('student', 'first_choice', 'second_choice', 'third_choice', 'email')

    def create(self, validated_data):
        email = validated_data.pop('email')  # Remove email from validated data

        # Create the Choice instance without the email field
        choice = Choice.objects.create(**validated_data)

        # You can now send the email after creating the choice if needed
        # Optionally, you could return choice and handle email sending in your view

        return choice

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
