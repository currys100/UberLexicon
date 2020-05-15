from django.shortcuts import render, redirect
from django.http import HttpResponse
from words.models import Item, Word


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/words/the-only-list')
    return render(request, 'home.html')


def new_list(request):
    word_ = Word.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=word_)
    return redirect('/lists/the-only-list-in-the-world/')


def view_words(request):
    items = Item.objects.all()
    return render(request, 'words.html', {'items': items})
