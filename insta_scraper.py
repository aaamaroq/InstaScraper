from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import maskpass
from time import sleep
import pyautogui
import requests
import os
import json
import pyttsx3


class InstagramScraper:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None

    def _descargar_imagen(sef,url, nombre_archivo):
        carpeta = "imagenes"
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        if not os.path.exists(ruta_archivo):
            response = requests.get(url)
            if response.status_code == 200:
                with open(ruta_archivo, "wb") as archivo:
                    archivo.write(response.content)


    def create_session(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com/accounts/login/")
        self.driver.maximize_window()
        sleep(2)
        username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        sleep(5)


    def _obtenerUsuarios(self):
        # Encontrar todas las imágenes con el atributo alt que comience con "Foto del perfil de"
        imagenes = self.driver.find_elements(By.XPATH,"//img[starts-with(@alt, 'Foto del perfil de')]")
        #Para cada perfil obtenemos el elemento imagen y sus nombres
        usuarios= []

        for imagen in imagenes:
            # Obtener el contenido del atributo alt
            alt_text = imagen.get_attribute("alt")
            #Limpiamos el texto
            usuario = alt_text.replace("Foto del perfil de ", "")
            #descargamos su foto de perfil
            #self._descargar_imagen(imagen.get_attribute("src"), usuario + ".jpg")
            #añadimos el usuario
            usuarios.append(usuario)

        return usuarios

    def scrape_following(self, name, principal=True, misSeguidores = []):

        #Dirigirnos a la pagina y esperar que carge
        url= "https://www.instagram.com/"+name+"/following"

        print(url)
        self.driver.get(url)
        sleep(5)

        

        viejo_listado=0
        listado=1
        #Definimos las coordeandas exactas
        x=1187
        start_y=480
        end_y=800
        #movemos el ratón a las primeras coordeandas
        #volver arriba el ratón a las primeras coordeandas
        pyautogui.moveTo(x, start_y, duration=0.5)
        parada=False

        usuarios = []

        while( not parada):

            viejo_listado=listado


            # Hacer clic y mantener pulsado el botón izquierdo
            pyautogui.mouseDown()

            #movemos el ratón a hacia abajo
            pyautogui.moveTo(x, end_y, duration=0.5)

            #Esperar que carge
            sleep(5)

            #volver arriba el ratón a las primeras coordeandas
            pyautogui.moveTo(x, start_y, duration=0.5)

            # Soltar el botón izquierdo del ratón
            pyautogui.mouseUp()

            # Comprobamos si hay algún usuario que siga que yo no sigo y de ser así paramos (si es un seguidor)
            usuarios = self._obtenerUsuarios()

            diferencia = set(usuarios).difference(set(misSeguidores))


            if len(diferencia) > 0 and not principal:
                parada = True
                print("PARO!"+str(set(usuarios).difference(set(misSeguidores))))

            # Comprobamos si el numero de usuarios ha cambiado si no es así es que no hay mas y paramos
            listado = len(usuarios)

            if(listado==viejo_listado):
                parada=True

            print("viejo listado : "+str(viejo_listado)+ " listado : "+ str(listado))


        # Eliminamos el usuario de la lista de sus seguidores
        usuarios.remove(name)

        if principal:
            return usuarios
        else:
            return  [elemento for elemento in usuarios if elemento in misSeguidores]

            
# Cargamos el reproductor de voz
engine = pyttsx3.init()
engine.setProperty("rate", 150) # Ajusta la velocidad a 150 palabras por minuto
engine.setProperty("voice", "spanish") # Selecciona una voz en español

# Ejemplo de uso
# Iniciamos sesión con ocntraseña segura y obtenemos nuestros seguidores
username = input("Intrduce el usuario:")
password = maskpass.askpass(prompt="Introduce la contraseña: ", mask="*")
scraper = InstagramScraper(username, password)
scraper.create_session()
map= dict()

usuarios = scraper.scrape_following(username)
map[username] = usuarios


# mostramos nuestros seguiddores
print("mis seguidores son")
print(usuarios)

# Comprobamos si vamos a ejecutar o rescatar perjudicados
opcion = input("¿Quiere realizar ejecución o rescatar perjudicados (1/2)? ")
listado=[]


if opcion == "1":
    # Si es la primera ejecución
    # Guardar archivos perjudicados.json y relaciones.json con el contenido []
    data = []
    with open("perjudicados.json", "w") as perjudicados_file:
        json.dump(data, perjudicados_file)

    with open("relaciones.json", "w") as relaciones_file:
        json.dump(data, relaciones_file)

    listado=usuarios


elif opcion == "2":
    # Código para rescatar perjudicados

    # Abrir el archivo JSON
    with open('perjudicados.json') as f:
        listado = json.load(f)


    with open('relaciones.json') as f:
        map = json.load(f)


perjudicados=[]

# Obtenemos las coincidencias entre las personas que sigo y las que siguen mis seguidores
i=0
print(len(listado))

for usuario in listado:

    i=i+1
    # Indicamos el porcentaje por el que va es multiplo de 10 lo indicamos
    porcentaje = (i + 1) * 100 / len(listado)
    if porcentaje % 10 == 0:
        engine.say(str(porcentaje)+ " por ciento")
        engine.runAndWait()

    print("EL USUARIO ACTUAL ES "+usuario)
    map[usuario] = scraper.scrape_following(usuario,principal= False,misSeguidores = usuarios)
    if len(map[usuario]) <= 2:
        perjudicados.append(usuario)

print("PERJUDICADOS:")
print(perjudicados)
# Guardar el vector como archivo JSON
with open("perjudicados.json", "w") as archivo:
    json.dump(perjudicados, archivo)


# Guardar el mapa como archivo JSON
with open("relaciones.json", "w") as archivo:
    json.dump(map, archivo)

