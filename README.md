# to-do-list
A simple To do list with python and flask

Buenas gente! Aca les voy a dar los pasos para poner en funcionamiento la app, 
puede funcionar de forma remota como tambien esta preparada para desplegarse en linea.


1º Crear carpeta para la aplicacion (El comando es el mismo para Windows y Linux)

(Si estas en windows, ejecuta Powershell como administrador)

    mkdir todolist
    
2º Movete dentro de la carpeta todolist
    
    cd todolist

3º Te recomiendo crear un entorno virtual, este te permite guardar todas las dependencias necesarias para que la app funcione.

    python -m venv env


4º Activar entorno

Linux
    
    source env/bin/activate

Windows
    
    . env\Scripts\activate

NOTA IMPORTANTE(WINDOWS) : Si te surge un error de seguridad como me paso a mi, asegurate de estar ejecutando Powershell como administrador,
si el error persiste te recomiendo ejecutar este comando y dale que si cuando te pregunte.
                
    Set-ExecutionPolicy -ExecutionPolicy Unrestricted
    

5º Vamos a descargar el repositorio, dirigite a la pestaña de Code y copia el codigo, sino ejecuta directamente el codigo que te dejo

    git clone https://github.com/Parzival-ReadyPlayer/to-do-list.git

Este comando va a crear una carpeta dentro de todolist, con todos los archivos del repositorio
    
6º Comprobar los archivos 

    ls

7º Te tiene que figurar la carpeta to-do-list, movete a esa carpeta

    cd to-do-list

8º Instalar requirements.txt

    pip install -r requirements.txt
    
9º Si pones a correr la app en este momento, va a fallar y te explico por que. Utilizo este repositorio para desplegar la app, entonces las
variables de entorno deben estar en un archivo .env en la carpeta de la aplicacion to-do-list, este archivo se ignora al subirse al servidor mediante
el archivo .gitignore por cuestiones de seguridad.

Entonces, abri la carpeta to-do-list en tu editor de codigo

9)a)Crear archivo .env y dentro establece las variables de entorno
        
        SECRET_KEY=1634ff3506760f9677ea258cfb32deb8a35d6e21049d12f4f42b8f9bd7bb53e5
        SQLALCHEMY_DATABASE_URI=sqlite:////todo.db
        

El directorio deberia tener esta forma o similar

        │   .env
        │   .gitignore
        │   app.py
        │   Procfile
        │   README.md
        │   requirements.txt
        │
        ├───instance
        │       
        ├───static
        │       
        └───templates
       
10º Ultimo paso, volve a tu terminal, fijate que estes ubicado correctamente, con tu entorno virtual activado

        python app.py
        
Te va a figurar lo siguiente:

         * Serving Flask app 'app'
         * Debug mode: off
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
         * Running on http://127.0.0.1:5000
         
11º Copia la direccion y pegala en tu navegador

        http://127.0.0.1:5000


Si llegaste hasta aca te agradezco tu atencion, intente ser lo mas detallado posible pero si tenes algun error, podes consultarmelo.

La aplicacion todavia necesita mejorar su rendimiento pero funciona, si tenes una opinion o consejos, son bienvenidos, todos los dias se aprende algo.



