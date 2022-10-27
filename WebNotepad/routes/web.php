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

Route::get('/redactNote', function() {
    return redactNote();
});

Route::get('/readNote', function() {
    return readNote();
});

Route::get('/createNote', function() {
    return createNote();
});

Route::get('/deleteNote', function() {
    return deleteNote();
});



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

function redactNote() {
    $path = public_path('allNotes/Заметка №11.txt');
    if (File::exists($path)) {
        File::put($path, "Для детей!");
        return "Файл изменен";
    } else {
        return "не существует";
    }
}

function readNote() {
    $path = public_path('allNotes/Заметка №11.txt');
    $noteText = File::get($path);

    return $noteText;
}

function createNote() {
    $path = public_path('allNotes/Заметка №11.txt');
    if (File::exists($path)) {
        return "Файл уже существует";
    } else {
        File::put($path, "Я родился!");
        return "Файл создан";
    }
}

function deleteNote() {
    $path = public_path('allNotes/Заметка №11.txt');
    if (File::exists($path)) {
        File::delete($path);
        return "Файл удален";
    } else {
        return "Файл не существует";
    }
}