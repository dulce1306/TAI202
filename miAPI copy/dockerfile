#importar imagen base de python
FROM python:3.12-slim

#Crear en el contenedor la Carpeta Trabajo
WORKDIR /app

#Copiar los requerimentos al contenedor
COPY requirements.txt .

#Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt 

#Copia el codigo del servidor
COPY ./app ./app 

#Exponer el puerto de trabajo
EXPOSE 5000

#Comando a ejecutar levantar servidor
CMD ["uvicorn","app.main:app","--host", "0.0.0.0", "--port", "5000", "--reload"]