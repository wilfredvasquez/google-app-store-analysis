# google-app-store-analysis

## Crear el entorno virtual

Se necesita crear un entorno virtual para que los módulos que instalemos solo afecten este desarrollo

**Opción 1:**

- Instalar virtualenv, crear el entorno y activarlo:

```
# sudo apt install virtualenv
# virtualenv env
# source env/bin/activate
```

**Opción 2:**

- Instalar python3-venv, crear el entorno y activarlo

```
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
```

## Instalar requerimientos

El archivo requeriments.txt contiene los módulo necesarios para que nuestro programa funcione. Con el siguiente comando hacemos que se instalen todos.

```
pip install -r requirements.txt
```

## Limpiar el dataset

Ejecutar el archivo python clean_dataset.py. El hará la limpieza necesaria y generará un nuevo archivo con el dataset procesado

```
python3 clean_dataset.py
```
