import streamlit as st
from os import path
import numpy as np
from dicom_io import DicomIO
from ct_scanner import CTScanner
from paths import DICOMS_DIR, IMAGES_DIR
from image import Image
from algorithms import *
from components import Components

st.set_page_config(page_title="Symulacja Skanera CT")
components = Components()
components.sidebar()

if components.current_application == components.APPS["CT"]:
    components.header_ct()
    components.horizontal_separator()
    
    column_selector, column_uploader = st.columns([1, 2])

    with column_selector:
        components.file_selector(IMAGES_DIR)
        
    with column_uploader:
        components.file_uploader(IMAGES_DIR)
        
    components.settings()
    components.image_preview()

elif components.current_application == components.APPS["DICOM"]:
    components.header_dicom()
    components.horizontal_separator()

    column_selector, column_uploader = st.columns([1, 2])

    with column_selector:
        components.file_selector(DICOMS_DIR)
        
    with column_uploader:
        components.file_uploader(DICOMS_DIR)

    if st.button('Wczytaj'):
        dcm = DicomIO()
        new_patient_data = {}
        if components.current_dicom_file in components.stored_dicoms_names:
            dcm.read(path.join(DICOMS_DIR, components.current_dicom_file))
            st.image(dcm.patient_data.pixel_array)
            patient_data = dcm.get_patient_data()
            new_patient_data["PatientName"] = st.text_input("Imie i nazwisko: ", value=str(patient_data.PatientName))
            new_patient_data["PatientID"] = st.text_input("ID pacjenta: ", value=str(patient_data.PatientID))
            new_patient_data["ImageComments"] = st.text_input("Komentarz do obrazu: ", value=str(patient_data.ImageComments))

elif components.current_application == components.APPS["CreateDICOM"]:  
    new_img = None
    dcm = DicomIO()
    new_patient_data = {}
    with st.form(key="formCreate"):
        dcm.filename = path.join(DICOMS_DIR, st.text_input("Nazwa pliku", value="newDICOM") + ".dcm")
        uploaded_file = st.file_uploader("Wgraj obraz", type=["jpg"])
        if uploaded_file:
            with open(path.join(IMAGES_DIR, uploaded_file.name), "wb") as f: 
                f.write(uploaded_file.getbuffer())
            new_img = Image(path.join(IMAGES_DIR, uploaded_file.name))
            new_img = np.asarray(new_img.get_image())
        new_patient_data["PatientName"] = st.text_input("Imie i nazwisko: ", value='')
        new_patient_data["PatientID"] = st.text_input("ID pacjenta: ", value='')
        new_patient_data["ImageComments"] = st.text_input("Komentarz do obrazu: ", value='')
        if st.form_submit_button(label="Utwórz plik"):
            dcm.write(new_patient_data, new_img)
            st.success("Plik utworzony pomyślnie!")