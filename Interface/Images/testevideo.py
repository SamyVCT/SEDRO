import tkinter as tk
from PIL import Image, ImageTk
import imageio
from threading import Thread
import time

def obter_dimensoes_tela():
    largura = root.winfo_screenwidth()
    altura = root.winfo_screenheight()
    return largura, altura

def carregar_video(file_path):
    video = imageio.get_reader(file_path)
    return video

def obter_quadro(video, index):
    try:
        quadro = video.get_data(index)
        return Image.fromarray(quadro)
    except Exception as e:
        print(e)
        return None

def testLoop(panel, video):
    index = 0

    while True:
        quadro = obter_quadro(video, index)
        if quadro is not None:
            photo = ImageTk.PhotoImage(quadro)
            panel.configure(image=photo)
            panel.image = photo
            index += 1
        else:
            index = 0

def escolher_video():
    file_path = tk.filedialog.askopenfilename(filetypes=[("Arquivos de vídeo", "*.mp4;*.avi;*.mkv")])
    if file_path:
        root.withdraw()
        video = carregar_video(file_path)
        thread = Thread(target=testLoop, args=(panel, video))
        thread.daemon = True
        thread.start()
        root.deiconify()

# Crie a janela principal
root = tk.Tk()
root.title("SEDRO")

largura_tela, altura_tela = obter_dimensoes_tela()
root.geometry(f"{largura_tela}x{altura_tela}")

panel = tk.Label(root)
panel.place(x=root.winfo_screenwidth() - 750, y=20)

# Botão para escolher um vídeo
select_button = tk.Button(root, text="Escolher Vídeo", command=escolher_video)
select_button.place(x=root.winfo_screenwidth() - 750, y=root.winfo_screenheight() - 50)

# Inicie o loop principal da interface gráfica
root.mainloop()