# Парсер новостей

## Настройки парсера

В каталоге `settings` отредактируйте файл `parserSettings.conf`

```apache
LinksHolder=file
FileHolderName=sites.txt
MultiURLs=False
StopClass=footer
SpamTag=a
FindTag=p
FindClass=article__text
```

### Параметры

- `LinksHolder`=["cmd" - __default__, "file"]
>Данный параметр указывает парсеру откуда ожидать ссылку: 
>- `cmd` - ожидает из командной строки;
>- `file` - ожидает из файла (тогда обязательно наличие параметра `FileHolderName`).

- `FileHolderName`=[fileName]
>Данный параметр задается при `LinksHolder=file`. Указывает расположение и название файла в котором содержатся ссылки на сайты.

- `MultiURLs`=["False" - __default__, "True"]
> При параметре, равном `True`, осуществляется поиск по всем ссылкам указанным в командной строке при `LinksHolder`=cmd.

- `StopClass`=[string]
> Название класса, при котором дальнейший поиск элементов с тегами `FindTag` или классами `FindClass` заканчивается.

- `SpamTag`=[string]
> Иногда в статье делают "закладки" в тегах основного текста (например тег `<p>` внутри тега `<a>`). Можно указать название "тега-паразита" в данном параметре и парсинг его не обработает.

- `FindTag`=[string]
> Тег в котором будет осуществляться поиск тела статьи.

- `FindClass`=[string]
> Класс в котором будет осуществляться поиск тела статьи, при условии, что `FindTag`=None или элементов с тегом `FindTag` нет.

## Настройки форматирования

В каталоге `settings` отредактируйте файл `formatSettings.conf`

```apache
MaxWidthText=80
LinksFormat=[{l}; {s}]
NumTitleIndents=1
NumParagraphIndents=1
```

### Параметры

- `MaxWidthText`=[int]
> Максимальное количество букв в строке.

- `LinksFormat`=[[{s};{l}] | {s}[{l}] | [{l};{s}]]
> Формат вывода ссылки. s - текст ссылки, l - сама ссылка.

- `NumTitleIndents`=[int]
> Количество отступов посте заголовка.

- `NumParagraphIndents`=[int]
> Количество отступов между параграфами.

## Использование

Если `LinksHolder`=cmd:
```shell
> python main.py http[s]://site.ru/path/to/page[/|.htm|.html|...] [other links]
```
> Примечание: `[other links]` имеет смысл указывать только при `MultiURLs`=True.

Если `LinksHolder`=file:
```shell
> python main.py
```
> Примечание: При `LinksHolder`=file осуществляется по всем ссылкам из файла `FileHolderName`.