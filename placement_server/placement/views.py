from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Program, Choice, Results, ConsiderationRequest, Placement
from .serializers import ProgramSerializer, ChoiceSerializer, ResultsSerializer, ConsiderationRequestSerializer, PlacementSerializer


class SubmitChoicesView(APIView):
    def post(self, request, student_id):
        choice = get_object_or_404(Choice, student_id=student_id)

        if choice.submitted:
            return JsonResponse({'error': 'Choices have already been submitted.'}, status=403)

        # Validate and set the choices before this point
        choice.submitted = True
        choice.save()

        # Get student email from request or related model
        student_email = request.data.get('email')  # Make sure email is passed in the request data
        if not student_email:
            return JsonResponse({'error': 'Email not provided.'}, status=400)

        # Send confirmation email
        self.send_confirmation_email(student_email, student_id, choice)

        return JsonResponse({'message': 'Choices submitted successfully.'}, status=200)

    def send_confirmation_email(self, email, student_id, choice):
        subject = 'Confirmation of Your Program Choices'
        message = f"Dear Student {student_id},\n\nYou have successfully submitted your choices:\n\n" \
                  f"First Choice: {choice.first_choice}\n" \
                  f"Second Choice: {choice.second_choice}\n" \
                  f"Third Choice: {choice.third_choice}\n\n" \
                  f"Thank you for your submission!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

class ProgramListCreateView(ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ChoiceListCreateView(ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ChoiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ResultsListCreateView(ListCreateAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer


class ResultsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer


class ConsiderationRequestListCreateView(ListCreateAPIView):
    queryset = ConsiderationRequest.objects.all()
    serializer_class = ConsiderationRequestSerializer


class ConsiderationRequestDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ConsiderationRequest.objects.all()
    serializer_class = ConsiderationRequestSerializer


class PlacementListCreateView(ListCreateAPIView):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer


class PlacementDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer


class UpdateChoicesView(APIView):
    def patch(self, request, student_id):
        choice = get_object_or_404(Choice, student_id=student_id)

        if choice.submitted:
            return JsonResponse({'error': 'Choices have already been submitted and cannot be changed.'}, status=403)

        # Here, add the logic to update the choice fields
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmitChoicesView(APIView):
    def post(self, request, student_id):
        choice = get_object_or_404(Choice, student_id=student_id)

        if choice.submitted:
            return JsonResponse({'error': 'Choices have already been submitted.'}, status=403)

        # Assuming you've validated and set the choices before this point
        choice.submitted = True
        choice.save()

        return JsonResponse({'message': 'Choices submitted successfully.'}, status=200)
