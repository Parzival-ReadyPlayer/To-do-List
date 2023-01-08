# to-do-list
A simple To do list with python and flask

Buenas gente! Aca les voy a dar los pasos para poner en funcionamiento la app, puede funcionar de forma remota como tambien esta preparada para desplegarse en linea.

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

NOTA IMPORTANTE: Si te surge un error de seguridad como me paso a mi, asegurate de estar ejecutando Powershell como administrador,
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
    

    




