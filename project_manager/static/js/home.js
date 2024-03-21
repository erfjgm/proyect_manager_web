const listBoards = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_boards/');
        const data = await response.json();
        let content = '';
        data.boards.forEach((board) => {
            content += `
            <option value=${board.name}> ${board.name} </option>
            `;
        });
        user.innerHTML = content;
        return data.boards[0].name;
    } catch (ex) {
        alert(ex);
    }
};

async function listLists(name) {
    try {
        const dataToSend = {
            name_board: name
        };
        const response = await fetch('http://127.0.0.1:8000/list_lists/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        const data = await response.json();
        let content = '';
        const listCardsPromises = data.lists.map(async (list) => {
            const cards = await listCards(list.name);
            return { list, cards };
        });
        const listsData = await Promise.all(listCardsPromises);
        listsData.forEach(({ list, cards }) => {
            content += `
                <div class="col-sm-4">
                    <div class="card">
                            <div class="card-header">
                                <div class="row">
                                <div class="col-sm-10 col-10">
                                <input type="text" class="form-control listName" id="${list.name}" value="${list.name}">
                                </div>
                                <div class="col-sm-1 col-1">
                                <button class="btn btn-danger deleteList" id="${list.name}">-</button>
                                </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <ul class="list-group">
                `;
            cards.forEach((card) => {
                content += `
                                    <li class="list-group-item mycard">${card.name}</li>
                            `;
            });
            content += ` 
                                </ul>
                                <button class="btn btn-primary addCard" id="${list.name}">+</button>                                
                            </div>
                    </div>
                </div>               
                `;
        });
        content += `
            <div id="contBtn" class="col-sm-1">

            </div> 
            `;
        lists.innerHTML = content;
        var addNewList = document.createElement('button');
        addNewList.id = 'addNewList';
        addNewList.className = 'btn btn-primary';
        addNewList.innerHTML = '+';
        contBtn.appendChild(addNewList);
        addNewList.addEventListener('click', function () {
            $('#exampleModalLabel').text('Agregar nuevo List en el Board ' + $('#activeBoard').text());
            $('#boardName').val('');
            $('#btnAddEdit').text('Agregar');
            $('#btnAddEdit').data('action', 'addList');
            $('#myModal').modal('show');
        });
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function listCards(name) {
    try {
        const dataToSend = {
            name_list: name,
            act_board: $('#activeBoard').text()
        };
        const response = await fetch('http://127.0.0.1:8000/list_cards/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        const data = await response.json();
        return (data.cards);
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function listDetailsCard(nameCard,nameList) {
    try {
        const dataToSend = {
            name_card: nameCard,
            name_list: nameList,
            name_board: $('#activeBoard').text()
        };
        const response = await fetch('http://127.0.0.1:8000/list_detail_card/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        const data = await response.json();
        return (data.card_detail);
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function addBoard(name) {
    try {
        const dataToSend = {
            new_board: name
        };
        const response = await fetch('http://127.0.0.1:8000/add_board/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        if (!response.ok) {
            const errorData = await response.json()
            if (errorData.error) {
                alert(errorData.error);
            } else {
                console.log(errorData);
            }
        } else {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function deleteBoard(name) {
    try {
        const confirmDelete = window.confirm(`¿Estás seguro de que quieres eliminar el board "${name}"?`);
        if (confirmDelete) {
            const dataToSend = {
                delete_board: name
            };
            const response = await fetch('http://127.0.0.1:8000/delete_board/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
                },
                body: JSON.stringify(dataToSend)
            });
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function editBoard(oldName, newName) {
    try {
        const dataToSend = {
            old_board: oldName,
            new_board: newName
        };
        const response = await fetch('http://127.0.0.1:8000/edit_board/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        if (!response.ok) {
            const errorData = await response.json();
            if (errorData.error) {
                alert(errorData.error);
            } else {
                console.log(errorData);
            }
        } else {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function addList(newList, actBoard) {
    try {
        const dataToSend = {
            new_list: newList,
            board: actBoard
        };
        const response = await fetch('http://127.0.0.1:8000/add_list/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        if (!response.ok) {
            const errorData = await response.json()
            if (errorData.error) {
                alert(errorData.error);
            } else {
                console.log(errorData);
            }
        } else {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
}

async function editList(oldList, newList, actBoard) {
    try {
        const dataToSend = {
            oldListName: oldList,
            newListName: newList,
            board: actBoard
        };
        const response = await fetch('http://127.0.0.1:8000/edit_list/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        if (!response.ok) {
            const errorData = await response.json()
            if (errorData.error) {
                alert(errorData.error);
            } else {
                console.log(errorData);
            }
        } else {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
}

async function deleteList(name, actBoard) {
    try {
        const confirmDelete = window.confirm(`¿Estás seguro de que quieres eliminar el list "${name}"?`);
        if (confirmDelete) {
            const dataToSend = {
                delete_list: name,
                board: actBoard
            };
            const response = await fetch('http://127.0.0.1:8000/delete_list/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
                },
                body: JSON.stringify(dataToSend)
            });
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function addCard(cardName,cardDetail,delivery_date,selectedUsers) {
    try {
        const dataToSend = {
            board_name: $('#activeBoard').text(),
            list_name: $('#activeList').text(),
            card_Name: cardName,
            card_Detail: cardDetail,
            delivery_date: delivery_date,
            selected_Users: selectedUsers
        };
        const response = await fetch('http://127.0.0.1:8000/add_card/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        if (!response.ok) {
            const errorData = await response.json()
            if (errorData.error) {
                alert(errorData.error);
            } else {
                console.log(errorData);
            }
        } else {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
}

async function editCard(cardOldName,cardName,cardDetail,delivery_date,selectedUsers) {
    try {
        const dataToSend = {
            board_name: $('#activeBoard').text(),
            list_name: $('#activeList').text(),
            card_old_name: cardOldName,
            card_Name: cardName,
            card_Detail: cardDetail,
            delivery_date: delivery_date,
            selected_Users: selectedUsers
        };
        const response = await fetch('http://127.0.0.1:8000/edit_card/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
            },
            body: JSON.stringify(dataToSend)
        });
        if (!response.ok) {
            const errorData = await response.json()
            if (errorData.error) {
                alert(errorData.error);
            } else {
                console.log(errorData);
            }
        } else {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
}

async function deleteCard(cardName){
    try {
        const confirmDelete = window.confirm(`¿Estás seguro de que quieres eliminar la tarjeta "${cardName}"?`);
        if (confirmDelete) {
            const dataToSend = {
                board_name: $('#activeBoard').text(),
                list_name: $('#activeList').text(),
                card_Name: cardName,
            };
            const response = await fetch('http://127.0.0.1:8000/delete_card/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': jQuery("[name=csrfmiddlewaretoken]").val()
                },
                body: JSON.stringify(dataToSend)
            });
            if (!response.ok) {
                const errorData = await response.json()
                if (errorData.error) {
                    alert(errorData.error);
                } else {
                    console.log(errorData);
                }
            } else {
                const data = await response.json();
                return data;
            }
        }
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
}

const listUsers = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_users/');
        const data = await response.json();
        return data.users;
    } catch (ex) {
        alert(ex);
    }
};

$('select[name="user"]').on('change', async function () {
    listLists($(this).val());
    activeBoard.innerHTML = $(this).val();
});

window.addEventListener('load', async () => {
    board_active = await listBoards();
    listLists(board_active);
    activeBoard.innerHTML = board_active;
});

$('.closedModal').click(function () {
    //$('#myModal').modal('hide');
    $('.modal').modal('hide');
});

$('#OptionsBoard').click(function () {
    var posicionBoton = $('#OptionsBoard').offset();
    $('#BotonsOptions').css({
        top: posicionBoton.top + $('#OptionsBoard').outerHeight(),
        left: posicionBoton.left
    });
    $('#BotonsOptions').toggle();
});

$('#addNewBoard').click(function () {
    $('#exampleModalLabel').text('Agregar nuevo Board');
    $('#boardName').val('');
    $('#btnAddEdit').text('Agregar');
    $('#btnAddEdit').data('action', 'add');
    $('#myModal').modal('show');
});

$('#editBoard').click(async function () {
    $('#BotonsOptions').hide();
    $('#exampleModalLabel').text('Editar Board');
    $('#boardName').val($('#activeBoard').text());
    $('#btnAddEdit').text('Editar');
    $('#btnAddEdit').data('action', 'edit');
    $('#myModal').modal('show');
});

$('#deleteBoard').click(async function () {
    const deleteBoardName = $('#activeBoard').text();
    $('#BotonsOptions').hide();
    const result = await deleteBoard(deleteBoardName);
    board_active = await listBoards();
    listLists(board_active);
    activeBoard.innerHTML = board_active;
});

//Logica del modal add/edit board+list
$('#btnAddEdit').click(async function () {
    const action = $(this).data('action');
    const inputName = $('#boardName').val();
    if (inputName.trim() !== '') {
        try {
            let result;
            if (action === 'add') {
                result = await addBoard(inputName);
                activeBoard.innerHTML = inputName;
            } else if (action === 'edit') {
                const oldBoardName = $('#activeBoard').text().trim();
                result = await editBoard(oldBoardName, inputName);
                activeBoard.innerHTML = inputName;
            } else if (action === 'addList') {
                const actBoard = $('#activeBoard').text();
                result = await addList(inputName, actBoard);
            }
            await listBoards();
            await listLists($('#activeBoard').text());
            $('select[name="user"]').val($('#activeBoard').text());
        } catch (error) {
            console.error(`Error al ${action === ADD_ACTION ? 'agregar' : 'editar'} el board:`, error.message);
        } finally {
            $('#myModal').modal('hide');
        }
    }
});

$(document).on('blur', '.listName', async function () {
    const actBoard = $('#activeBoard').text();
    const inputName = $(this).val()
    const oldName = $(this).attr("id");
    if (inputName !== oldName) {
        result = await editList(oldName, inputName, actBoard);
        const alertSuccess = $('#customAlert')
        alertSuccess.text("El nombre de la lista " + oldName + " se ha actualizado a " + inputName);
        alertSuccess.show();
        setTimeout(function () {
            alertSuccess.fadeOut(2000);
        }, 3000);
        await listBoards();
        await listLists($('#activeBoard').text());
        $('select[name="user"]').val($('#activeBoard').text());
    }
});

$(document).on('click', '.deleteList', async function () {
    const listDeleteName = $(this).attr("id");
    const actBoard = $('#activeBoard').text();
    const result = await deleteList(listDeleteName, actBoard);
    listLists(actBoard);
});

//Funcion para abrir CARD para añadir
$(document).on('click', '.addCard', async function () {
    const listName = $(this).attr("id");
    activeList.innerHTML = listName;
    $('#cardModalLabel').text('Agregar nuevo Card en ' + listName);
    $('#cardName').val('');
    $('#cardDetail').val('');
    $('#fechaInput').val('');
    $('#btnAddEditCard').data('action', 'add');
    $('#btnAddEditCard').text('Agregar');
    $('#btnDeleteCard').hide();    
    //Tenemos que cargar los usuarios
    const usuarios = await listUsers();
    let content = '';
    usuarios.forEach((user) => {
        content += `
            <input type="checkbox" class="btn-check" id="${user.id}" autocomplete="off">
            <label class="btn btn-outline-primary" for="${user.id}">${user.username}</label>     
        `;
    })
    usersCard.innerHTML = content;
    $('#cardModal').modal('show');
});

//Funcion para abrir CARD para editar
$(document).on('click', '.mycard', async function () {    
    var nameCard = $(this).text();
    var card = $(this).closest('.card');
    var cardHeader = card.find('.card-header');
    var nameList = cardHeader.find('.listName').val();
    activeList.innerHTML = nameList;
    $('#cardModalLabel').text('Agregar nuevo Card en ' + nameList);
    $('#cardName').val($(this).text());
    card_detail = await listDetailsCard(nameCard,nameList);
    $('#cardDetail').val(card_detail[0]);
    $('#fechaInput').val(card_detail[1]);
    $('#btnDeleteCard').show();    
    const usuarios = await listUsers();
    let content = '';
    usuarios.forEach((user) => {
        const isChecked = card_detail[2].some((user_act) => user_act.id === user.id);
        content += `
            <input type="checkbox" class="btn-check" id="${user.id}" autocomplete="off" ${isChecked ? 'checked' : ''}>
            <label class="btn btn-outline-primary" for="${user.id}">${user.username}</label>     
        `;
    })
    usersCard.innerHTML = content;
    $('#btnAddEditCard').data('cardOldName', nameCard);
    $('#btnAddEditCard').data('action', 'edit');
    $('#btnAddEditCard').text('Editar');
    $('#cardModal').modal('show');
});

//Funcion para controlar el CARD Modal
$('#btnAddEditCard').click(async function () {
    const action = $(this).data('action');
    const cardName = $('#cardName').val();
    const cardDetail = $('#cardDetail').val();
    const delivery_date = $('#fechaInput').val();
    const selectedUsers = [];
    $('.btn-check:checked').each(function () {
        selectedUsers.push($(this).attr('id'));
    });
    if (action === 'add') {
        result = await addCard(cardName,cardDetail,delivery_date,selectedUsers);
    }
    else if(action === 'edit') {
        const cardOldName = $(this).data('cardOldName');
        result = await editCard(cardOldName,cardName,cardDetail,delivery_date,selectedUsers);
    }
    await listLists($('#activeBoard').text());
    $('#cardModal').modal('hide');
});

//Funcion para cuando pulsamos en el CARD Modal delete
$('#btnDeleteCard').click(async function () {
    const cardName = $('#cardName').val();
    result = await deleteCard(cardName);
    await listLists($('#activeBoard').text());
    $('#cardModal').modal('hide');    
});