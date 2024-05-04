from os import listdir, path
import streamlit as st
from PIL import Image as img
from paths import *
from image import *
from ct_scanner import *

class Components:
    APPS = {"CT": "Symulacja tomografu", "DICOM": "Przeglądarka DICOM", "CreateDICOM": "Utwórz DICOM"}
    def __init__(self):
        self.stored_images_names = listdir(IMAGES_DIR)
        self.stored_dicoms_names = listdir(DICOMS_DIR)
        self.current_file = ''
        self.current_dicom_file = ''
        self.scanned = {}
        self.session = st.session_state
        self.step = 1
        self.device_count = 100
        self.device_range = 180
        self.scan_count = int(180 // self.step)
        self.up_to_angle = 180

    def sidebar(self):
        st.sidebar.title("IwM - projekt 1")
        self.current_application = st.sidebar.selectbox("Wybierz aplikację", (self.APPS["CT"], self.APPS["DICOM"], self.APPS["CreateDICOM"]))
    
    def file_uploader(self, directory):
        file = st.file_uploader(f"Wgraj plik {directory[:-2]}")
        if file is not None:
            with open(path.join(directory, file.name), "wb") as f: 
                f.write(file.getbuffer())  
                self.reload_files(directory)   
                st.success("Zapisano plik")
                
    def reload_files(self, directory):
        self.stored_images_names = listdir(directory)

    def file_selector(self, directory):
        if directory == IMAGES_DIR:
            self.current_file = st.selectbox("Wybierz zdjęcie", [''] + self.stored_images_names)
        elif directory == DICOMS_DIR:
            self.current_dicom_file = st.selectbox("Wybierz DICOM",  [''] + self.stored_dicoms_names)
            
    def settings(self):
        with st.form(key="image_set"):
            self.step = st.slider('Krok [°]', min_value=0.1, max_value=10.0, value=float(self.step), step=0.1)
            self.device_count = st.slider('Liczba urządzeń', min_value=10, max_value=360, value=self.device_count)
            self.device_range = st.slider('Rozpiętość urządzeń', min_value=10, max_value=180, value=self.device_range)
            self.up_to_angle = st.slider('Licz, aż do kąta: ', min_value=0, max_value=180, value=self.up_to_angle)
            self.scan_count = int(180 // self.step)
            submit = st.form_submit_button(label="Generuj")
        if submit:
            self.run()
    
    def image_preview(self):
        if self.current_file in self.scanned.keys():
            st.image(img.fromarray(self.scanned[self.current_file].get_image() * 255).convert('L'), width=None)
            st.image(img.fromarray(self.scanned[self.current_file].get_transposed_sinogram() * 255).convert('L'), width=None)
            st.image(img.fromarray(self.scanned[self.current_file].get_result_image() * 255).convert('L'), width=None)

    def get_current_file(self):
        return path.join(IMAGES_DIR, self.current_file)
    
    def run(self):
        image = Image(self.get_current_file())
        self.scanned[self.current_file] = CTScanner(
            image.center_with_padding,
            image.size_with_padding // 2,
            self.device_range,
            self.device_count,
            self.scan_count,
            image.get_image_with_padding(),
            self.up_to_angle
        )
        self.scanned[self.current_file].calculate_sinogram_data()
        self.scanned[self.current_file].calculate_result_data()
                
    def header(self):
        st.header("Symulacja tomografu komputerowego")
    
    def horizontal_separator(self):
        st.markdown("---")
        
    def header_ct(self):
        st.subheader("Symulator")

    def header_dicom(self):
        st.subheader("DICOM")
