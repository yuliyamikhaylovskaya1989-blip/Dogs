import requests
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import messagebox as mb


def get_random_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except Exception as e:
        mb.showerror("Ошибка", f"Ошибка при запросе к API: {e}")
        return None


def show_image():
    image_url = get_random_dog_image()
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)
            tab =ttk.Frame(notebook)
            notebook.add(tab, text=f"Картинка №{notebook.index('end')+1}")
            lb = ttk.Label(tab, image=img)
            lb.pack(padx=10, pady=10)
            lb.image = img

        except requests.RequestException as e:
            mb.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")
    progress.stop()



def prog():
    progress['value']=0
    progress.start(30)
    window.after(3000,show_image)




window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")

label = ttk.Label()
label.pack(padx=10, pady=10)

button = ttk.Button(text="Загрузить изображение", command=prog)
button.pack(padx=10, pady=10)

progress=ttk.Progressbar(mode="determinate", length=300)
progress.pack(padx=10, pady=10)

width_label = ttk.Label(text="Ширина:")
width_label.pack(side='left', padx=(10, 0))
width_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side='left', padx=(0, 10))

height_label = ttk.Label(text="Высота:")
height_label.pack(side='left', padx=(10, 0))
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side='left', padx=(0, 10))

top_level_window=Toplevel(window)
top_level_window.title("Изображение собачек")

notebook=ttk.Notebook(top_level_window)
notebook.pack(expand=True,fill='both',padx=10, pady=10 )



window.mainloop()



