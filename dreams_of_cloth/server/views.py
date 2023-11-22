from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PrintMessageView(APIView):
    """
    Print a message to the server terminal
    """
    def get(self, request, format=None):
        print("Server was pinged by client")
        return Response("Message printed", status=status.HTTP_200_OK)

