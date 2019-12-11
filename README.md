# docstrings2html

Автор: Зырянов Евгений (finkrer@gmail.com)

## Описание
Данное приложение позволяет получать документацию модулей Python на основе
docstrings с выводом в виде HTML-страниц.

## Требования
* Python не ниже версии 3.7
* mako

## Состав
* Основной файл: `docstrings2html.py`
* Модули: `modules/`
* Шаблоны: `templates/`
* Тесты: `tests/`

## Консольная версия
Справка по запуску: `./docstrings2html.py --help`

Примеры запуска:

* `./docstrings2html.py module.py`

* `./docstrings2html.py module1.py module2.py --output=./documentation`

* `./docstrings2html.py -i package`

## Подробности реализации
Реализующие логику программы модули расположены в папке `modules/`.
Класс `PackageParser` создает на основе внутренней структуры папки объект,
содержащий все вложенные пакеты и модули.
Класс `ModuleParser` разбивает текст модуля на классы и методы, также
считывая их docstrings.
Затем класс `TemplateFormatter` создает HTML-страницы
документации на основе шаблонов mako (в папке `templates/`).
Есть возможность построить индекс всех получившихся страниц, а также
индексы для каждого вложенного пакета.

### О шаблонах
`base.html` отвечает за общий текст всех страниц, в том числе CSS.
В `docpage.html` и `index.html` описаны соответствующие страницы.
`module_index.html` и `navbar.html` отвечают за элементы, которые можно
переиспользовать: индекс модуля и навигационную строку сверху страницы.