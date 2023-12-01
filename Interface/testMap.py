from PIL import Image, ImageDraw, ImageTk
import math
import tkinter as tk
from threading import Thread
import time
import imageio

def polygonDirection(angle1, angle2, width, height):
    center = (width/2, height/2)

    angle1 = angle1%360
    angle2 = angle2%360
    
    if(angle1 < 45 or angle1 >= 315):
        point1 = (width,  height/2 - width*math.tan(angle1*math.pi/180)/2)

    elif (angle1 < 135):
        point1 = (width/2 + height/(2*math.tan(angle1*math.pi/180)), 0)

    elif (angle1 < 225):
        point1 = (0, height/2 - width*math.tan(math.pi - angle1*math.pi/180)/2)

    elif (angle1 < 315):
        point1 = (width/2 - height*(math.tan(3*math.pi/2 - angle1*math.pi/180))/2, height)

    if(angle2 < 45 or angle2 >= 315):
        point2 = (width, height/2 - width*math.tan(angle2*math.pi/180)/2)

    elif (angle2 < 135):
        point2 = (width/2 + height/(2*math.tan(angle2*math.pi/180)), 0)

    elif (angle2 < 225):
        point2 = (0, height/2 - width*math.tan(math.pi - angle2*math.pi/180)/2)

    elif (angle2 < 315):
        point2 = (width/2 - height*(math.tan(3*math.pi/2 - angle2*math.pi/180))/2, height)


    point1 = (point1[0] + point1[0] - width/2, point1[1] + point1[1] - height/2)
    point2 = (point2[0] + point2[0]- width/2, point2[1] + point2[1] - height/2)

    return [(width/2, height/2), point1, point2]

def drawMap(color, angles, points, areas,panel):
    im = Image.open("Images/basedrone2.png").resize((700, 350)).convert('RGBA')
    width, height = im.width, im.height
    drone = Image.open("Images/drone.png").resize((50,25)).convert('RGBA')
    d = ImageDraw.Draw(im)
    widthDrone, heightDrone = drone.size
    #print(angles[0][0], angles[0][1])
    

    for angle in angles:
        d.polygon(polygonDirection(angle[0], angle[1], width, height), fill=color, outline=color)

    for x in points:
        tamanho_ponto = 10
        d.line((x[0] - tamanho_ponto, x[1] - tamanho_ponto, x[0] + tamanho_ponto, x[1] + tamanho_ponto), fill=x[2], width=5)
        d.line((x[0] + tamanho_ponto, x[1] - tamanho_ponto, x[0] - tamanho_ponto, x[1] + tamanho_ponto), fill=x[2],width=5)

    for area in areas:
        tamanho_ponto = area[2]
        d.ellipse((area[0] - tamanho_ponto, area[1] - tamanho_ponto, area[0] + tamanho_ponto, area[1] + tamanho_ponto), fill=area[3])


    # x_ponto = 3*width/4
    # y_ponto = 3*height/4
    # tamanho_ponto = 10
    # d.line((x_ponto - tamanho_ponto, y_ponto - tamanho_ponto, x_ponto + tamanho_ponto, y_ponto + tamanho_ponto), fill='red', width=5)
    # d.line((x_ponto + tamanho_ponto, y_ponto - tamanho_ponto, x_ponto - tamanho_ponto, y_ponto + tamanho_ponto), fill='red',width=5)

    im.paste(drone, (int(width/2 - widthDrone/2), int(height/2 - heightDrone/2)))

    photo = ImageTk.PhotoImage(im)

    panel.configure(image=photo)
    panel.image = photo

def MapLoop(panel, im):
    a1 = 0
    a2 = 20

    a3 = 180
    a4 = 200

    x1 = 300
    y1 = 100
    x2 = 200
    y2 = 300

    while(1):
        drawMap('green', [(a1,a2), (a3,a4)], [(x1,y1,'blue'), (x2,y2, 'yellow')], [(300, 500, 50, '#f3000faa')],panel)
        a1 += 1
        a2 += 1
        a3 += 1
        a4 += 1
    
def obter_dimensoes_tela():
    largura = root.winfo_screenwidth()
    altura = root.winfo_screenheight()
    return largura, altura

def obter_quadro(video, index):
    try:
        quadro = video.get_data(index)
        quadro_redimensionado = Image.fromarray(quadro).resize((700, 350))
        return ImageTk.PhotoImage(quadro_redimensionado)
  
    except Exception as e:
        print(e)
        return None

def videoPlayer(panel):
    
    video = imageio.get_reader('Images/video.mp4')
    index = 0
    while True:
        # print('in here')
        quadro = obter_quadro(video, index)
        if quadro is not None:
            panel.configure(image=quadro)
            panel.image = quadro
            index += 1
        else:
            index = 0

def click1(event):
    # Obtém as coordenadas do clique
    x, y = event.x, event.y
    print(f"Clique 1: Clique detectado em ({x}, {y})")

def click2(event):
    # Obtém as coordenadas do clique
    x, y = event.x, event.y
    print(f"Click 2: Clique detectado em ({x}, {y})")

def click3(event):
    # Obtém as coordenadas do clique
    x, y = event.x, event.y
    print(f"Click 3: Clique detectado em ({x}, {y})")

# Crie a janela principal
root = tk.Tk()
root.title("SEDRO")
largura_tela, altura_tela = obter_dimensoes_tela()

root.geometry(f"{largura_tela}x{altura_tela}")
root.configure(bg="#303030")

panel = tk.Label(root)

img = Image.open("Images/videodrone.png").resize((700, 350)).convert('RGBA')
img_tk = ImageTk.PhotoImage(img)
panel2 = tk.Label(root, image = img_tk)


img = Image.open("Images/videodrone.png").resize((700, 350)).convert('RGBA')
img_tk = ImageTk.PhotoImage(img)
panel3 = tk.Label(root, image = img_tk)

panel.bind("<Button-1>", click1)  # <Button-1> representa o clique do botão esquerdo do mouse
panel2.bind("<Button-1>", click2)  # <Button-1> representa o clique do botão esquerdo do mouse
panel3.bind("<Button-1>", click3)  # <Button-1> representa o clique do botão esquerdo do mouse

panel.place(x=root.winfo_screenwidth() - 750, y=20)
panel2.place(y=root.winfo_screenheight() - 460, x=root.winfo_screenwidth() - 750)
panel3.place(y=root.winfo_screenheight() - 460, x=40)


# Inicie a thread
thread = Thread(target=MapLoop, args=(panel, img))
thread2 = Thread(target=videoPlayer, args=(panel2,))
thread.daemon = True 
thread2.daemon = True 

thread.start()
thread2.start()

# Inicie o loop principal da interface gráfica
root.mainloop()
