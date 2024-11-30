from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, LoginSerializer, EmptySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer


# ---------------------------- JWT endpoints ----------------------------

@extend_schema(tags=["Auth - Token"])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=["Auth - Token"])
class CustomTokenRefreshView(TokenRefreshView):
    pass

@extend_schema(tags=["Auth - Token"])
class CustomTokenVerifyView(TokenVerifyView):
    pass

# ---------------------------- Authentication Endpoints ----------------------------

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer 

    @extend_schema(
        tags=["Auth - Registration"],
        summary="User Registration",
        description="Registers a new user and sends a verification link.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "The username for the new user"},
                    "email": {"type": "string", "description": "The email for the new user"},
                    "password": {"type": "string", "description": "The password for the new user"},
                    "password2": {"type": "string", "description": "Confirm password"}
                },
                "required": ["username", "email", "password", "password2"]
            }
        }
    )
    def post(self, request):
        password1 = request.data.get("password")
        password2 = request.data.get("password2")

        # Validate that passwords match
        if password1 != password2:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  

        # Create a verification link
        verification_link = f"http://127.0.0.1:8000/auth/api/verify-email/?user_id={user.id}"
        print(f"Verification Link: {verification_link}")

        return Response(
            {"message": "User registered successfully. Please verify your email."},
            status=status.HTTP_201_CREATED
        )

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmptySerializer

    @extend_schema(
        tags=["Auth - Registration"],
        summary="Verify Email",
        description="Activates a user account after email verification."
    )
    def get(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response({"error": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                return Response({"message": "User is already verified."}, status=status.HTTP_200_OK)
            user.is_active = True
            user.save()
            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid user ID."}, status=status.HTTP_404_NOT_FOUND)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Replace with actual serializer class for login

    @extend_schema(
        tags=["Auth - Login/Logout"],
        summary="Login",
        description="Logs in a user and returns a JWT token."
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Token generation logic
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer
    
    @extend_schema(
        tags=["Auth - Login/Logout"],
        summary="Logout",
        description="Logs out a user by blacklisting the refresh token."
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------- Password Management Endpoints ----------------------------

class ForgotPasswordView(APIView):
    @extend_schema(
        tags=["Auth - Password"],
        summary="Forgot Password",
        description="Sends a password reset link to the user's email."
    )
    def post(self, request):
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)
        send_mail(
            "Reset your password",
            f"Click the link to reset your password: http://example.com/reset-password/?user_id={user.id}",
            "no-reply@example.com",
            [email],
        )
        return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    @extend_schema(
        tags=["Auth - Password"],
        summary="Reset Password",
        description="Resets the user's password using the provided user ID and new password."
    )
    def post(self, request):
        user_id = request.query_params.get("user_id")
        new_password = request.data.get("new_password")
        user = get_object_or_404(User, id=user_id)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Auth - Password"],
        summary="Change Password",
        description="Allows a logged-in user to change their password."
    )
    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

# ---------------------------- Profile Management Endpoints ----------------------------

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Auth - Profile"],
        summary="Get Profile",
        description="Fetches the profile details of the logged-in user."
    )
    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Auth - Profile"],
        summary="Update Profile",
        description="Updates the profile information of the logged-in user."
    )
    def put(self, request):
        user = request.user
        user.username = request.data.get("username", user.username)
        user.email = request.data.get("email", user.email)
        user.save()
        return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
