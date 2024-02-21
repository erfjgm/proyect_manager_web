from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from .models import Board, List, Card, Company, UserProfile


def home(request):
    if request.user.is_authenticated:
        boards = list(Board.objects.filter(company=list(
            UserProfile.objects.filter(user=request.user))[0].company))
        if request.method == 'POST':
            board = request.POST.get('board')
            print(request.POST.get('board'))
            if board:
                board = get_object_or_404(Board, name=board)
                lists = list(List.objects.filter(board=board))
                return render(request, 'home.html', {
                    'title': 'Inicio',
                    'board': board,
                    'boards': boards,
                    'lists': lists,
                })        
        lists = list(List.objects.filter(board=boards[0]))
        return render(request, 'home.html', {
            'title': 'Inicio',
            'board': boards[0],
            'boards': boards,
            'lists': lists,
        })
    else:
        return render(request, 'home.html', {
            'title': 'Inicio',
        })


def exit(request):
    logout(request)
    return redirect('home')
