# Procesamiento de PDFs para Extracción de Números de Proceso

Este script, `main.py`, permite procesar un conjunto de archivos PDF dentro de un directorio y extraer números de proceso escritos a mano utilizando OCR (Reconocimiento Óptico de Caracteres). Utiliza tanto PaddleOCR como EasyOCR para realizar la extracción automática de números. Si no se encuentra el número de proceso en el archivo, el programa tiene la opción de pedir la entrada manual del número.

## Requerimientos

Para ejecutar este proyecto, necesitas tener instaladas las dependencias listadas en el archivo `requirements.txt`. Puedes instalarlas con:

pip install -r requirements.txt


### Dependencias principales
- `paddleocr`
- `easyocr`
- `pdf2image`
- `Pillow`
- `opencv-python`
- `tkinter` (incluido por defecto en la mayoría de las instalaciones de Python)
- `numpy`

## Uso

1. Coloca todos los archivos PDF en una carpeta llamada `SOLICITUD` (SOLICITUD\ANCUD\ANCUD 1) o en la que prefieras procesar.
2. Ejecuta el script principal `main.py`. Este procesará los archivos `SOL.PDF` dentro de la carpeta especificada.

```bash
python main.py
```

3. El script intentará extraer el número de proceso de la primera página de cada archivo PDF.

### Estructura de carpetas
El script buscará en la carpeta SOLICITUD (o la que especifiques) archivos llamados SOL.PDF y procesará estos archivos uno por uno.

### Flujo de procesamiento
El script convierte la primera página del archivo PDF a una imagen.
Luego utiliza PaddleOCR para intentar detectar un número de proceso que comience con 16, 17 o 18.
Si PaddleOCR no encuentra ningún número válido, EasyOCR hará el intento.
Si ninguno de los dos detecta un número, el programa puede mostrar una interfaz gráfica para ingresar el número manualmente.

### Procesamiento manual
Si deseas introducir el número de proceso de manera manual, debes comentar el return en la siguiente sección del código:

```python
if not numero_proceso:
    return  # Comentar esta línea si quieres introducir manualmente el número
    log_message("Ningún OCR detectó el número de proceso, mostrando GUI manual.")
    manual_input_gui(jpg_path, pdf_path)
```

### Salida
Si se encuentra un número de proceso, se guarda en un archivo numero_proceso.txt dentro de la misma carpeta del PDF.
Si no se encuentra un número o si se ingresa manualmente, también se guarda en el mismo archivo numero_proceso.txt.


### Manejo de errores
El script está diseñado para continuar ejecutándose aunque ocurran errores en el proceso. Si un archivo PDF falla al procesar, el programa lo saltará y continuará con los demás archivos.