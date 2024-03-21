from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

@login_required
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

@login_required
def list_lists(request):       
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            board_name = request_data.get('name_board')
            if board_name is not None:
                board = Board.objects.get(name=board_name)
                lists = list(List.objects.filter(board=board,is_deleted=False).values('id', 'name'))
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

#En esta funcion nos queda comprobar que el board pertenezca al la compañia
@login_required
def add_list(request):
    try:
        if request.method == 'POST':
            request_data = json.loads(request.body.decode('utf-8'))
            new_list_name = request_data.get('new_list')
            board_name = request_data.get('board')
            if not new_list_name or not board_name:
                return JsonResponse({'error': 'Nombre de board requerido'}, status=400)
            board = Board.objects.get(name=board_name)
            if List.objects.filter(name__iexact=new_list_name, board=board).exists():
                return JsonResponse({'error': f'Ya existe un board con el nombre "{new_list_name}" en esta compañía'}, status=400)
            new_list = List.objects.create(name=new_list_name, board=board, creat_by=request.user)
            return JsonResponse({'success': f'List  creado con éxito'}, status=200)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Perfil de usuario no encontrado'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error en la creación del board: {str(e)}'}, status=500)

@login_required
def edit_list(request):
    try:
        if request.method == 'POST':
            request_data = json.loads(request.body.decode('utf-8'))
            oldListName = request_data.get('oldListName')
            newListName = request_data.get('newListName')
            board_name = request_data.get('board')
            if not oldListName or not newListName or not board_name:
                return JsonResponse({'error': 'Nombre de board requerido'}, status=400)
            user_profile = UserProfile.objects.get(user=request.user)
            board = Board.objects.get(name=board_name, company=user_profile.company)
            if List.objects.filter(name__iexact=newListName, board=board).exists():
                return JsonResponse({'error': f'Ya existe un list con el nombre "{newListName}" en esta compañía'}, status=400)
            edit_list= List.objects.get(name__iexact=oldListName, board=board)
            edit_list.name=newListName
            edit_list.save()
            return JsonResponse({'success': f'Board  creado con éxito'}, status=200)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Perfil de usuario no encontrado'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error en la creación del board: {str(e)}'}, status=500)

@login_required
def delete_list(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        delete_list_name = request_data.get('delete_list')
        board_name = request_data.get('board')
        if not delete_list_name or not board_name:
                return JsonResponse({'error': 'Faltan datos de entrada'}, status=400)
        user_profile = UserProfile.objects.get(user=request.user)
        board=Board.objects.get(name__iexact=board_name, company=user_profile.company)
        list_to_delete = List.objects.get(name=delete_list_name,board=board)
        count_delete=List.objects.filter(name__icontains=list_to_delete.name+"_delete").values('name').count()
        list_to_delete .name=list_to_delete .name+"_delete"+str(count_delete+1)
        list_to_delete .is_deleted=True
        list_to_delete .deleted_by= request.user
        list_to_delete .deletion_date=timezone.now()
        list_to_delete .save()
        return JsonResponse({'success': True})

@login_required
def list_cards(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            list_name = request_data.get('name_list')
            board_name = request_data.get('act_board')
            if list_name is not None:
                board= Board.objects.get(name=board_name)
                lista = List.objects.get(name=list_name,board=board)
                cards = list(Card.objects.filter(lista=lista,is_deleted=False).values('id','name'))
                return JsonResponse({'cards': cards})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'List not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def list_detail_card(request):
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        name_board = request_data.get('name_board')
        name_list = request_data.get('name_list')
        name_card = request_data.get('name_card')

        user_profile = UserProfile.objects.get(user=request.user)
        board = Board.objects.get(name=name_board,company=user_profile.company)
        list_obj = List.objects.get(name= name_list, board=board)
        card = Card.objects.get(name= name_card, lista=list_obj)

        #print([card.description,card.delivery_date,card.assigned_users])
        assigned_users = card.assigned_users.all().values('user_id')
        user_ids = [profile['user_id'] for profile in assigned_users]
        users=list(User.objects.filter(id__in=user_ids).values('id','username'))  
        #print(assigned_users,user_ids,users)
        #print(name_board,name_list,name_card)
        return JsonResponse({'card_detail': [card.description,card.delivery_date,users]})

#Esta funcion nos queda obtimizarla!!!!!
@login_required
def add_card(request):
    try:
        if request.method == 'POST':
            # Obtenemos y extraemos datos del cuerpo de la solicitud POST
            request_data = json.loads(request.body)
            board_name = request_data.get('board_name')
            list_name = request_data.get('list_name')
            new_card_name = request_data.get('card_Name')
            new_card_detail = request_data.get('card_Detail')
            delivery_date = request_data.get('delivery_date')
            if not delivery_date:
                delivery_date=None            
            selected_Users = request_data.get('selected_Users')

            # Obtenemos los usuarios actual, board y list
            user_profile = get_object_or_404(UserProfile, user=request.user)
            board = get_object_or_404(Board, name=board_name, company=user_profile.company)
            list_obj = get_object_or_404(List, name=list_name, board=board)
            
            #Creamos la tarjeta nueva
            new_card = Card.objects.create(name=new_card_name, lista=list_obj, description=new_card_detail,
                                           delivery_date=delivery_date)
            new_card.assigned_users.add(*selected_Users)
            return JsonResponse({'success': f'Card creado con éxito'}, status=200)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Perfil de usuario no encontrado'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error en la creación del board: {str(e)}'}, status=500)

