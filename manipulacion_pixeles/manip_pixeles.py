import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

class CameraApp:
    def __init__(self, root):

        # Inicializa la ventana principal de la aplicación
        self.root = root
        self.root.title("Fusionar Cámaras")
        self.root.geometry("1200x600") 
        
        # Variables para almacenar las cámaras
        self.cap1 = None
        self.cap2 = None

        # aaarear y colocar las etiquetas de las cámaras
        self.label1 = Label(root)
        self.label1.grid(row=0, column=0)

        self.label2 = Label(root)
        self.label2.grid(row=0, column=1)

        self.label_merged = Label(root)
        self.label_merged.grid(row=1, column=0, columnspan=2)

        # Crear y colocar los botones
        self.btn_iniciar = Button(root, text="INICIAR CAMARAS", command=self.iniciar_camaras)
        self.btn_iniciar.grid(row=2, column=0, columnspan=2)
        
        self.btn_fusionar = Button(root, text="FUSIONAR CAMARAS", command=self.fusionar)
        self.btn_fusionar.grid(row=3, column=0, columnspan=2)

        self.btn_salir = Button(root, text="SALIR", command=self.salir)
        self.btn_salir.grid(row=4, column=0, columnspan=2)

    def iniciar_camaras(self):
        # Inicializar las cámaras
        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(1)
        self.update_frames()

    def update_frames(self):
        if self.cap1 is not None and self.cap2 is not None:
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()

            if ret1 and ret2:
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

                frame1 = self.add_label(frame1, "Persona")
                frame2 = self.add_label(frame2, "Fondo")

                img1 = Image.fromarray(frame1)
                img2 = Image.fromarray(frame2)

                imgtk1 = ImageTk.PhotoImage(image=img1)
                imgtk2 = ImageTk.PhotoImage(image=img2)

                self.label1.imgtk = imgtk1
                self.label1.configure(image=imgtk1)

                self.label2.imgtk = imgtk2
                self.label2.configure(image=imgtk2)

            self.root.after(10, self.update_frames)

    def add_label(self, frame, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 30)
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        cv2.putText(frame, text, 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
        return frame

    def fusionar(self):
        lector = LectorVideo()
        lector.captura_video()

    def salir(self):
        # Liberar cámaras y cerrar ventanas
        self.__del__()
        self.root.destroy()

    def __del__(self):
        # Liberar cámaras y cerrar ventanas de OpenCV
        if self.cap1 is not None:
            self.cap1.release()
        if self.cap2 is not None:
            self.cap2.release()
        cv2.destroyAllWindows()

class LectorVideo:
    def __init__(self):
        print(cv2.__version__)

    def eventoTrack(self, valor):
        pass

    def captura_video(self):
        cv2.namedWindow('Cam1_persona', cv2.WINDOW_AUTOSIZE)

        # Crear trackbars para ecualización y binarización
        cv2.createTrackbar('Clip-Limit', 'Cam1_persona', 40, 250, self.eventoTrack)
        cv2.createTrackbar('Tile-Size', 'Cam1_persona', 8, 250, self.eventoTrack)
        cv2.setTrackbarMin('Tile-Size', 'Cam1_persona', 1)
        cv2.createTrackbar('Hmin', 'Cam1_persona', 1, 180, self.eventoTrack)
        cv2.createTrackbar('Smin', 'Cam1_persona', 37, 255, self.eventoTrack)
        cv2.createTrackbar('Vmin', 'Cam1_persona', 61, 255, self.eventoTrack)

        cv2.createTrackbar('Hmax', 'Cam1_persona', 133, 180, self.eventoTrack)
        cv2.createTrackbar('Smax', 'Cam1_persona', 229, 255, self.eventoTrack)
        cv2.createTrackbar('Vmax', 'Cam1_persona', 209, 255, self.eventoTrack)

        cv2.createTrackbar('Umbral', 'Cam1_persona', 50, 200, self.eventoTrack)

        video = cv2.VideoCapture(0)  # Captura a la persona en cromo
        video2 = cv2.VideoCapture(1)  # Captura el fondo paisaje

        if video.isOpened() and video2.isOpened():
            while True:
                ret1, frame1 = video.read()
                ret2, frame2 = video2.read()

                if not ret1 or not ret2:
                    break

                img_lab = cv2.cvtColor(frame1, cv2.COLOR_BGR2Lab)
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                ecualizada = cv2.equalizeHist(frame1)
                clahe = cv2.createCLAHE()
                clahe.setTilesGridSize((cv2.getTrackbarPos('Tile-Size', 'Cam1_persona'),
                                       cv2.getTrackbarPos('Tile-Size', 'Cam1_persona')))
                clahe.setClipLimit(cv2.getTrackbarPos('Clip-Limit', 'Cam1_persona'))
                img_clahe = clahe.apply(frame1)

                img_lab[:, :, 0] = clahe.apply(img_lab[:, :, 0])
                clahe_color = cv2.cvtColor(img_lab, cv2.COLOR_Lab2BGR)

                frame = cv2.flip(clahe_color, 1)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                binaria = cv2.inRange(hsv,
                                      (cv2.getTrackbarPos('Hmin', 'Cam1_persona'),
                                       cv2.getTrackbarPos('Smin', 'Cam1_persona'),
                                       cv2.getTrackbarPos('Vmin', 'Cam1_persona')),
                                      (cv2.getTrackbarPos('Hmax', 'Cam1_persona'),
                                       cv2.getTrackbarPos('Smax', 'Cam1_persona'),
                                       cv2.getTrackbarPos('Vmax', 'Cam1_persona'))
                                      )

                img_and = cv2.bitwise_and(frame, frame, mask=binaria)

                kernel = np.ones((5, 5), np.uint8)
                binaria = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel)
                binaria = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)

                frame = cv2.cvtColor(img_and, cv2.COLOR_BGR2GRAY)
                frame = cv2.resize(frame, dsize=(0, 0), fx=0.80, fy=0.80)

                frame = cv2.GaussianBlur(frame, (5, 5), sigmaX=1.3, sigmaY=1.3)

                gX = cv2.Sobel(frame, ddepth=cv2.CV_16S, dx=1, dy=0, ksize=5)
                gY = cv2.Sobel(frame, ddepth=cv2.CV_16S, dx=0, dy=1, ksize=5)

                gXAbs = cv2.convertScaleAbs(gX)
                gYAbs = cv2.convertScaleAbs(gY)
                gXY = cv2.addWeighted(gXAbs, 0.5, gYAbs, 0.5, gamma=1.0)

                laplaciano = cv2.Laplacian(frame, ddepth=cv2.CV_16S, ksize=5)
                laplaciano = cv2.convertScaleAbs(laplaciano)

                img_canny = cv2.Canny(frame, float(cv2.getTrackbarPos('Umbral', 'Cam1_persona')),
                                      float(cv2.getTrackbarPos('Umbral', 'Cam1_persona')) * 2.7)

                edges_colored = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
                edges_colored = cv2.resize(edges_colored, (img_and.shape[1], img_and.shape[0]))

                combined = cv2.addWeighted(img_and, 0.5, edges_colored, 0.5, 0)

                mask_inv = cv2.bitwise_not(binaria)
                fondo = cv2.bitwise_and(frame2, frame2, mask=mask_inv)

                resultado = cv2.add(fondo, combined)

                cv2.imshow('Cam1_persona', resultado)

                if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' key to quit
                    break

            video.release()
            video2.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    app = CameraApp(root)
    root.mainloop()