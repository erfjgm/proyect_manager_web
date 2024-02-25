from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from .models import Board, List, Card, UserProfile


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

def list_boards(request):
    if request.method == 'GET':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            company_boards = list(Board.objects.filter(company=user_profile.company).values('id','name'))
            return JsonResponse({'boards': company_boards})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'UserProfile not found for the current user'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

def list_lists(request):       
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            board_name = request_data.get('name_board')
            if board_name is not None:
                board = Board.objects.get(name=board_name)
                lists = list(List.objects.filter(board=board).values('id', 'name'))
                return JsonResponse({'lists': lists})
            else:
                return JsonResponse({'error': 'Missing or invalid "name_board" parameter'}, status=400)
        except Board.DoesNotExist:
            return JsonResponse({'error': 'Board not found'}, status=404)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Error decoding JSON: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'This view only accepts POST requests'}, status=405)

def list_cards(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            list_name = request_data.get('name_list')
            if list_name is not None:
                lista = List.objects.get(name=list_name)
                cards = list(Card.objects.filter(lista=lista).values('id','name'))
                return JsonResponse({'cards': cards})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'List not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
        
def exit(request):
    logout(request)
    return redirect('home')
