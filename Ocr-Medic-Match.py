from IPython.display import display
import ipywidgets as widgets
from google.colab.patches import cv2_imshow
import pandas as pd
import re
import cv2
import easyocr as ocr
import numpy as np
import pytesseract
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
uploader = widgets.FileUpload()
display(uploader)
drugs_data = {
    'ilac_isimleri': ['IESPOR VIM DRY', 'MULTISEF VIM DRY', 'AUGMENTIN FILM TAB BID', 'Klamoks FILM TAB BID',
                     'AUGMENTIN SUSP DRY ES', 'IECILLINE AIM SOLV80 M', 'CIPRO FILMTAB', 'SEFAZOL V.IM DRY',
                     'CEFAMEZIN VIM DRY', 'IESPOR VIM DRY', 'MULTISEF VIM DRY', 'Klamoks FILM TAB BID',
                     'NOVOSEF VIM', 'EFAKS VIM DRY', 'AMOKLAVIN FILM TAB BID', 'AKSEF VIM', 'CROXILEX FILM TAB BID',
                     'IESEF VIM DRY', 'CEZOL VIM DRY', 'AUGMENTIN SUSP DRY ES 600 MG 1 100 ML'],
    'etkin_madde': ['Sefazolin', 'Sefuroksim', 'Amoksisilin + Klavulanik Asit', 'Amoksisilin trihidrat',
                    'Amoksisilin trihidrat', 'Penisilin G potasyum', 'Siprofloksasin hidroklorür',
                    'Sefazolin', 'Sefazolin', 'Sefazolin', 'Sefuroksim', 'Amoksisilin trihidrat',
                    'Seftriakson', 'Sefuroksim', 'Amoksisilin', 'Sefuroksim + Lidokain HCl',
                    'Amoksisilin trihidrat', 'Seftriakson', 'Sefazolin',
                    'Amoksisilin + Potasyum klavulanat'],
    'etkilesim_icinde_olanlar': ['BCG Intravezikal Kolera Asisi', 'BCG Intravezikal Kolera Asisi',
                                 'BCG Intravezikal Kolera Asisi', 'BCG Intravezikal Kolera Asisi', 'BCG Intravezikal Kolera Asisi',
                                 'BCG Intravezikal Kolera Asisi', 'Agomelatin',
                                 'BCG Intravezikal Kolera Asisi','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin','Agomelatin']
               }
drugs_data = pd.DataFrame(drugs_data)
# Taranan görüntüdeki ilaç ismini al
ocr_text = pytesseract.image_to_string(img)

def process_image(change):
    img = cv2.imdecode(np.frombuffer(uploader.data[0], np.uint8), cv2.IMREAD_UNCHANGED)
    ocr_text = pytesseract.image_to_string(img)
    drug_names = [drug for drug in drugs_data['ilac_isimleri']]
    matches = process.extractOne(ocr_text, drug_names)
    if matches[1]>80:
        match_index = drug_names.index(matches[0])
        display(widgets.HTML(f"<b>Etkin Madde:</b> {drugs_data.at[match_index, 'etkin_madde']}"))
        display(widgets.HTML(f"<b>Etkileşim İçinde Olanlar:</b> {drugs_data.at[match_index, 'etkilesim_icinde_olanlar']}"))
    else:
        display(widgets.HTML("<b>Eşleşen ilaç bulunamadı.</b>"))

uploader.observe(process_image, names='data')