@login_required
def edit_card(request):
    try:
        if request.method == 'POST':
            # Obtenemos y extraemos datos del cuerpo de la solicitud POST
            request_data = json.loads(request.body)
            board_name = request_data.get('board_name')
            list_name = request_data.get('list_name')
            card_old_name = request_data.get('card_old_name')
            card_new_name = request_data.get('card_Name')
            card_detail = request_data.get('card_Detail')
            delivery_date = request_data.get('delivery_date')
            if not delivery_date:
                delivery_date=None            
            selected_users = request_data.get('selected_Users')

            # Obtenemos los usuarios actual, board, list y card
            user_profile = get_object_or_404(UserProfile, user=request.user)
            board = get_object_or_404(Board, name=board_name, company=user_profile.company)
            list_obj = get_object_or_404(List, name=list_name, board=board)
            card = get_object_or_404(Card, name=card_old_name, lista=list_obj)
            
            # Actualizar los campos de card
            card.name=card_new_name
            card.description=card_detail
            card.delivery_date=delivery_date
            card.save() 

            # Actualizar usuarios asignados
            card.assigned_users.set(selected_users)  

            return JsonResponse({'success': 'Tarjeta actualizada con éxito'}, status=200) 
    except Exception as e:
        return JsonResponse({'error': f'Error al editar la tarjeta: {str(e)}'}, status=500)

@login_required
def delete_card(request):
    try:
        if request.method == 'POST':
            # Obtenemos y extraemos datos del cuerpo de la solicitud POST
            request_data = json.loads(request.body)
            board_name = request_data.get('board_name')
            list_name = request_data.get('list_name')
            card_name = request_data.get('card_Name')

            # Obtenemos los usuarios actual, board, list y card
            user_profile = get_object_or_404(UserProfile, user=request.user)
            board = get_object_or_404(Board, name=board_name, company=user_profile.company)
            list_obj = get_object_or_404(List, name=list_name, board=board)
            card = get_object_or_404(Card, name=card_name, lista=list_obj)
            
            # Actualizar los campos de card
            count_delete=Card.objects.filter(name__icontains=card.name+"_delete").values('name').count()
            card.name=card.name+"_delete"+str(count_delete+1)
            card.is_deleted=True
            card.deleted_by= request.user
            card.deletion_date=timezone.now()
            card.save() 
            print(card)

            return JsonResponse({'success': 'Tarjeta borrada con éxito'}, status=200) 
    except Exception as e:
        return JsonResponse({'error': f'Error al editar la tarjeta: {str(e)}'}, status=500)

@login_required
def list_users(request):
    if request.method == 'GET':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            users_profile= UserProfile.objects.filter(company=user_profile.company,rol='USER').values('user_id')
            user_ids = [profile['user_id'] for profile in users_profile]
            users=list(User.objects.filter(id__in=user_ids).values('id','username'))                 
            return JsonResponse({'users': users})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'UserProfile not found for the current user'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

def exit(request):
    logout(request)
    return redirect('home')
