import serial
import time
from datetime import datetime
import qrcode
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import cv2
from screeninfo import get_monitors
import os


# -------------------------------
# CONEXÃO COM ARDUINO
# -------------------------------

def conectar_arduino():

    try:
        arduino = serial.Serial('COM3',9600,timeout=1)
        time.sleep(2)
        print("Arduino conectado")
        return arduino

    except:
        print("Erro ao conectar Arduino")
        return None


# -------------------------------
# GOOGLE DRIVE
# -------------------------------

def conectar_drive():

    try:

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        print("Google Drive conectado")

        return drive

    except Exception as e:

        print("Erro Google Drive:",e)
        return None


# -------------------------------
# CAPTURAR FOTO
# -------------------------------

def capturar_foto():

    try:

        cam = cv2.VideoCapture(0)

        if not cam.isOpened():
            print("Webcam não encontrada")
            return None

        ret, frame = cam.read()

        cam.release()

        if ret:

            nome = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

            cv2.imwrite(nome, frame)

            print("Foto salva:",nome)

            return nome

        else:

            print("Erro ao capturar foto")
            return None

    except Exception as e:

        print("Erro webcam:",e)
        return None


# -------------------------------
# UPLOAD GOOGLE DRIVE
# -------------------------------

def enviar_drive(drive,arquivo):

    try:

        file_drive = drive.CreateFile({'title':arquivo})
        file_drive.SetContentFile(arquivo)
        file_drive.Upload()

        link = file_drive['alternateLink']

        print("Upload feito")

        return link

    except Exception as e:

        print("Erro upload:",e)
        return None


# -------------------------------
# GERAR QR CODE
# -------------------------------

def gerar_qr(link):

    try:
        nome_qr = "qr_" + datetime.now().strftime("%H%M%S") + ".png"
        qr = qrcode.make(link)
        qr.save(nome_qr)
        return nome_qr
    except:
        print("Erro QR")
        return None


# -------------------------------
# MOSTRAR QR CODE NO SEGUNDO MONITOR
# -------------------------------

def mostrar_qr(qr):

    try:
        monitores = get_monitors()
        if len(monitores) < 2:
            print("Segundo monitor não encontrado")
            return
        
        monitor = monitores[1]
        x = monitor.x
        y = monitor.y
        w = monitor.width
        h = monitor.height
        img = cv2.imread(qr)
        img = cv2.resize(img,(w,h))
        cv2.namedWindow("QR", cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow("QR",x,y)
        cv2.setWindowProperty("QR",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("QR",img)
        cv2.waitKey(10000)
        cv2.destroyWindow("QR")

    except Exception as e:

        print("Erro monitor:",e)


# -------------------------------
# PROGRAMA PRINCIPAL
# -------------------------------

def main():

    arduino = conectar_arduino()
    drive = conectar_drive()

    if arduino == None or drive == None:

        print("Erro inicialização")
        return


    print("Cabine pronta...")

    while True:

        try:

            comando = arduino.readline().decode().strip()

            if comando == "Capture":

                print("Tirando foto...")

                foto = capturar_foto()

                if foto:

                    link = enviar_drive(drive,foto)

                    if link:

                        qr = gerar_qr(link)

                        if qr:

                            mostrar_qr(qr)

        except Exception as e:

            print("Erro execução:",e)


# -------------------------------

if __name__ == "__main__":
    main()