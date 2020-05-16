from django.shortcuts import render, redirect
from django.http import HttpResponse
from words.models import Item, Word


def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    return render(request, 'home.html')


def new_word(request):
    word_ = Word.objects.create()
    Item.objects.create(text=request.POST['item_text'], word=word_)
    return redirect('/words/alir_lexicon/')


def view_words(request):
    items = Item.objects.all()
    return render(request, 'words.html', {'items': items})
