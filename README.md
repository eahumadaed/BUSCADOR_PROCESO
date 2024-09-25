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
