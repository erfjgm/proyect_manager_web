from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
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
            company_boards = list(Board.objects.filter(company=user_profile.company,is_deleted=False).values('id','name'))
            return JsonResponse({'boards': company_boards})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'UserProfile not found for the current user'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

@login_required
def add_board(request):
    try:
        if request.method == 'POST':
            request_data = json.loads(request.body.decode('utf-8'))
            new_board_name = request_data.get('new_board')
            if not new_board_name:
                return JsonResponse({'error': 'Nombre de board requerido'}, status=400)
            user_profile = UserProfile.objects.get(user=request.user)
            if Board.objects.filter(name__iexact=new_board_name, company=user_profile.company).exists():
                return JsonResponse({'error': f'Ya existe un board con el nombre "{new_board_name}" en esta compañía'}, status=400)
            new_board = Board.objects.create(name=new_board_name, company=user_profile.company)
            return JsonResponse({'success': f'Board "{new_board_name}" creado con éxito'}, status=200)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Perfil de usuario no encontrado'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error en la creación del board: {str(e)}'}, status=500)

@login_required
def edit_board(request):
    if request.method == 'POST':
            request_data = json.loads(request.body.decode('utf-8'))
            new_board_name = request_data.get('new_board')
            old_board_name = request_data.get('old_board')
            user_profile = UserProfile.objects.get(user=request.user)
            if Board.objects.filter(name__iexact=new_board_name, company=user_profile.company).exists():
                return JsonResponse({'error': f'Ya existe un board con el nombre "{new_board_name}" en esta compañía'}, status=400)
            edit_board= Board.objects.get(name__iexact=old_board_name, company=user_profile.company)
            edit_board.name=new_board_name
            edit_board.save()
            return JsonResponse({'success': 'Board creado con éxito'}, status=200)

@login_required
def delete_board(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        delete_board_name = request_data.get('delete_board')
        if not delete_board_name:
                return JsonResponse({'error': 'Nombre de board requerido'}, status=400)
        user_profile = UserProfile.objects.get(user=request.user)
        delete_board=Board.objects.get(name__iexact=delete_board_name, company=user_profile.company)
        count_delete=Board.objects.filter(name__icontains=delete_board.name+"_delete").values('name').count()
        delete_board.name=delete_board.name+"_delete"+str(count_delete+1)
        delete_board.is_deleted=True
        delete_board.deleted_by= request.user
        delete_board.deletion_date=timezone.now()
        delete_board.save()
        return JsonResponse({'success': True})

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
