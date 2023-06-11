import serial
import keyboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume    
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Configurar el puerto serial
puerto = 'COM6'  # Reemplaza con el puerto serial correcto en tu sistema
velocidad = 9600  # Reemplaza con la velocidad correcta en baudios
timeout = 1  # Tiempo de espera en segundos

# Crear una instancia del objeto Serial
ser = serial.Serial(puerto, velocidad, timeout=timeout)

try:
    def increase_volume():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        newVolume = volume.GetMasterVolumeLevel()+4
        if newVolume > 0:
            newVolume = 0
        volume.SetMasterVolumeLevel(newVolume, None)
        print(volume.GetVolumeRange())
        return volume.GetMasterVolumeLevel()


    def decrease_volume():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        newVolume = volume.GetMasterVolumeLevel()-4
        if newVolume < -65.25:
            newVolume = -65.25
        volume.SetMasterVolumeLevel(newVolume, None)
        return volume.GetMasterVolumeLevel()


    def next_track():
        keyboard.press_and_release('media_next')


    def previous_track():
        keyboard.press_and_release('media_previous')


    def play_pause():
        keyboard.press_and_release('media_play_pause')
        return "Pausa" if is_music_playing() else "Reanudar"

    def getRealVolume(value):
        minValue = -65.25
        maxValue = 0
        realValue = ((value - minValue) / (maxValue - minValue)) * 100
        return realValue

    def serialWrite(ser, data):
        print("Enviado:"+data)
        data_bytes = data.encode('utf-8')
        ser.write(data_bytes)
        
    while True:
        if ser.in_waiting > 0:
            # Leer la información recibida por el puerto serial
            code = ser.readline().decode('utf-8').rstrip()
            
            # Imprimir la línea recibida
            print("Recibido: " + code)

            # Actions
            if code == "1":
                previous_track()
                serialWrite(ser, "Cancion anterior")
            elif code == "2": 
                serialWrite(ser, play_pause())  
            elif code == "3":
                next_track()   
                serialWrite(ser, "Siguiente cancion")
            elif code == "6":   
                current_volume = increase_volume()
                serialWrite(ser, "Volumen: " + str(int(getRealVolume(current_volume))))
            elif code == "9":
                current_volume = decrease_volume()
                serialWrite(ser, "Volumen: " + str(int(getRealVolume(current_volume))))


except KeyboardInterrupt:
    # Cerrar la conexión serial al interrumpir el programa
    ser.close()

