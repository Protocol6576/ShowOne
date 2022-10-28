var myData = [
    {
        title: 'Заметка №1',
        rank: '1',
    },
    {
        title: 'Заметка №2',
        rank: '2',
    },
    {
        title: 'Заметка №3',
        rank: '3',
    }
];

function updapteNoteList() {
    $$("NotesList").clearAll(); // Заменить на аргумент в функции load (Который true)
    $$("NotesList").load(function() {
        return webix.ajax().get('getNotesList');
    });
};

webix.ready(function(){
    webix.ui({
        rows: [
            {
                cols: [
                    {
                        // Меню слева
                        width: 300,
                        type: 'clean',

                        rows: [
                            {
                                height: 40,
                                type: 'clean',

                                cols: [
                                    {
                                        view:'search',
                                        id: 'NotesList_input',

                                        placeholder: 'Найти...',
                                    },
                                    {
                                        // Обновить список
                                        view: 'icon',
                                        icon: 'wxi-download',
                                        click: function() {
                                            $$("NotesList").clearAll();
                                            $$("NotesList").load(function() {
                                                return webix.ajax().get('getNotesList');
                                            });
                                        },
                                    },
                                    {
                                        // Создать файл. Добавить вывод в случае наличия такого же файла, а не окошко блин
                                        view: 'icon',
                                        icon: 'wxi-plus-circle',
                                        click: function() {
                                            webix.prompt({
                                                title:"Создание заметки",
                                                text:"Введите название новой заметки",
                                                ok:"Submit",
                                                cancel:"Cancel",
                                                input:{
                                                  required:true,
                                                  placeholder:"Ваше название",
                                                },
                                                width: 350,
                                              }).then(function(result){
                                                webix.ajax().get('createNote/' + result).then(function(data) {
                                                    data = data.text();
                                                    webix.message(data);
                                                    updapteNoteList();
                                                });
                                              });

                                            
                                        },
                                    }
                                ]
                            },
                            {
                                view: 'list',
                                id: 'NotesList',
                                data: ' ', // НЕ УДАЛЯТЬ! Иначе не произайдет прогрузки

                                select: 'true',
                                template:"#rank#. #title#",
                                ready: function() {
                                    updapteNoteList();
                                },

                                onContext:{}, // Позволяет использовать свое контекстное меню
                            },

                        ]
                    },
                    {
                        // Текстовое поле справа

                        rows: [
                            {    
                                cols: [
                                    {
                                        
                                    },
                                    {
                                        // Загрузить данные
                                        view: 'icon',
                                        icon: 'wxi-download',
                                        click: function() {
                                            var itemId = $$("NotesList").getSelectedItem().title; // Изменить (выглядит ужасно)
                                            var newText = $$("NoteTextArea").getValue();
                                            webix.ajax().get('redactNote/' + itemId + '/' + newText).then(function(data) {
                                                data = data.text();
                                                webix.message(data);
                                                updapteNoteList();
                                            });
                                        },
                                    }
                                ]
                                
                            },
                            {
                                view: 'textarea',
                                id: 'NoteTextArea',
                                placeholder: 'Напишите что-то здесь',
                                
                                borderless: false,
                                css: 'WebNotelistStyle',
                            },                        
                        ]


                        
                    }
                ]
            }
        ]
    });



    // *** Дополнительные элементы интерфейса ***

    // Контекстное меню для списка заметок
    webix.ui({ 
        view:"contextmenu",
        id:"cmenu",
        data:["Переименовать","Удалить",{ $template:"Separator" },"Логи"],
        on:{
            onItemClick: function(id) {
                var context = this.getContext(); // Зачем так много переменных? ИСПРАВИТЪ!!!
                var list = context.obj;
                var listId = context.id;
                var itemId = list.getItem(listId).title;

                switch (id) {
                    case "Переименовать":
                        webix.message("**Сделать переименвоание**");
                        updapteNoteList();
                        break;
                    case "Удалить":

                        webix.confirm({
                            title:"Подтвердите действие",
                            ok:"Да", 
                            cancel:"Нет",
                            text:'Вы уверены что хотите удалить "' + list.getItem(listId).title + '"?',
                        }).then(function(result){
                            webix.ajax().get('deleteNote/' + itemId).then(function(data) { // Оптимизировать (Выглядит чет некрасиво)
                                data = data.text();
                                webix.message(data);
                                updapteNoteList();
                            });
                        });
                        break;
                    case "Логи":
                        webix.message("**Сделать вывод логов**");
                        break;
                };
                
                //webix.message("List item: <i>"+list.getItem(listId).title+"</i> <br/>Context menu item: <i>"+this.getItem(id).value+"</i>");
            }
        }
    });

    
    $$("cmenu").attachTo($$("NotesList"));



    // *** События ***

    // Фильтрация списка заметок
    $$("NotesList_input").attachEvent("onTimedKeyPress",function(){
        var value = this.getValue().toLowerCase();
        $$("NotesList").filter(function(obj){
          return obj.title.toLowerCase().indexOf(value) !== -1;
        })
    });

});