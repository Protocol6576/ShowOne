<?php

use Illuminate\Support\Facades\Route;



Route::get('/', function () {
    return view('welcome');
});

Route::get('/main', function () {
    return view('mainPage');
});



// *** Роуты к запросам на сервер ***

Route::get('/getNotesList', function() {
    return (getFileNames());
});

Route::get('/redactNote/{noteName}/{noteText}', function($noteName, $noteText) {
    return redactNote($noteName, $noteText);
});

Route::get('/readNote/{noteName}', function($noteName) {
    return readNote($noteName);
});

Route::get('/createNote/{noteName}', function($noteName) {
    return createNote($noteName);
});

Route::get('/deleteNote/{noteName}', function($noteName) {
    return deleteNote($noteName);
});

Route::get('/getText/{text}', function($text) {
    return getText($text);
});

function getText($text) {
    return ($text."[eq");
}

// *** Запросы на сервер для взаимодействия с "заметками" ***

// Изменить: чтоб работа была не только с файлом "Заметка №11", забудешь ведь

function getFileNames() {
    $path = public_path('allNotes');
    $filesInFolder = File::files($path);

    foreach($filesInFolder as $key => $path){
        $files = pathinfo($path);
        $NotesList[] = array(
            "rank" => "|",
            "title" => $files['filename']
        );
    }

    return $NotesList;
    
}

function redactNote($noteName, $noteText) {
    $path = public_path('allNotes/'.$noteName.'.txt');
    if (File::exists($path)) {
        File::put($path, $noteText);
        return "Файл изменен";
    } else {
        return "не существует";
    }
}

function readNote($noteName) {
    $path = public_path('allNotes/'.$noteName.'.txt');
    $noteText = File::get($path);

    return $noteText;
}

function createNote($noteName) {
    $path = public_path('allNotes/'.$noteName.'.txt');
    if (File::exists($path)) {
        return "Файл уже существует";
    } else {
        File::put($path, "Я родился!");
        return "Файл создан";
    }
}

function deleteNote($noteName) {
    $path = public_path('allNotes/'.$noteName.'.txt');
    if (File::exists($path)) {
        File::delete($path);
        return "Файл удален";
    } else {
        return "Файл не существует";
    }
}