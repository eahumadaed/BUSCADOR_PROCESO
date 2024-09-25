import os
from pdf2image import convert_from_path # type: ignore
from paddleocr import PaddleOCR # type: ignore
from PIL import Image
from datetime import datetime
import re
import cv2 # type: ignore
import numpy as np
import easyocr # type: ignore
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

paddle_ocr = PaddleOCR(use_angle_cls=True, lang='es')
easy_ocr = easyocr.Reader(['es'])

def log_message(message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def convert_pdf_to_jpg(pdf_path):
    try:
        log_message(f"Convirtiendo la primera página de {pdf_path} a imagen JPG.")
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        if images:
            output_dir = os.path.dirname(pdf_path)
            jpg_path = os.path.join(output_dir, "pagina_1.jpg")
            images[0].save(jpg_path, 'JPEG')
            log_message(f"Imagen guardada en {jpg_path}")
            return jpg_path
        else:
            log_message("No se pudo convertir la primera página del PDF.")
            return None
    except Exception as e:
        log_message(f"Error al convertir el PDF a imagen JPG: {e}")
        return None

def extract_number_with_paddleocr(image_path):
    try:
        log_message(f"Extrayendo números escritos a mano de la imagen {image_path} usando PaddleOCR.")
        image = cv2.imread(image_path)
        result = paddle_ocr.ocr(image, cls=True)
        numero_pattern = re.compile(r'\b(16|17|18)\d{3,7}\b')
        for line in result:
            for element in line:
                text = element[1][0]
                match = numero_pattern.search(text)
                if match:
                    numero_proceso = match.group(0)
                    log_message(f"Número de proceso detectado con PaddleOCR: {numero_proceso}")
                    return numero_proceso
        log_message("PaddleOCR no encontró ningún número de proceso válido.")
        return None
    except Exception as e:
        log_message(f"Error al extraer números con PaddleOCR: {e}")
        return None

def extract_number_with_easyocr(image_path):
    try:
        log_message(f"Extrayendo números escritos a mano de la imagen {image_path} usando EasyOCR.")
        image = cv2.imread(image_path)
        result = easy_ocr.readtext(image)
        numero_pattern = re.compile(r'\b(16|17|18)\d{3,7}\b')
        for line in result:
            text = line[1]
            match = numero_pattern.search(text)
            if match:
                numero_proceso = match.group(0)
                log_message(f"Número de proceso detectado con EasyOCR: {numero_proceso}")
                return numero_proceso
        log_message("EasyOCR no encontró ningún número de proceso válido.")
        return None
    except Exception as e:
        log_message(f"Error al extraer números con EasyOCR: {e}")
        return None

def manual_input_gui(image_path, pdf_path):
    try:
        log_message(f"Mostrando GUI para ingresar número de proceso manualmente para {image_path}")
        root = tk.Tk()
        root.title("Validar Número de Proceso")
        img = Image.open(image_path)
        img = img.resize((500, 700), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=img)
        img_label.grid(row=0, column=0, columnspan=2)
        entry_label = tk.Label(root, text="Ingrese el número de proceso:")
        entry_label.grid(row=1, column=0, padx=10, pady=10)
        entry_field = tk.Entry(root, width=30)
        entry_field.grid(row=1, column=1, padx=10, pady=10)

        def guardar_numero():
            numero_proceso = entry_field.get().strip()
            if not numero_proceso:
                numero_proceso = "N/A"
            output_dir = os.path.dirname(pdf_path)
            numero_proceso_txt_path = os.path.join(output_dir, "numero_proceso.txt")
            with open(numero_proceso_txt_path, 'a') as f:
                f.write(f"{numero_proceso}\n")
            log_message(f"Número de proceso guardado: {numero_proceso}")
            root.destroy()

        save_button = tk.Button(root, text="Guardar", command=guardar_numero)
        save_button.grid(row=2, column=0, padx=10, pady=10)

        def guardar_sin_numero():
            entry_field.delete(0, tk.END)
            entry_field.insert(0, "N/A")
            guardar_numero()

        na_button = tk.Button(root, text="Sin Número", command=guardar_sin_numero)
        na_button.grid(row=2, column=1, padx=10, pady=10)

        root.mainloop()
    except Exception as e:
        log_message(f"Error en la GUI para entrada manual: {e}")

def process_sol_pdf(pdf_path):
    try:
        output_dir = os.path.dirname(pdf_path)
        numero_proceso_txt_path = os.path.join(output_dir, "numero_proceso.txt")
        if os.path.exists(numero_proceso_txt_path):
            log_message(f"{numero_proceso_txt_path} ya existe, omitiendo este PDF.")
            return
        if 'ñ' in pdf_path.lower():
            return
        if re.search(r'[áéíóúÁÉÍÓÚñÑ]', pdf_path):
            return
        log_message(f"Procesando {pdf_path}")
        jpg_path = convert_pdf_to_jpg(pdf_path)
        if jpg_path:
            numero_proceso = extract_number_with_paddleocr(jpg_path)
            if not numero_proceso:
                numero_proceso = extract_number_with_easyocr(jpg_path)
            if not numero_proceso:
                return
                log_message("Ningún OCR detectó el número de proceso, mostrando GUI manual.")
                manual_input_gui(jpg_path, pdf_path)
            else:
                with open(numero_proceso_txt_path, 'a') as f:
                    f.write(f"{numero_proceso}\n")
                log_message(f"Número de proceso {numero_proceso} guardado en {numero_proceso_txt_path}")
        else:
            log_message("Error al convertir el PDF a imagen.")
    except Exception as e:
        log_message(f"Error procesando el PDF {pdf_path}: {e}")

def process_pdfs_in_directory(directory):
    try:
        log_message(f"Iniciando procesamiento de PDFs en el directorio {directory}.")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower() == 'sol.pdf':
                    pdf_path = os.path.join(root, file)
                    process_sol_pdf(pdf_path)
    except Exception as e:
        log_message(f"Error al procesar el directorio {directory}: {e}")

if __name__ == "__main__":
    directorio = "SOLICITUD"
    log_message("Comenzando el procesamiento de directorio.")
    process_pdfs_in_directory(directorio)
    log_message("Procesamiento de directorio finalizado.")
