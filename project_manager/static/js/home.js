const listBoards = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_boards/');
        const data = await response.json();
        let content = '';
        data.boards.forEach((board) => {
            content += `
            <option> ${board.name} </option>
            `;
        });
        user.innerHTML = content;
        listLists(data.boards[0].name)
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
        })
        const data = await response.json();
        let content = '';

        const listCardsPromises = data.lists.map(async (list) => {
            const cards = await listCards(list.name);
            return { list, cards };
        });
        const listsData = await Promise.all(listCardsPromises)
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
            })
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
}

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
        })
        const data = await response.json();

        return (data.cards)
    } catch (error) {
        console.error('Error en la solicitud:', error.message);
    }
}


$('select[name="user"]').on('change', async function () {
    listLists($(this).val())
})

window.addEventListener('load', async () => {
    await listBoards();
})    
