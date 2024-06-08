from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "pages/index.html")

def error_404(request, exception):
    return render(request, "pages/404.html", status=404)

def error_500(request):
    return render(request, "pages/500.html", status=500)