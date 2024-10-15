# social/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import SocialAccount
from .serializers import SocialAccountSerializer

class SocialAccountViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = SocialAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the user to the currently authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        accounts = SocialAccount.objects.filter(user=request.user)
        serializer = SocialAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            account = SocialAccount.objects.get(pk=pk, user=request.user)
            account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SocialAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def status(self, request, pk=None):
        try:
            account = SocialAccount.objects.get(pk=pk, user=request.user)
            # Check the status of the account (e.g., token validity)
            return Response({'status': 'connected'}, status=status.HTTP_200_OK)
        except SocialAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

