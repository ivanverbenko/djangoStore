from django.shortcuts import render

# Create your views here.
def index(request):
    context={'title':'store'}
    return render(request, 'products/index.html',context=context)

def products(request):
    context = {'title': 'store-catalog'}
    return render(request, 'products/products.html')