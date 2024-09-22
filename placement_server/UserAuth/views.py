from datetime import timezone
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .models import ConfirmationCode
from .serializers import ConfirmEmailSerializer, ConfirmationSerializer, StudentRegistrationSerializer, UserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStudent, IsHOD, IsDean
from django.contrib.auth import get_user_model

User = get_user_model()

class UserListView(APIView):  # Require authentication to view users

    def get(self, request):
        users = User.objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)  # Serialize multiple users
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentDetailView(APIView):

    def get(self, request, student_id):
        try:
            user = User.objects.get(student_id=student_id)  # Fetch user by student_id
            serializer = UserSerializer(user)  # Serialize the user data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)


class StudentRegistrationView(APIView):
    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create and send confirmation code
            confirmation_code = ConfirmationCode.objects.create(user=user)
            code = confirmation_code.generate_code()
            send_mail(
                'Email Confirmation Code',
                f'Your confirmation code is {code}',
                settings.DEFAULT_FROM_EMAIL,
                'groupminiproject13@gmail.com',
                fail_silently=True,
            )
            return Response({"detail": "Registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        password = request.data.get('password')

        user = authenticate(student_id=student_id, password=password)

        if user is not None:
            if user.is_active or False:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User account is not active."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"https://yourfrontend.com/reset-password/{uid}/{token}"

            send_mail(
                'Reset Your Password',
                f'Click the following link to reset your password: {reset_link}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)


class ResendConfirmationCodeView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        try:
            user = User.objects.get(student_id=student_id, is_active=False)
            confirmation = ConfirmationCode.objects.get(user=user)
            
            # Generate new code
            new_code = confirmation.generate_code()
            
            # Send new confirmation email
            send_mail(
                'New Confirmation Code',
                f'Your new confirmation code is: {new_code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            
            return Response({"message": "New confirmation code sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found or already active."}, status=status.HTTP_404_NOT_FOUND)
        except ConfirmationCode.DoesNotExist:
            return Response({"error": "Confirmation code not found."}, status=status.HTTP_404_NOT_FOUND)
        
class ConfirmEmailView(APIView):
    def post(self, request):
        serializer = ConfirmEmailSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            try:
                confirmation_code = ConfirmationCode.objects.get(code=code, is_verified=False)
                user = confirmation_code.user
                user.is_active = True  # Activate the user
                user.save()
                confirmation_code.is_verified = True
                confirmation_code.save()
                return Response({"detail": "Email successfully confirmed."}, status=status.HTTP_200_OK)
            except ConfirmationCode.DoesNotExist:
                return Response({"detail": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ConfirmRegistrationView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        code = request.data.get('code')
        
        try:
            user = User.objects.get(student_id=student_id)
            confirmation = ConfirmationCode.objects.get(user=user, code=code)
            
            # Activate the user
            user.is_active = True
            user.save()
            
            # Mark the confirmation code as verified
            confirmation.is_verified = True
            confirmation.save()
            
            return Response({"message": "User activated successfully."}, status=status.HTTP_200_OK)
        except (User.DoesNotExist, ConfirmationCode.DoesNotExist):
            return Response({"error": "Invalid student ID or confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
        





class StudentOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        # Logic for students
        return Response({"message": "Hello Student"})

class HODOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsHOD]

    def get(self, request):
        # Logic for HOD
        return Response({"message": "Hello HOD"})

class DeanOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsDean]

    def get(self, request):
        # Logic for Dean
        return Response({"message": "Hello Dean"})


