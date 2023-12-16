from pathlib import Path
from tkinter import (
    Button, Entry, Label, messagebox, Radiobutton, StringVar, Tk
)

import pytube

DOWNLOAD_PATH = r'D:\Видео'
LOGO_PATH = r'D:\dev\my_projects\youtube_downloader\youtube_logo.ico'


def create_main_window():
    '''Создание главного окна программы.'''
    root = Tk()
    root.geometry('500x200')
    root.resizable(False, False)
    root.title('  YouTube загрузчик')
    root.config(background='#D3D3D3')
    root.iconbitmap(default=LOGO_PATH)
    return root


root = create_main_window()

quality = StringVar(value='-')  # переменная для селектора выбора качества
link = StringVar()  # переменная для ссылки на видео


def check_path(download_path):
    '''Определяет место сохранения скачанного файла.'''
    if Path(download_path).exists():
        return download_path
    return None


def show_common_block():
    '''Отображает общий блок с заголовком, полем для ввода ссылки и кнопкой
    «Очистить».'''
    main_label.pack(pady=5)
    entry_label.pack(anchor='w', padx=10, pady=10)
    entry.pack(anchor='w', padx=10)
    reset_btn.place(x=415, y=89)


def show_next_exit_btns():
    '''Отображает кнопки «Далее» и «Выход» под общим блоком.'''
    next_btn.place(x=100, y=130)
    exit_btn.place(x=300, y=140)


def show_selection_buttons():
    '''Отображает кнопки выбора качества контента.'''
    position = {'padx': 10, 'pady': 5, 'anchor': 'nw'}
    header.pack(**position)
    high_btn.pack(**position)
    medium_btn.pack(**position)
    sound_btn.pack(**position)


def reset_button():
    '''Определяет поведение кнопки «Очистить».'''
    link.set('')  # очищаем строку с адресом видео
    quality.set(value='-')
    # убираем все лишние элементы окна
    header.pack_forget()
    high_btn.pack_forget()
    medium_btn.pack_forget()
    sound_btn.pack_forget()
    content_name.place_forget()
    content_info.config(text='')
    content_info.place_forget()
    download_btn.place_forget()
    root.geometry('500x200')
    show_next_exit_btns()


def check_link():
    '''Отрабатывает нажатие кнопки «Далее».'''
    global youtubelink

    inputed_link = link.get()  # получаем введённую пользователем ссылку
    if inputed_link == '':
        messagebox.showinfo(title='  К сведению', message='Не указана ссылка!')
        return
    try:
        # переводим ссылку в нужный формат
        youtubelink = pytube.YouTube(inputed_link)
    except Exception:
        error_text = 'Видео не найдено!\nПроверьте правильность ссылки.'
        messagebox.showerror('  Ошибка', error_text)
        return
    root.geometry('500x270')
    next_btn.place_forget()
    exit_btn.place(x=420, y=210)
    content_name.config(text=f'{youtubelink.title[:30]}...')
    content_name.place(x=170, y=130)
    content_info.place(x=220, y=155)
    show_selection_buttons()


def quality_info():
    '''Отображает информацию о выбранном качестве контента.'''
    global content, content_quality

    selected_quality = quality.get()
    if selected_quality == 'max':
        content = youtubelink.streams.get_highest_resolution()
        content_quality = content.resolution
    elif selected_quality == 'mid':
        max_res = youtubelink.streams.get_highest_resolution().resolution
        max_res = int(max_res[:-1])
        medium_resolutions = (
            ('720p', '480p') if max_res > 720 else ('480p', '360p')
        )
        for content in reversed(
            youtubelink.streams.filter(progressive=True)
        ):
            if content.resolution in medium_resolutions:
                break
        else:  # этот блок сработает только если не сработает break
            content = youtubelink.streams.get_highest_resolution()
        content_quality = content.resolution
    elif selected_quality == 'sound':
        content = youtubelink.streams.get_audio_only()
        content_quality = content.abr
    text = f'Качество {content_quality}\n{round(content.filesize_mb, 1)} Mb'
    content_info.config(text=text)
    # отобразить кнопку скачивания видео
    download_btn.place(x=220, y=200)


def download():
    '''Скачивает выбранный контент.'''
    save_to = check_path(DOWNLOAD_PATH)
    content.download(
        output_path=save_to,
        filename_prefix=f'{content_quality}_'
    )
    text = 'папке с программой' if save_to is None else save_to
    messagebox.showinfo(
        title='  Готово',
        message=f'Загрузка файла завершена!\nСохранён в {text}'
    )


# заголовок общего окна
main_label = Label(
    root, text='Загрузка видео с YouTube',
    font=('Calibri Bold', 18), fg='#008B8B', bg='#D3D3D3'
)

# поле ввода ссылки на видео и его заголовок
entry_label = Label(
    root, text='Ссылка на видео:', font=('Arial', 12), bg='#D3D3D3'
)
entry = Entry(root, textvariable=link, font=('Arial'), width=35)

# кнопка очистки поля ввода
reset_btn = Button(
    root, text='ОЧИСТИТЬ', font=('Calibri', 10), bd=4, command=reset_button
)

# кнопка «Далее» проверяет введённую ссылку
next_btn = Button(
        root,
        text='Далее', font=('Calibri Bold', 14), fg='#006400', bd=6,
        command=check_link
    )

# кнопка «Выход» закрывает окно программы
exit_btn = Button(
    root, text='ВЫХОД', font=('Calibri', 12), bd=4,
    command=lambda: root.destroy()
)

# блок с заголовком и радиокнопками
header = Label(text='Выберите качество', font=('Arial', 10), bg='#D3D3D3')
high_btn = Radiobutton(
    text='Максимальное', bg='#D3D3D3', variable=quality, value='max',
    command=quality_info
)
medium_btn = Radiobutton(
    text='Среднее', bg='#D3D3D3', variable=quality, value='mid',
    command=quality_info
)
sound_btn = Radiobutton(
    text='Только звук', bg='#D3D3D3', variable=quality, value='sound',
    command=quality_info
)

# кнопка «Скачать» выбранный контент
download_btn = Button(
    root,
    text='СКАЧАТЬ', font=('Calibri Bold', 14), fg='#006400', bd=6,
    command=download
)

# метки для отображения информации о скачиваемом файле (редактируемые)
content_name = Label(
    text='', font=('Calibri Bold', 11), fg='#008B8B', bg='#D3D3D3'
)
content_info = Label(text='', bg='#D3D3D3')

show_common_block()
show_next_exit_btns()

if __name__ == '__main__':
    root.mainloop()
    # https://youtu.be/9OP04Q-z2uY?si=JuLaiNkWvFsdPjuQ
