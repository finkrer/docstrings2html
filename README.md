# docstrings2html

Автор: Зырянов Евгений (finkrer@gmail.com)

## Описание
Данное приложение позволяет получать документацию модулей Python на основе
docstrings с выводом в виде HTML-страницы.

## Требования
* Python не ниже версии 3.7
* mako
* anytree

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

* `./docstrings2html.py package1 package2`

## Подробности реализации
Реализующие логику программы модули расположены в папке `modules/`.
Класс `entity_parser.Parser` разбивает текст модуля на классы (`entity_parser.Class`)
и методы (`entity_parser.Method`), также считывая их docstrings.
Затем класс `template_formatter.TemplateFormatter` создает HTML-страницу документации
на основе шаблона mako (`templates/docpage.html`). Есть возможность построить индекс
получившихся страниц с помощью шаблона. Индекс использует anytree для построения
дерева файлов, чтобы показывать их в более удобном формате.