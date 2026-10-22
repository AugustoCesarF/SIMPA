from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginTokenView(APIView):
    """
    RF08 — Autenticação por token simples do Django REST Framework.
    Permite login com username ou e-mail + senha.
    Retorna o token de autenticação e dados básicos do usuário.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        login_input = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        if not login_input or not password:
            return Response(
                {"error": "Informe usuário/e-mail e senha."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login_str = str(login_input).strip()
        # Se for e-mail, buscar o username correspondente
        user_candidate = User.objects.filter(email__iexact=login_str).first()
        username_to_try = user_candidate.username if user_candidate else login_str

        user = authenticate(request, username=username_to_try, password=password)

        # Se falhou mas o input original não era e-mail, tentar também como username direto
        if not user and user_candidate:
            user = authenticate(request, username=login_str, password=password)

        if not user:
            return Response(
                {"error": "Credenciais inválidas. Verifique usuário/e-mail e senha."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"error": "Conta de usuário inativa."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
                "nome": user.get_full_name() or user.username,
            },
            status=status.HTTP_200_OK,
        )


class LogoutTokenView(APIView):
    """
    Revoga o token de autenticação do usuário conectado.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            Token.objects.filter(user=request.user).delete()
            return Response(
                {"message": "Token revogado com sucesso. Logout realizado."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Erro ao revogar token: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MeView(APIView):
    """
    Retorna os dados do usuário atualmente autenticado via Token.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(
            {
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
                "nome": user.get_full_name() or user.username,
                "is_staff": user.is_staff,
            },
            status=status.HTTP_200_OK,
        )
