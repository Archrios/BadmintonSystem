from django.shortcuts import render, HttpResponse
from rest_framework.generics import ListAPIView
from .models import Users
from .serializers import UserSerializer

def home(request):
    return HttpResponse("""<h1 class="text-3xl font-bold text-blue-600">Hello Tailwind!</h1>""")

def test(request):
    return render(request, "base.html")

class UserListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer