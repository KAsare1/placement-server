from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Program, Choice, Results, ConsiderationRequest, Placement
from .serializers import ProgramSerializer, ChoiceSerializer, ResultsSerializer, ConsiderationRequestSerializer, PlacementSerializer
import csv


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
        try:
            self.send_confirmation_email(student_email, student_id, choice)
        except Exception as e:
            # Log the error (you might want to use Python's logging module here)
            print(f"Error sending email: {str(e)}")
            return JsonResponse({'error': 'Failed to send confirmation email.'}, status=500)

        return JsonResponse({'message': 'Choices submitted successfully.'}, status=200)

    def send_confirmation_email(self, email, student_id, choice):
        subject = 'Confirmation of Your Program Choices'
        message = f"""Dear Student {student_id},

                    You have successfully submitted your choices:

                    First Choice: {choice.first_choice}
                    Second Choice: {choice.second_choice}
                    Third Choice: {choice.third_choice}

                    Thank you for your submission!"""
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    

class ProgramListCreateView(ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ChoiceListCreateView(ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        # Save the new Choice instance
        choice = serializer.save()

        # Get the email from the request payload
        email = serializer.validated_data.get('email')

        # Send an email using the provided email address
        send_mail(
            subject='Your Choices Have Been Submitted',
            message=f'Dear {choice.student},\n\nYou have successfully submitted your choices:\n1. {choice.first_choice}\n2. {choice.second_choice}\n3. {choice.third_choice}',
            from_email=settings.DEFAULT_FROM_EMAIL,  # Replace with your configured email address
            recipient_list=[email],  # Send email to the provided email
            fail_silently=False,
        )


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



class SaveChoiceView(APIView):
    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            # Save the choice
            choice = serializer.save()
            
            # Get the email from the serializer
            email = serializer.validated_data['email']
            
            # Compose the email message
            subject = "Your Program Choices"
            message = f"""
            Dear {choice.student},

            Your program choices have been recorded as follows:
            1st Choice: {choice.first_choice}
            2nd Choice: {choice.second_choice}
            3rd Choice: {choice.third_choice}

            Thank you for submitting your choices.
            """
            
            # Send the email
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                # Mark the choice as submitted
                choice.submitted = True
                choice.save()
                
                return Response({"message": "Choices saved and email sent successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # If email sending fails, we might want to delete the saved choice
                choice.delete()
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class ExportDataView(APIView):


    def get(self, request):
        # Create the HTTP response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="choices_data.csv"'

        writer = csv.writer(response)

        # Write the headers for the CSV
        writer.writerow(['Student', 'First Choice', 'Second Choice', 'Third Choice'])

        # Write the data rows from the Choice model
        for obj in Choice.objects.all():  # Adjust the queryset if necessary
            writer.writerow([obj.student, obj.first_choice, obj.second_choice, obj.third_choice])

        return response
