from django.shortcuts import render, redirect
from django.http import HttpResponse
from words.models import Item, Word


def home_page(request):
    return render(request, 'home.html')


def new_word(request):
    word_ = Word.objects.create()
    Item.objects.create(text=request.POST['item_text'], word=word_)
    return redirect(f'/words/{word_.id}/')


def view_words(request, word_id):
    word_ = Word.objects.get(id=word_id)
    return render(request, 'words.html', {'word': word_})


def add_item(request, word_id):
    word_added = Word.objects.get(id=word_id)
    Item.objects.create(text=request.POST['item_text'], word=word_added)
    return redirect(f'/words/{word_added.id}/')