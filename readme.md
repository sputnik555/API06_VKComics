# Публикация комиксов

Скрипт публикует случайный комикс с сайта [xkcd.com](https://xkcd.com/) в группу VK.

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Для настройки скрипта необходимо записать в файле `.env` параметры доступа к API VK. Для этого необходимо выполнить следующие шаги:
1. Зарегистрировать приложение вконтакте в разделе [Мои приложеня](https://vk.com/dev). Типом приложения указать standalone
2. Нажать на кнопку редактировать, скопировать параметр clint_id из адресной строки (он понадобится в следующем шаге).
3. Выпонить процедуру [Implict Flow](https://vk.com/dev/implicit_flow_user), при этом указав параметр `scope=photos,groups,wall,offline`. Скопировать значение параметра `access_token` из адресной строки и указать его в `VK_TOKEN` в файле `.env`
4. Указать id вашей группы в параметре `VK_GROUP_ID` файла `.env`. Узнать ID вы можете [здесь](https://regvk.com/id/)
5. Укажите в параметре `TEMPFILENAME` файла `.env`  имя для временного файла.

Пример заполненного файла `.env`:
```
VK_GROUP_ID=207992301
VK_TOKEN=a9987d71b3a932af5993c5e3d0e4f97399283dd202825fa355143df5f04d1e5e3bb35e3f642f746c709ad
TEMPFILENAME=image.png
```
### Пример запуска скрипта

Для запуска скрипта необходимо выполнить в консоли команду:

`python main.py`

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).