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
                                    <div class="card-body">
                                        <h4 class="card-title">${list.name}</h4>
                        `;
            cards.forEach((card) => {
                content += `
                            <p class="card-text">${card.name}</p>
                            `;
            });
            content += `            
                        <a href="#" class="btn btn-primary">Entrar</a>
                    </div>
                </div>
            </div>
            `;
        });
        lists.innerHTML = content;
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
};

async function listCards(name) {
    try {
        const dataToSend = {
            name_list: name
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

async function editBoard(oldName,newName) {
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

$('select[name="user"]').on('change', async function () {
    listLists($(this).val());
    activeBoard.innerHTML = $(this).val();
});

window.addEventListener('load', async () => {
    board_active=await listBoards();
    listLists(board_active);
    activeBoard.innerHTML = board_active;
});

$('.btnCancelNewBoard').click(function () {
    $('#myModal').modal('hide');
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
    $('#btnAddEditBoard').text('Agregar');
    $('#btnAddEditBoard').data('action', 'add');
    $('#myModal').modal('show');
});

$('#editBoard').click(async function () {
    $('#BotonsOptions').hide();
    $('#exampleModalLabel').text('Editar Board');
    $('#boardName').val($('#activeBoard').text());
    $('#btnAddEditBoard').text('Editar');
    $('#btnAddEditBoard').data('action', 'edit');
    $('#myModal').modal('show');
});

$('#btnAddEditBoard').click(async function () {
    const action = $(this).data('action')
    const newBoardName = $('#boardName').val()
    if (newBoardName.trim() !== '') {
        try {
            let result;
            if (action === 'add') {
                result = await addBoard(newBoardName);
            } else if (action === 'edit') {
                const oldBoardName = $('#activeBoard').text().trim();
                result = await editBoard(oldBoardName, newBoardName);
            }
            await listBoards();
            await listLists(newBoardName);
            $('select[name="user"]').val(newBoardName);
            //$('select[name="user"]').change()
            activeBoard.innerHTML = newBoardName;
        } catch (error) {
            console.error(`Error al ${action === ADD_ACTION ? 'agregar' : 'editar'} el board:`, error.message);
        } finally {            
            $('#myModal').modal('hide');
        }
    }
});

$('#deleteBoard').click(async function () {
    const deleteBoardNombre = $('#activeBoard').text();
    $('#BotonsOptions').hide();
    const result = await deleteBoard(deleteBoardNombre);
    board_active= await listBoards();
    listLists(board_active);
    activeBoard.innerHTML = board_active;
});