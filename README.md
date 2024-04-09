## Приложение для скачивания роликов YouTube
С помощью данного приложения можно скачивать видеоролики из сервиса Youtube, используя ссылку на видео. Имеется возможность выбрать качество видео (максимум 720р) и скачать отдельно аудио дорожку.

Для запуска приложения на Windows следуйте инструкции:
1. Установить *pyinstaller*
```
pip install pyinstaller
```
2. Клонировать проект
```
git clone https://github.com/AntonLukin1986/YouTube_downloader.git
```
3. Создать и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
```
4. Установить зависимости
```
pip install -r requirements.txt
```
5. Перейти в папку уровнем выше
```
cd ..
```
6. Выполнить команду
```
pyinstaller --onefile --name="Загрузчик YouTube" --icon="youtube_logo.ico" youtube_downloader.pyw
```
7. Запускающий приложение файл «**Загрузчик YouTube.exe**» появится в папке **dist**

### Дополнительная информация:
Замена расширения «.py» на «.pyw» в файле *youtube_downloader* приводит к отключению вывода окна консоли при запуске exe-файла в Windows.
