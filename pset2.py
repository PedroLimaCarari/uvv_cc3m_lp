#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage

## NO ADDITIONAL IMPORTS ALLOWED!

def k_desfoque(n): # gera o kernel de desfoque
    return [[1 / (n ** 2) for x in range(n)]for x in range(n)] # 1 dividido pelo tamanho do kernel ao quadrado para cada pixel no kernel

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels

    def get_pixel(self, x, y):      # pega a cor do pixel nas cordenadas X e Y
        if x < 0:  # correção de erro
            x = 0
        elif x >= self.width - 1:  # correção de erro
            x = self.width - 1
        if y < 0:  # correção de erro
            y = 0
        elif y >= self.height - 1:  # correção de erro
            y = self.height - 1
        return self.pixels[(x + y * self.width)]

    def set_pixel(self, x, y, c): # muda a cor do pixel para a cor nova desejada
        self.pixels[(x + y * self.width)] = c


    def apply_per_pixel(self, func): # aplica a função desejada em cada pixel da imagem
        result = Image.new(self.width, self.height)
        for x in range(result.width):
            for y in range(result.height):
                color = self.get_pixel(x, y)
                newcolor = func(color)
                result.set_pixel(x, y, newcolor)

        return result

    def inverted(self): # inverte as cores da imagem escolhida utilizando a função abaixo, que consiste em pegar 255 e diminuir do valor do pixel
        return self.apply_per_pixel(lambda c: 255 - c)

    def blurred(self, n): # é uma função utilizada para borrar a imagem
        kernel = k_desfoque(n) # chama a função que gera o kernel para desfoque
        desfoque = self.correlacao(kernel) 
        desfoque.acertar()
        return desfoque

    def sharpened(self, n): # é uma função para deixar uma imagem nítida 
        img_borrada = self.blurred(n)
        img_nitidez = Image.new(self.width, self.height)
        for i in range(self.width):
            for j in range(self.height):
                img_nitidez.set_pixel(i, j, round(2 * self.get_pixel(i, j) - img_borrada.get_pixel(i, j))) # aplica a função imag_nitidez para cada pixel 
        img_nitidez.acertar()                                                                              # onde ele pega o dobro do valor do pixel da imagem padrão
        return img_nitidez                                                                                 # e diminui da imagem borrada

    def edges(self, k1, k2):    # é uma função para detectar as boras da imagem
        img1 = self.correlacao(k1)  # cria 2 imagens para 2 kerneis
        img2 = self.correlacao(k2)
        img_borda = Image.new(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                img_borda.set_pixel(x, y, round(math.sqrt(img1.get_pixel(x, y) ** 2 + img2.get_pixel(x, y) ** 2))) # arredonda a raiz quadrada da soma do valor de  
        img_borda.acertar()        # chama a função acertar para a imagem final                                    # entrada ao quadrado da img 1 e 2
        return img_borda

    def correlacao(self, kernel):                       # a função de correlação é a função responsável por aplicar o kernel nas imagens requeridas
        z = len(kernel)                                 # essa função verifica
        meio = z // 2
        image_new = Image.new(self.width, self.height)
        for x in range(image_new.width):
            for y in range(image_new.height):
                color_new = 0
                for a in range(z):
                    for b in range(z):
                        color_new += self.get_pixel((x - meio + b), (y - meio + a)) * kernel[a][b] 
                image_new.set_pixel(x, y, color_new)
        return image_new

    def acertar(self):             # corrige problemas nos valores do pixel 
        for x in range(self.width):
            for y in range(self.height):
                pixel = self.get_pixel(x, y)
                if pixel < 0:      # deixa os pixeis em um intervalo de o a 255 e o arredonda para o valor inteiro mais próximo
                    pixel = 0   
                elif pixel > 255:
                    pixel = 255
                pixel = int(round(pixel))
                self.set_pixel(x, y, pixel)

    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    def __repr__(self):
        return "Image(%s, %s, %s)" % (self.width, self.height, self.pixels)

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass

    #Questão 2
    # i = Image.load('test_images/bluegill.png')
    #inv = i.inverted()
    #inv.save('test_results/peixe.png')

    #Questão 4
    #kernelq4 = [[0,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0],
    #            [1,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0],
    #            [0,0,0,0,0,0,0,0,0]]
    #i = Image.load('test_images/pigbird.png')
    #i.show()
    #renato = i.correlacao(kernelq4)
    #renato.show()
    #renato.save('test_results/porco.png')

    #Questão 4 parte 2
    #i = Image.load('test_images/cat.png')
    #bor = i.blurred(5)
    #i.show()
    #bor.show()
    #jubileu = i.blurred(5)
    #jubileu.save('test_results/cat.png')

    # Questão 5
    # kernel1 = [[0, 0, 0],
    #            [0, 2, 0],
    #            [0, 0, 0]]
    # kernel2 = [[1/9, 1/9, 1/9],
    #            [1/9, 1/9, 1/9],
    #            [1/9, 1/9, 1/9]]
    # kernel = [[-1/9, -1/9, -1/9],
    #           [-1/9, 17/9, -1/9],
    #           [-1/9, -1/9, -1/9]]
    # i = Image.load('test_images/python.png')
    # nitidez = i.correlacao(kernel)
    # nitidez.show()
    # i.show()
    # roberto = i.sharpened(11)
    # roberto.save('test_results/python.png')

    # Questão 6
    #i = Image.load('test_images/obra.png')
    #borda = i.edges([[-1, 0, 1],
    #                 [-2, 0, 2],
    #                 [-1, 0, 1]], [[-1, -2, -1],
    #                               [0,   0,  0],
    #                               [1,   2,  1]])
    #i.show()
    #borda.show()
    #yuri = i.edges([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]], [[-1, -2, -1],[0, 0, 0],[1, 2, 1]])
    #yuri.save('test_results/obra.png')

    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
