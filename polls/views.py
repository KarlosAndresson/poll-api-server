from django.shortcuts import render


def main_page(request):
    template = f'index.html'
    context = {}
    return render(request, template, context)
