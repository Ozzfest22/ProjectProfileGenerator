from ProjectProfileGenerator.ConexionDB.conexion import obtener_conexion
from ProjectProfileGenerator.Routes.rutas_login import get_Id
from flask import session
from deepface import DeepFace
import mediapipe as mp
import cv2


def insertar_datos(edad, gen, race, emociones, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("exec sp_InsertarPerfil ?, ?, ?, ?, ?", edad, gen, race, emociones, id)
        
    conexion.commit()
    conexion.close()

def obtener_perfil(Id):
    conexion = obtener_conexion()
    perfil = None
    with conexion.cursor() as cursor:
        cursor.execute("exec sp_ObtenerPerfil ?", Id)
        perfil = cursor.fetchone()

    conexion.close()
    return perfil


detros = mp.solutions.face_detection
rostros = detros.FaceDetection(min_detection_confidence= 0.8, model_selection=0)

dibujorostro = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)


def generate():
     numero = 0

     while True:
        ret, frame = cap.read()
        
        img =cv2.imread("ProjectProfileGenerator/static/img.png")

        img = cv2.resize(img, (0, 0), None, 0.18, 0.18)
        ani, ali, c = img.shape

        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        
        resrostros = rostros.process(rgb)

        
        if resrostros.detections is not None:
            
            for rostro in resrostros.detections:
                
                al, an, c = frame.shape
                box = rostro.location_data.relative_bounding_box
                xi, yi, w, h = int(box.xmin * an), int(box.ymin * al), int(box.width * an), int(box.height * al)
                xf, yf = xi + w, yi + h

                
                cv2.rectangle(frame, (xi, yi), (xf, yf), (255, 255, 0), 1)
                frame[10:ani + 10, 10:ali+10] = img

                
                info = DeepFace.analyze(rgb, actions=['age', 'gender', 'race', 'emotion'], enforce_detection= False)

                
                edad = info['age']

                
                emociones = info['dominant_emotion']

                
                race = info['dominant_race']

                
                gen = info['gender']
                

                # Traducimos
                if gen == 'Man':
                    gen = 'Hombre'

                    # Emociones
                    if emociones == 'angry':
                        emociones = 'enojado'
                    if emociones == 'disgust':
                        emociones = 'disgustado'
                    if emociones == 'fear':
                        emociones = 'miedoso'
                    if emociones == 'happy':
                        emociones = 'feliz'
                    if emociones == 'sad':
                        emociones = 'triste'
                    if emociones == 'surprise':
                        emociones = 'sorprendido'
                    if emociones == 'neutral':
                        emociones = 'neutral'

                    # Race
                    if race == 'asian':
                        race = 'asiatico'
                    if race == 'indian':
                        race = 'indio'
                    if race == 'black':
                        race = 'negro'
                    if race == 'white':
                        race = 'blanco'
                    if race == 'middle eastern':
                        race = 'oriente medio'
                    if race == 'latino hispanic':
                        race = 'latino'

                elif gen == 'Woman':
                    gen = 'Mujer'

                    # Emociones
                    if emociones == 'angry':
                        emociones = 'enojada'
                    if emociones == 'disgust':
                        emociones = 'disgustada'
                    if emociones == 'fear':
                        emociones = 'miedosa'
                    if emociones == 'happy':
                        emociones = 'feliz'
                    if emociones == 'sad':
                        emociones = 'triste'
                    if emociones == 'surprise':
                        emociones = 'sorprendida'
                    if emociones == 'neutral':
                        emociones = 'neutral'

                    # Race
                    if race == 'asian':
                        race = 'asiatica'
                    if race == 'indian':
                        race = 'india'
                    if race == 'black':
                        race = 'negra'
                    if race == 'white':
                        race = 'blanca'
                    if race == 'middle eastern':
                        race = 'oriente medio'
                    if race == 'latino hispanic':
                        race = 'latina'

                
                cv2.putText(frame, str(gen), (65, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(frame, str(edad), (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(frame, str(emociones), (75, 135), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(frame, str(race), (75, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                
                if numero == 5:                   
                    Id = get_Id()
                    insertar_datos(edad, gen, race, emociones, Id)
                    print('Datos insertados')
 
                    

                numero += 1         


        
        suc, encode = cv2.imencode('.jpg', frame)
        frame = encode.tobytes()
        
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(frame) + b'\r\n')



        