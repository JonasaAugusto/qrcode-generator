import qrcode
import smtplib
import ssl
import os
import re
import json
import sys 
import csv
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog, scrolledtext, colorchooser
from email.message import EmailMessage
from PIL import ImageTk, Image

class QRCodeApp:
    def __init__(self, master):
        self.master = master
        
        # --- ESTRUTURA DE TRADUÇÃO ---
        self.translations = {
            'pt': {
                'window_title': "Gerador de QR Code",
                'customize_btn': "Personalizar Cores",
                'customize_title': "Personalização de Cores",
                'customize_label': "Defina as cores para os QR Codes:",
                'fill_color_label': "Cor do QR Code:",
                'back_color_label': "Cor de Fundo:",
                'choose_color_btn': "Escolher",
                'save_current_btn': "Salvar Cor Atual",
                'history_btn': "Histórico de Cores",
                'color_preset_exists_msg': "Esta combinação de cores já existe no histórico.",
                'history_title': "Histórico de Cores",
                'load_btn': "Carregar",
                'delete_btn': "Excluir",
                'no_color_history': "Nenhum histórico de cores salvo.",
                'qr_history_btn': "Histórico",
                'qr_history_title': "Histórico de QR Codes Gerados",
                'regenerate_btn': "Visualizar/Usar Novamente",
                'no_qr_history': "Nenhum QR Code no histórico.",
                'welcome_label': "Selecione o tipo de QR Code para gerar:",
                'link_btn': "Link (URL)",
                'text_btn': "Texto Simples",
                'phone_btn': "Telefone",
                'more_options_btn': "Mais Opções...",
                'github_credit': "by Jonas Augusto",
                'back_btn': "< Voltar",
                'more_options_title': "Mais Opções",
                'more_options_label': "Selecione uma opção adicional:",
                'options_list': ["Wi-Fi", "E-mail", "Contato (vCard)", "Localização"],
                'warning_select_type': "É necessário selecionar um tipo de QR Code.",
                'fill_data_for': "Insira os dados para o QR Code de {}",
                'text_label': "Texto (limite de aprox. 2953 caracteres):",
                'url_label': "URL Completa:",
                'wifi_ssid': "Nome da Rede (SSID):",
                'wifi_pass': "Senha da Rede (8-63 caracteres):",
                'wifi_security': "Tipo de Segurança:",
                'wifi_security_opts': ["WPA/WPA2", "WEP", "Nenhuma"],
                'vcard_name': "Nome Completo:",
                'vcard_phone': "Telefone:",
                'vcard_phone_type': "Tipo de Telefone:",
                'vcard_phone_type_opts': ["Celular", "Trabalho", "Casa"],
                'vcard_email': "E-mail (opcional):",
                'vcard_org': "Empresa (opcional):",
                'vcard_method_title': "Criação de Contato (vCard)",
                'vcard_method_label': "Escolha o método de criação:",
                'vcard_manual_btn': "Criação Manual",
                'vcard_batch_btn': "Criação Automatizada (CSV)",
                'batch_vcard_title': "Geração em Lote de vCards",
                'select_csv_btn': "Selecionar Arquivo CSV",
                'no_file_selected': "Nenhum arquivo selecionado",
                'selected_file_label': "Arquivo:",
                'select_folder_btn': "Selecionar Pasta para Salvar",
                'generate_batch_btn': "Iniciar Geração em Lote",
                'processing_csv_status': "Processando linha {} de {}...",
                'batch_success_msg': "{} QR Codes gerados com sucesso!",
                'batch_error_reading_csv': "Erro ao ler o arquivo CSV. Verifique o formato e a codificação (UTF-8).",
                'batch_no_folder_error': "É necessário selecionar uma pasta para salvar os arquivos.",
                'batch_no_file_error': "É necessário selecionar um arquivo CSV.",
                'csv_format_help_title': "Ajuda com Formato CSV",
                'csv_format_help_text': """O arquivo .csv deve ter um cabeçalho com as seguintes colunas, nesta ordem:\n\nNome,Telefone,Email,Empresa,TipoTelefone\n\n- Onde 'TipoTelefone' deve ser uma das opções: Celular, Trabalho, ou Casa.\n- Use codificação UTF-8 para garantir a compatibilidade de caracteres.""",
                'geo_gmaps_link': "Link do Google Maps:",
                'geo_use_link': "Utilizar Link do Google Maps",
                'geo_use_coords': "Inserir Coordenadas Manuais",
                'geo_lat': "Latitude:",
                'geo_lon': "Longitude:",
                'geo_help_title': "Ajuda: Coordenadas Geográficas",
                'geo_help_text': """Para obter as coordenadas no Google Maps:\n\n1. Encontre o local desejado no mapa.\n2. Clique com o botão direito do mouse sobre o ponto.\n3. O primeiro item no menu são as coordenadas (Latitude, Longitude).\n4. Clique nas coordenadas para copiá-las.""",
                'mailto_to': "E-mail do Destinatário:",
                'mailto_subject': "Assunto (opcional):",
                'tel_tel': "Número de Telefone (formato internacional, ex: +5532...):",
                'generate_btn': "Gerar e Visualizar",
                'preview_title': "Pré-visualização e Ações",
                'save_btn': "Salvar Arquivo",
                'send_email_btn': "Enviar por E-mail",
                'email_input_title': "Dados para Envio por E-mail",
                'email_dest': "E-mail do Destinatário:",
                'email_rem': "Seu E-mail (Remetente):",
                'email_pass': "Senha de App (Gmail):",
                'success_title': "Sucesso",
                'info_title': "Informação",
                'error_title': "Erro",
                'invalid_input_title': "Entrada Inválida",
                'save_success_msg': "Arquivo salvo com sucesso em:\n{}",
                'url_error': "URL inválida. O link deve iniciar com 'http://' ou 'https://'.",
                'text_error': "O campo de texto não pode estar vazio.",
                'text_limit_error': "O texto excede o limite máximo de caracteres (aprox. 2953).",
                'ssid_error': "O nome da rede (SSID) é obrigatório.",
                'wifi_pass_error': "A senha de Wi-Fi deve conter entre 8 e 63 caracteres.",
                'vcard_error': "Nome e Telefone são campos obrigatórios.",
                'vcard_email_error': "O formato do e-mail informado é inválido.",
                'mailto_error': "O formato do e-mail do destinatário é inválido.",
                'tel_error': "Número de telefone inválido. Utilize o formato internacional (ex: +5532...).",
                'gmaps_link_error': "Link inválido. Deve iniciar com 'https://www.google.com/maps/'.",
                'coords_not_found_error': "Não foi possível extrair as coordenadas do link. Verifique a URL ou insira manualmente.",
                'coords_value_error': "Latitude e Longitude devem ser valores numéricos.",
                'lat_range_error': "Valor de Latitude inválido. Deve estar entre -90 e 90.",
                'lon_range_error': "Valor de Longitude inválido. Deve estar entre -180 e 180.",
                'email_dest_invalid': "O formato do e-mail do destinatário é inválido.",
                'email_rem_invalid': "O formato do e-mail do remetente é inválido.",
                'app_pass_invalid': "Senha de App inválida. Deve conter 16 letras minúsculas, sem espaços.",
                'auth_error_title': "Erro de Autenticação",
                'auth_error_msg': "Falha na autenticação. Verifique seu e-mail e Senha de App.",
                'generic_error_title': "Erro Inesperado",
                'generic_error_msg': "Ocorreu um erro inesperado: {}",
                'email_success_msg': "E-mail enviado com sucesso para {}.",
                'sending_status': "Enviando..."
            },
            'en': {
                'window_title': "QR Code Generator",
                'customize_btn': "Customize Colors",
                'customize_title': "Color Customization",
                'customize_label': "Set the colors for the QR Codes:",
                'fill_color_label': "QR Code Color:",
                'back_color_label': "Background Color:",
                'choose_color_btn': "Choose",
                'save_current_btn': "Save Current Color",
                'history_btn': "Color History",
                'color_preset_exists_msg': "This color combination already exists in the history.",
                'history_title': "Color History",
                'load_btn': "Load",
                'delete_btn': "Delete",
                'no_color_history': "No saved color history.",
                'qr_history_btn': "History",
                'qr_history_title': "Generated QR Code History",
                'regenerate_btn': "View/Use Again",
                'no_qr_history': "No QR Codes in history.",
                'welcome_label': "Select the QR Code type to generate:",
                'link_btn': "Link (URL)",
                'text_btn': "Plain Text",
                'phone_btn': "Phone",
                'more_options_btn': "More Options...",
                'github_credit': "by Jonas Augusto",
                'back_btn': "< Back",
                'more_options_title': "More Options",
                'more_options_label': "Select an additional option:",
                'options_list': ["Wi-Fi", "E-mail", "Contact (vCard)", "Location"],
                'warning_select_type': "A QR Code type must be selected.",
                'fill_data_for': "Enter data for {} QR Code",
                'text_label': "Text (approx. 2953 character limit):",
                'url_label': "Full URL:",
                'wifi_ssid': "Network Name (SSID):",
                'wifi_pass': "Network Password (8-63 characters):",
                'wifi_security': "Security Type:",
                'wifi_security_opts': ["WPA/WPA2", "WEP", "None"],
                'vcard_name': "Full Name:",
                'vcard_phone': "Phone:",
                'vcard_phone_type': "Phone Type:",
                'vcard_phone_type_opts': ["Mobile", "Work", "Home"],
                'vcard_email': "E-mail (optional):",
                'vcard_org': "Organization (optional):",
                'vcard_method_title': "Contact (vCard) Creation",
                'vcard_method_label': "Choose the creation method:",
                'vcard_manual_btn': "Manual Creation",
                'vcard_batch_btn': "Automated Creation (CSV)",
                'batch_vcard_title': "vCard Batch Generation",
                'select_csv_btn': "Select CSV File",
                'no_file_selected': "No file selected",
                'selected_file_label': "File:",
                'select_folder_btn': "Select Folder to Save",
                'generate_batch_btn': "Start Batch Generation",
                'processing_csv_status': "Processing row {} of {}...",
                'batch_success_msg': "{} QR Codes successfully generated!",
                'batch_error_reading_csv': "Error reading CSV file. Check the format and encoding (UTF-8).",
                'batch_no_folder_error': "A folder must be selected to save the files.",
                'batch_no_file_error': "A CSV file must be selected.",
                'csv_format_help_title': "CSV Format Help",
                'csv_format_help_text': """The .csv file must have a header with the following columns, in this order:\n\nName,Phone,Email,Company,PhoneType\n\n- Where 'PhoneType' can be: Mobile, Work, or Home.\n- Use UTF-8 encoding to ensure character compatibility.""",
                'geo_gmaps_link': "Google Maps Link:",
                'geo_use_link': "Use Google Maps Link",
                'geo_use_coords': "Enter Coordinates Manually",
                'geo_lat': "Latitude:",
                'geo_lon': "Longitude:",
                'geo_help_title': "Help: Geographic Coordinates",
                'geo_help_text': """How to get coordinates from Google Maps:\n\n1. Find the desired location on the map.\n2. Right-click on the point.\n3. The first item in the menu is the coordinates (Latitude, Longitude).\n4. Click the coordinates to copy them.""",
                'mailto_to': "Recipient's E-mail:",
                'mailto_subject': "Subject (optional):",
                'tel_tel': "Phone Number (international format, e.g., +1555...):",
                'generate_btn': "Generate & View",
                'preview_title': "Preview & Actions",
                'save_btn': "Save File",
                'send_email_btn': "Send via Email",
                'email_input_title': "Email Submission Details",
                'email_dest': "Recipient's E-mail:",
                'email_rem': "Your E-mail (Sender):",
                'email_pass': "App Password (Gmail):",
                'success_title': "Success",
                'info_title': "Information",
                'error_title': "Error",
                'invalid_input_title': "Invalid Input",
                'save_success_msg': "File successfully saved to:\n{}",
                'url_error': "Invalid URL. Must start with 'http://' or 'https://'.",
                'text_error': "The text field cannot be empty.",
                'text_limit_error': "Text exceeds the maximum character limit (approx. 2953).",
                'ssid_error': "The network name (SSID) is required.",
                'wifi_pass_error': "The Wi-Fi password must contain between 8 and 63 characters.",
                'vcard_error': "Name and Phone are required fields.",
                'vcard_email_error': "The provided e-mail format is invalid.",
                'mailto_error': "The recipient's e-mail format is invalid.",
                'tel_error': "Invalid phone number. Use international format (e.g., +1555...).",
                'gmaps_link_error': "Invalid link. Must start with 'https://www.google.com/maps/'.",
                'coords_not_found_error': "Could not extract coordinates from the link. Check the URL or enter them manually.",
                'coords_value_error': "Latitude and Longitude must be numeric values.",
                'lat_range_error': "Invalid Latitude value. Must be between -90 and 90.",
                'lon_range_error': "Invalid Longitude value. Must be between -180 and 180.",
                'email_dest_invalid': "The recipient's e-mail format is invalid.",
                'email_rem_invalid': "The sender's e-mail format is invalid.",
                'app_pass_invalid': "Invalid App Password. Must be 16 lowercase letters with no spaces.",
                'auth_error_title': "Authentication Error",
                'auth_error_msg': "Authentication failed. Check your email and App Password.",
                'generic_error_title': "Unexpected Error",
                'generic_error_msg': "An unexpected error occurred: {}",
                'email_success_msg': "Email successfully sent to {}.",
                'sending_status': "Sending..."
            }
        }
        
        self.current_lang = tk.StringVar(value='pt')
        self.qr_type = tk.StringVar()
        self.qr_image_data = None
        self.geo_input_mode = tk.StringVar(value='link')
        self.qr_photo_image = None
        self.current_screen = 'show_home_screen'
        self.csv_file_path = None
        self.save_folder_path = None

        self.hyperlink_font = font.Font(family="Helvetica", size=9, underline=True)
        self.vcmd = (self.master.register(self._validate_length), '%P', '%W')
        
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            icon_path = os.path.join(self.application_path, 'icone.ico')
            self.master.iconbitmap(icon_path)
        except tk.TclError:
            print("Arquivo 'icone.ico' não encontrado. Usando ícone padrão.")

        self.settings_path = os.path.join(self.application_path, "Preset")
        os.makedirs(self.settings_path, exist_ok=True)
        self.presets_file = os.path.join(self.settings_path, "color_presets.json")
        self.qr_history_file = os.path.join(self.settings_path, "qr_history.json")
        
        self.load_settings()
        self.center_window(600, 500)
        self.show_home_screen()

    def load_settings(self):
        try:
            with open(self.presets_file, 'r') as f:
                presets = json.load(f)
                if presets:
                    self.fill_color = presets[0].get('fill_color', 'black')
                    self.back_color = presets[0].get('back_color', 'white')
                    return
        except (FileNotFoundError, json.JSONDecodeError, IndexError):
            pass
        self.fill_color = 'black'
        self.back_color = 'white'

    def save_settings(self):
        lang = self.current_lang.get()
        new_preset = {'fill_color': self.fill_color, 'back_color': self.back_color}
        
        try:
            with open(self.presets_file, 'r') as f:
                presets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            presets = []

        if new_preset in presets:
            messagebox.showinfo(self.translations[lang]['info_title'], self.translations[lang]['color_preset_exists_msg'])
            return

        presets.insert(0, new_preset)
        with open(self.presets_file, 'w') as f:
            json.dump(presets, f, indent=4)
        
        self._build_color_history_frame()

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width/2 - width / 2)
        center_y = int(screen_height/2 - height / 2)
        self.master.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def _clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def _create_github_link(self):
        lang = self.current_lang.get()
        github_link = tk.Label(self.master, text=self.translations[lang]['github_credit'], fg="blue", cursor="hand2", font=self.hyperlink_font)
        github_link.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')
        github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/JonasaAugusto"))


    def _create_back_button(self, command):
        lang = self.current_lang.get()
        back_button = ttk.Button(self.master, text=self.translations[lang]['back_btn'], command=command)
        back_button.place(x=10, rely=1.0, y=-10, anchor='sw')

    def _create_language_button(self):
        other_lang_text = "English" if self.current_lang.get() == 'pt' else "Português"
        lang_button = ttk.Button(self.master, text=other_lang_text, command=self.toggle_language)
        lang_button.place(x=10, rely=1.0, y=-10, anchor='sw')

    def toggle_language(self):
        new_lang = 'en' if self.current_lang.get() == 'pt' else 'pt'
        self.current_lang.set(new_lang)
        current_screen_method = getattr(self, self.current_screen)
        current_screen_method()

    def _validate_length(self, value_if_allowed, widget_name):
        entry = self.master.nametowidget(widget_name)
        max_len = getattr(entry, "max_length", float('inf')) 
        return len(value_if_allowed) <= max_len

    def _create_validated_entry(self, parent, text_key, limit, show=None):
        lang = self.current_lang.get()
        ttk.Label(parent, text=self.translations[lang][text_key]).pack(anchor="w")
        entry = ttk.Entry(parent, width=60, validate="key", validatecommand=self.vcmd, show=show)
        entry.max_length = limit
        entry.pack(pady=5)
        return entry

    def _get_default_filename(self):
        qr_type_raw = self.qr_type.get()
        qr_type_sanitized = re.sub(r'[^a-zA-Z0-9]', '', qr_type_raw)
        return f"QR_Code_{qr_type_sanitized}.png"
    
    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_mouse_scroll(self, widget, canvas):
        widget.bind_all("<MouseWheel>", lambda e, c=canvas: self._on_mousewheel(e, c))
        widget.bind_all("<Button-4>", lambda e, c=canvas: c.yview_scroll(-1, "units"))
        widget.bind_all("<Button-5>", lambda e, c=canvas: c.yview_scroll(1, "units"))

    def show_home_screen(self):
        self.current_screen = 'show_home_screen'
        lang = self.current_lang.get()
        self.master.title(self.translations[lang]['window_title'])
        self._clear_widgets()
        
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(expand=True, fill='both')
        
        customize_btn = ttk.Button(self.master, text=self.translations[lang]['customize_btn'], command=self.show_customization_screen)
        customize_btn.place(relx=1.0, x=-10, y=10, anchor='ne')
        
        ttk.Label(frame, text=self.translations[lang]['welcome_label'], font=("Arial", 16)).pack(pady=20)
        style = ttk.Style(); style.configure('Big.TButton', font=('Arial', 11), padding=15)
        
        ttk.Button(frame, text=self.translations[lang]['link_btn'], style='Big.TButton', command=lambda: self.on_home_button_click("Link (URL)")).pack(pady=5, fill='x')
        ttk.Button(frame, text=self.translations[lang]['text_btn'], style='Big.TButton', command=lambda: self.on_home_button_click("Texto Simples")).pack(pady=5, fill='x')
        ttk.Button(frame, text=self.translations[lang]['phone_btn'], style='Big.TButton', command=lambda: self.on_home_button_click("Telefone (tel)")).pack(pady=5, fill='x')
        
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=20)
        
        bottom_buttons_frame = ttk.Frame(frame)
        bottom_buttons_frame.pack()
        ttk.Button(bottom_buttons_frame, text=self.translations[lang]['more_options_btn'], command=self.show_more_options_popup).pack(side='left', padx=5)
        ttk.Button(bottom_buttons_frame, text=self.translations[lang]['qr_history_btn'], command=self.show_qr_history_screen).pack(side='left', padx=5)
        
        self._create_language_button()
        self._create_github_link()

    def show_customization_screen(self):
        self.current_screen = 'show_customization_screen'
        lang = self.current_lang.get()
        self._clear_widgets()
        
        self.customization_frame = ttk.Frame(self.master, padding=20)
        self.customization_frame.pack(expand=True, fill='both')
        
        self._create_back_button(self.show_home_screen)
        
        ttk.Label(self.customization_frame, text=self.translations[lang]['customize_label'], font=("Arial", 16)).pack(pady=20)
        
        fill_frame = ttk.Frame(self.customization_frame); fill_frame.pack(fill='x', pady=10)
        ttk.Label(fill_frame, text=self.translations[lang]['fill_color_label'], font=("Arial", 11)).pack(side='left', padx=5)
        self.fill_color_box = tk.Label(fill_frame, bg=self.fill_color, width=4, relief='sunken')
        self.fill_color_box.pack(side='left', padx=5)
        ttk.Button(fill_frame, text=self.translations[lang]['choose_color_btn'], command=self.choose_fill_color).pack(side='left', padx=5)

        back_frame = ttk.Frame(self.customization_frame); back_frame.pack(fill='x', pady=10)
        ttk.Label(back_frame, text=self.translations[lang]['back_color_label'], font=("Arial", 11)).pack(side='left', padx=5)
        self.back_color_box = tk.Label(back_frame, bg=self.back_color, width=4, relief='sunken')
        self.back_color_box.pack(side='left', padx=5)
        ttk.Button(back_frame, text=self.translations[lang]['choose_color_btn'], command=self.choose_back_color).pack(side='left', padx=5)

        buttons_frame = ttk.Frame(self.customization_frame); buttons_frame.pack(pady=20)
        ttk.Button(buttons_frame, text=self.translations[lang]['save_current_btn'], command=self.save_settings).pack(side='left', ipadx=10, padx=5)
        
        ttk.Separator(self.customization_frame, orient='horizontal').pack(fill='x', pady=10)
        
        self.color_history_frame = ttk.Frame(self.customization_frame)
        self.color_history_frame.pack(expand=True, fill='both')
        self._build_color_history_frame()

        self._create_github_link()

    def _build_color_history_frame(self):
        for widget in self.color_history_frame.winfo_children():
            widget.destroy()

        lang = self.current_lang.get()
        ttk.Label(self.color_history_frame, text=self.translations[lang]['history_title'], font=("Arial", 12)).pack(pady=10)

        list_container = ttk.Frame(self.color_history_frame)
        list_container.pack(expand=True)

        canvas = tk.Canvas(list_container, width=350, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self._bind_mouse_scroll(scrollable_frame, canvas)
        
        try:
            with open(self.presets_file, 'r') as f:
                presets = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            presets = []
        
        if not presets:
            ttk.Label(scrollable_frame, text=self.translations[lang]['no_color_history'], padding=10).pack()
            return

        for i, preset in enumerate(presets):
            preset_frame = ttk.Frame(scrollable_frame, padding=5)
            preset_frame.pack(fill='x')
            color_frame = ttk.Frame(preset_frame); color_frame.pack(side='left', padx=10)
            tk.Label(color_frame, bg=preset['fill_color'], width=3, relief='sunken').pack(side='left')
            tk.Label(color_frame, text="➔", font=("Arial", 12)).pack(side='left', padx=5)
            tk.Label(color_frame, bg=preset['back_color'], width=3, relief='sunken').pack(side='left')
            ttk.Button(preset_frame, text=self.translations[lang]['load_btn'], command=lambda p=preset: self._load_preset(p)).pack(side='left', padx=5)
            ttk.Button(preset_frame, text=self.translations[lang]['delete_btn'], command=lambda idx=i: self._delete_preset(idx)).pack(side='left', padx=5)

    def choose_fill_color(self):
        color_code = colorchooser.askcolor(title=self.translations[self.current_lang.get()]['choose_color_btn'])
        if color_code and color_code[1]:
            self.fill_color = color_code[1]
            self.fill_color_box.config(bg=self.fill_color)
    
    def choose_back_color(self):
        color_code = colorchooser.askcolor(title=self.translations[self.current_lang.get()]['choose_color_btn'])
        if color_code and color_code[1]:
            self.back_color = color_code[1]
            self.back_color_box.config(bg=self.back_color)
    
    def _load_preset(self, preset):
        self.fill_color = preset['fill_color']
        self.back_color = preset['back_color']
        self.fill_color_box.config(bg=self.fill_color)
        self.back_color_box.config(bg=self.back_color)

    def _delete_preset(self, index):
        try:
            with open(self.presets_file, 'r') as f:
                presets = json.load(f)
            presets.pop(index)
            with open(self.presets_file, 'w') as f:
                json.dump(presets, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError, IndexError):
            pass
        self._build_color_history_frame()

    def show_qr_history_screen(self):
        self.current_screen = 'show_qr_history_screen'
        lang = self.current_lang.get()
        self._clear_widgets()
        self._create_back_button(self.show_home_screen)

        ttk.Label(self.master, text=self.translations[lang]['qr_history_title'], font=("Arial", 16)).pack(pady=20)

        canvas = tk.Canvas(self.master, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 50))
        scrollbar.pack(side="right", fill="y")
        
        self._bind_mouse_scroll(scrollable_frame, canvas)
        
        try:
            with open(self.qr_history_file, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
        
        if not history:
            ttk.Label(scrollable_frame, text=self.translations[lang]['no_qr_history'], padding=10).pack()
        else:
            for i, item in enumerate(history):
                item_frame = ttk.Frame(scrollable_frame, padding=10, relief='solid', borderwidth=1)
                item_frame.pack(fill='x', pady=5, padx=10)
                
                content_str = str(item['data'])
                if len(content_str) > 70:
                    content_str = content_str[:70] + "..."
                
                ttk.Label(item_frame, text=f"{item['type']}:", font=("Arial", 10, "bold")).pack(anchor='w')
                ttk.Label(item_frame, text=content_str, wraplength=400).pack(anchor='w')
                
                btn_frame = ttk.Frame(item_frame)
                btn_frame.pack(fill='x', pady=5)
                ttk.Button(btn_frame, text=self.translations[lang]['regenerate_btn'], command=lambda item=item: self._regenerate_qr(item)).pack(side='left')
                ttk.Button(btn_frame, text=self.translations[lang]['delete_btn'], command=lambda idx=i: self._delete_qr_history_item(idx)).pack(side='right')
        
        self._create_github_link()

    def _add_to_qr_history(self, data_string):
        qr_type = self.qr_type.get()
        new_entry = {'type': qr_type, 'data': data_string, 'fill_color': self.fill_color, 'back_color': self.back_color}
        try:
            with open(self.qr_history_file, 'r') as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
        
        if new_entry in history:
            history.remove(new_entry)
        
        history.insert(0, new_entry)
        if len(history) > 20:
            history = history[:20]
        with open(self.qr_history_file, 'w') as f:
            json.dump(history, f, indent=4)
            
    def _delete_qr_history_item(self, index):
        try:
            with open(self.qr_history_file, 'r') as f:
                history = json.load(f)
            history.pop(index)
            with open(self.qr_history_file, 'w') as f:
                json.dump(history, f, indent=4)
        except (FileNotFoundError, json.JSONDecodeError, IndexError):
            pass
        self.show_qr_history_screen()
        
    def _regenerate_qr(self, history_item):
        self.qr_type.set(history_item['type'])
        fill_color = history_item.get('fill_color', 'black')
        back_color = history_item.get('back_color', 'white')
        self.generate_custom_qr(history_item['data'], fill_color=fill_color, back_color=back_color)
        self.show_preview_and_actions_window(history_item['data'])

    def on_home_button_click(self, qr_type_name):
        self.qr_type.set(qr_type_name)
        self.show_data_input_screen()

    def show_more_options_popup(self):
        lang = self.current_lang.get()
        popup = tk.Toplevel(self.master)
        popup.title(self.translations[lang]['more_options_title'])
        popup_width, popup_height = 300, 350
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        master_width, master_height = self.master.winfo_width(), self.master.winfo_height()
        center_x = int(master_x + master_width/2 - popup_width / 2)
        center_y = int(master_y + master_height/2 - popup_height / 2)
        popup.geometry(f'{popup_width}x{popup_height}+{center_x}+{center_y}')
        popup.resizable(False, False); popup.transient(self.master); popup.grab_set()
        frame = ttk.Frame(popup, padding="20"); frame.pack(expand=True, fill="both")
        ttk.Label(frame, text=self.translations[lang]['more_options_label'], font=("Arial", 14)).pack(pady=10)
        style = ttk.Style(); style.configure('Popup.TButton', font=('Arial', 10), padding=10)
        internal_names = ["Wi-Fi", "E-mail (mailto)", "Contato (vCard)", "Localização (geo)"]
        display_names = self.translations[lang]['options_list']
        for i in range(len(internal_names)):
            btn = ttk.Button(frame, text=display_names[i], style='Popup.TButton', command=lambda val=internal_names[i]: self._select_option_from_popup(val, popup))
            btn.pack(pady=5, fill='x')

    def _select_option_from_popup(self, qr_type_name, popup):
        if qr_type_name == "Contato (vCard)":
            popup.destroy()
            self.show_vcard_method_screen()
        else:
            popup.destroy()
            self.on_home_button_click(qr_type_name)
    
    def show_vcard_method_screen(self):
        self.current_screen = 'show_vcard_method_screen'
        lang = self.current_lang.get()
        self._clear_widgets()
        self._create_back_button(self.show_home_screen)
        
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text=self.translations[lang]['vcard_method_label'], font=("Arial", 16)).pack(pady=20)
        style = ttk.Style(); style.configure('Big.TButton', font=('Arial', 11), padding=15)
        
        ttk.Button(frame, text=self.translations[lang]['vcard_manual_btn'], style='Big.TButton', command=lambda: self.on_home_button_click("Contato (vCard)")).pack(pady=10, fill='x')
        ttk.Button(frame, text=self.translations[lang]['vcard_batch_btn'], style='Big.TButton', command=self.show_batch_vcard_screen).pack(pady=10, fill='x')

        self._create_github_link()

    def show_batch_vcard_screen(self):
        self.current_screen = 'show_batch_vcard_screen'
        lang = self.current_lang.get()
        self._clear_widgets()
        self._create_back_button(self.show_vcard_method_screen)
        
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(expand=True, fill='both')

        ttk.Label(frame, text=self.translations[lang]['batch_vcard_title'], font=("Arial", 16)).pack(pady=10)
        
        help_frame = ttk.Frame(frame)
        help_frame.pack(fill='x', pady=10)
        ttk.Label(help_frame, text=self.translations[lang]['csv_format_help_text'].split('\n\n')[0], wraplength=500).pack(anchor='w')
        ttk.Button(help_frame, text="Detalhes", command=lambda: messagebox.showinfo(self.translations[lang]['csv_format_help_title'], self.translations[lang]['csv_format_help_text'])).pack(side='left', anchor='n', pady=5)
        
        self.csv_file_path = None
        self.save_folder_path = None

        file_frame = ttk.Frame(frame)
        file_frame.pack(fill='x', pady=5)
        self.csv_label = ttk.Label(file_frame, text=self.translations[lang]['no_file_selected'])
        ttk.Button(file_frame, text=self.translations[lang]['select_csv_btn'], command=self.select_csv_file).pack(side='left', padx=10)
        self.csv_label.pack(side='left')

        folder_frame = ttk.Frame(frame)
        folder_frame.pack(fill='x', pady=5)
        self.folder_label = ttk.Label(folder_frame, text="")
        ttk.Button(folder_frame, text=self.translations[lang]['select_folder_btn'], command=self.select_save_folder).pack(side='left', padx=10)
        self.folder_label.pack(side='left')

        self.progress_bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill='x', pady=10)
        self.status_label = ttk.Label(frame, text="")
        self.status_label.pack()

        self.generate_batch_button = ttk.Button(frame, text=self.translations[lang]['generate_batch_btn'], command=self.start_batch_processing)
        self.generate_batch_button.pack(pady=20, ipadx=10)

        self._create_github_link()

    def select_csv_file(self):
        lang = self.current_lang.get()
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.csv_file_path = path
            self.csv_label.config(text=os.path.basename(path))

    def select_save_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.save_folder_path = path
            self.folder_label.config(text=path)

    def start_batch_processing(self):
        lang = self.current_lang.get()
        if not self.csv_file_path:
            messagebox.showerror(self.translations[lang]['error_title'], self.translations[lang]['batch_no_file_error'])
            return
        if not self.save_folder_path:
            messagebox.showerror(self.translations[lang]['error_title'], self.translations[lang]['batch_no_folder_error'])
            return
        
        self.generate_batch_button.config(state="disabled")
        threading.Thread(target=self._process_csv_file, daemon=True).start()

    def _process_csv_file(self):
        lang = self.current_lang.get()
        try:
            with open(self.csv_file_path, mode='r', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader) # Pula o cabeçalho
                rows = list(reader)
                total = len(rows)
                self.progress_bar['maximum'] = total
                
                for i, row in enumerate(rows):
                    self.master.after(0, lambda i=i, t=total: self.status_label.config(text=self.translations[lang]['processing_csv_status'].format(i + 1, t)))
                    self.master.after(0, lambda i=i: self.progress_bar.config(value=i + 1))
                    
                    name, phone, email, org, phone_type_str = row
                    
                    phone_type_opts = self.translations[lang]['vcard_phone_type_opts']
                    vcard_phone_type_map = {phone_type_opts[0]: "CELL", phone_type_opts[1]: "WORK", phone_type_opts[2]: "HOME"}
                    vcard_phone_type = vcard_phone_type_map.get(phone_type_str.strip(), "VOICE")
                    
                    data_string = f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nFN:{name}\nORG:{org}\nTEL;TYPE={vcard_phone_type},VOICE:{phone}\nEMAIL:{email}\nEND:VCARD"
                    
                    self.generate_custom_qr(data_string)
                    filename = f"Contato_{name.replace(' ', '_')}.png"
                    self.qr_image_data.save(os.path.join(self.save_folder_path, filename))

            self.master.after(0, lambda: messagebox.showinfo(self.translations[lang]['success_title'], self.translations[lang]['batch_success_msg'].format(total)))
            self.master.after(0, self.show_home_screen)

        except Exception as e:
            self.master.after(0, lambda e=e: messagebox.showerror(self.translations[lang]['error_title'], self.translations[lang]['batch_error_reading_csv'] + f"\n({e})"))
        finally:
            self.master.after(0, lambda: self.generate_batch_button.config(state="normal"))
            self.master.after(0, lambda: self.status_label.config(text=""))
            self.master.after(0, lambda: self.progress_bar.config(value=0))
            
    def show_data_input_screen(self):
        self.current_screen = 'show_data_input_screen'
        lang = self.current_lang.get()
        self._clear_widgets()
        content_frame = ttk.Frame(self.master, padding=20); content_frame.pack(expand=True, fill='both')
        self._create_back_button(self.show_home_screen)
        qr_type = self.qr_type.get()
        display_type = self.qr_type.get().replace("(URL)","").replace("(tel)","").replace("(vCard)","").replace("(mailto)","").replace("(geo)","")
        ttk.Label(content_frame, text=self.translations[lang]['fill_data_for'].format(display_type), font=("Arial", 14)).pack(pady=10)
        self.entries = {}
        if qr_type == "Link (URL)": self.entries['url'] = self._create_validated_entry(content_frame, 'url_label', 2000)
        elif qr_type == "Texto Simples":
            ttk.Label(content_frame, text=self.translations[lang]['text_label']).pack(anchor="w")
            self.entries['text'] = scrolledtext.ScrolledText(content_frame, width=60, height=8); self.entries['text'].pack(pady=5, expand=True, fill='both')
        elif qr_type == "Wi-Fi":
            self.entries['ssid'] = self._create_validated_entry(content_frame, "wifi_ssid", 32)
            self.entries['password'] = self._create_validated_entry(content_frame, "wifi_pass", 63, show="*")
            ttk.Label(content_frame, text=self.translations[lang]['wifi_security']).pack(anchor="w")
            self.entries['security'] = ttk.Combobox(content_frame, values=self.translations[lang]['wifi_security_opts'], state="readonly")
            self.entries['security'].pack(pady=5); self.entries['security'].set(self.translations[lang]['wifi_security_opts'][0])
        elif qr_type == "Contato (vCard)":
            self.entries['name'] = self._create_validated_entry(content_frame, "vcard_name", 100)
            self.entries['phone'] = self._create_validated_entry(content_frame, "vcard_phone", 20)
            ttk.Label(content_frame, text=self.translations[lang]['vcard_phone_type']).pack(anchor="w")
            self.entries['phone_type_var'] = tk.StringVar(value=self.translations[lang]['vcard_phone_type_opts'][0])
            phone_type_frame = ttk.Frame(content_frame); phone_type_frame.pack(fill='x', pady=2)
            for phone_type in self.translations[lang]['vcard_phone_type_opts']:
                rb = ttk.Radiobutton(phone_type_frame, text=phone_type, variable=self.entries['phone_type_var'], value=phone_type)
                rb.pack(side='left', padx=10, pady=2)
            self.entries['email'] = self._create_validated_entry(content_frame, "vcard_email", 320)
            self.entries['org'] = self._create_validated_entry(content_frame, "vcard_org", 100)
        elif qr_type == "Localização (geo)": self._build_geo_screen(content_frame)
        elif qr_type == "E-mail (mailto)":
            self.entries['to'] = self._create_validated_entry(content_frame, "mailto_to", 320)
            self.entries['subject'] = self._create_validated_entry(content_frame, "mailto_subject", 100)
        elif qr_type == "Telefone (tel)":
            self.entries['tel'] = self._create_validated_entry(content_frame, "tel_tel", 20)
        ttk.Button(content_frame, text=self.translations[lang]['generate_btn'], command=self.on_generate).pack(pady=20, ipadx=10)
        self._create_github_link()
    
    def _build_geo_screen(self, parent_frame):
        lang = self.current_lang.get()
        self.geo_link_frame = ttk.Frame(parent_frame)
        self.entries['gmaps_link'] = self._create_validated_entry(self.geo_link_frame, "geo_gmaps_link", 2000)
        self.geo_coords_frame = ttk.Frame(parent_frame)
        coords_lat_frame = ttk.Frame(self.geo_coords_frame); coords_lat_frame.pack(fill='x')
        self.entries['lat'] = self._create_validated_entry(coords_lat_frame, "geo_lat", 20)
        coords_lon_frame = ttk.Frame(self.geo_coords_frame); coords_lon_frame.pack(fill='x', pady=5)
        self.entries['lon'] = self._create_validated_entry(coords_lon_frame, "geo_lon", 20)
        help_button = ttk.Button(coords_lon_frame, text="?", width=2, command=self.show_geo_help)
        help_button.pack(side='right', anchor='w', padx=5)
        radio_frame = ttk.Frame(parent_frame); radio_frame.pack(fill='x', pady=5)
        ttk.Radiobutton(radio_frame, text=self.translations[lang]['geo_use_link'], variable=self.geo_input_mode, value='link', command=self._toggle_geo_inputs).pack(side='left', padx=10)
        ttk.Radiobutton(radio_frame, text=self.translations[lang]['geo_use_coords'], variable=self.geo_input_mode, value='coords', command=self._toggle_geo_inputs).pack(side='left', padx=10)
        self._toggle_geo_inputs()

    def _toggle_geo_inputs(self):
        if self.geo_input_mode.get() == 'link':
            self.geo_coords_frame.pack_forget(); self.geo_link_frame.pack(fill='x')
        else:
            self.geo_link_frame.pack_forget(); self.geo_coords_frame.pack(fill='x')
    
    def show_geo_help(self):
        lang = self.current_lang.get()
        messagebox.showinfo(self.translations[lang]['geo_help_title'], self.translations[lang]['geo_help_text'])

    def on_generate(self):
        lang = self.current_lang.get()
        try:
            data_string = self._validate_and_get_data()
            if data_string is None: return
            self._add_to_qr_history(data_string)
            self.generate_custom_qr(data_string)
            self.show_preview_and_actions_window(data_string)
        except Exception as e:
            messagebox.showerror(self.translations[lang]['generic_error_title'], self.translations[lang]['generic_error_msg'].format(e))

    def generate_custom_qr(self, data, fill_color=None, back_color=None):
        fill = fill_color if fill_color is not None else self.fill_color
        back = back_color if back_color is not None else self.back_color
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10, border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill, back_color=back).convert('RGBA')
        self.qr_image_data = img

    def show_preview_and_actions_window(self, data_string):
        lang = self.current_lang.get()
        if not self.qr_image_data: return
        preview_window = tk.Toplevel(self.master)
        preview_window.title(self.translations[lang]['preview_title'])
        preview_width, preview_height = 340, 420
        master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
        master_width, master_height = self.master.winfo_width(), self.master.winfo_height()
        center_x = int(master_x + master_width/2 - preview_width / 2)
        center_y = int(master_y + master_height/2 - preview_height / 2)
        preview_window.geometry(f'{preview_width}x{preview_height}+{center_x}+{center_y}')
        preview_window.resizable(False, False); preview_window.transient(self.master); preview_window.grab_set()
        display_size = 300
        img_resized = self.qr_image_data.resize((display_size, display_size), Image.NEAREST)
        self.qr_photo_image = ImageTk.PhotoImage(img_resized)
        tk.Label(preview_window, image=self.qr_photo_image).pack(pady=20, padx=20)
        actions_frame = ttk.Frame(preview_window); actions_frame.pack(pady=(0, 20), padx=20, fill='x')
        ttk.Button(actions_frame, text=self.translations[lang]['save_btn'], command=lambda: self._save_from_preview(preview_window)).pack(side='left', expand=True, padx=5)
        ttk.Button(actions_frame, text=self.translations[lang]['send_email_btn'], command=lambda: self._email_from_preview(preview_window)).pack(side='left', expand=True, padx=5)
        
    def _save_from_preview(self, preview_window):
        lang = self.current_lang.get()
        default_name = self._get_default_filename()
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], initialfile=default_name, parent=preview_window)
        if filename:
            try:
                self.qr_image_data.save(filename)
                messagebox.showinfo(self.translations[lang]['success_title'], self.translations[lang]['save_success_msg'].format(filename))
                preview_window.destroy()
                self.show_home_screen()
            except Exception as e:
                messagebox.showerror(self.translations[lang]['error_title'], self.translations[lang]['save_error_msg'].format(e), parent=preview_window)

    def _email_from_preview(self, preview_window):
        preview_window.destroy()
        self.show_email_input_screen()
        
    def _validate_and_get_data(self):
        lang = self.current_lang.get()
        qr_type = self.qr_type.get()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        def error(msg_key, format_value=None): 
            msg = self.translations[lang][msg_key]
            if format_value: msg = msg.format(format_value)
            messagebox.showerror(self.translations[lang]['invalid_input_title'], msg); return None
        if qr_type == "Link (URL)":
            url = self.entries['url'].get().strip()
            if not url.startswith(('http://', 'https://')): return error('url_error')
            return url
        if qr_type == "Texto Simples":
            text = self.entries['text'].get("1.0", tk.END).strip()
            if not text: return error('text_error')
            byte_len = len(text.encode('utf-8'))
            if byte_len > 2953: return error('text_limit_error')
            return text
        if qr_type == "Wi-Fi":
            ssid, password, security = self.entries['ssid'].get().strip(), self.entries['password'].get(), self.entries['security'].get()
            security_opts = self.translations[lang]['wifi_security_opts']
            if not ssid: return error('ssid_error')
            if security != security_opts[2] and not (8 <= len(password) <= 63): return error('wifi_pass_error')
            internal_security = 'nopass' if security == security_opts[2] else security
            return f"WIFI:S:{ssid};T:{internal_security};P:{password};;"
        if qr_type == "Contato (vCard)":
            name, phone, phone_type_str = self.entries['name'].get().strip(), self.entries['phone'].get().strip(), self.entries['phone_type_var'].get()
            email, org = self.entries['email'].get().strip(), self.entries['org'].get().strip()
            if not name or not phone: return error('vcard_error')
            if email and not re.match(email_regex, email): return error('vcard_email_error')
            phone_type_opts = self.translations[lang]['vcard_phone_type_opts']
            vcard_phone_type_map = {phone_type_opts[0]: "CELL", phone_type_opts[1]: "WORK", phone_type_opts[2]: "HOME"}
            vcard_phone_type = vcard_phone_type_map.get(phone_type_str, "VOICE")
            return f"BEGIN:VCARD\nVERSION:3.0\nN:{name}\nFN:{name}\nORG:{org}\nTEL;TYPE={vcard_phone_type},VOICE:{phone}\nEMAIL:{email}\nEND:VCARD"
        if qr_type == "E-mail (mailto)":
            to, subject = self.entries['to'].get().strip(), self.entries['subject'].get().strip()
            if not re.match(email_regex, to): return error('mailto_error')
            return f"mailto:{to}?subject={subject}"
        if qr_type == "Telefone (tel)":
            tel = self.entries['tel'].get().strip()
            if not tel.startswith('+') or not all(c.isdigit() for c in tel[1:]): return error('tel_error')
            return f"tel:{tel}"
        if qr_type == "Localização (geo)":
            if self.geo_input_mode.get() == 'link':
                link = self.entries['gmaps_link'].get().strip()
                if not link.startswith("https://www.google.com/maps/"): return error('gmaps_link_error')
                match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", link)
                if not match: return error('coords_not_found_error')
                lat, lon = match.groups()
                return f"geo:{lat},{lon}"
            else:
                try:
                    lat, lon = float(self.entries['lat'].get().strip().replace(',', '.')), float(self.entries['lon'].get().strip().replace(',', '.'))
                    if not (-90 <= lat <= 90): return error('lat_range_error')
                    if not (-180 <= lon <= 180): return error('lon_range_error')
                    return f"geo:{lat},{lon}"
                except ValueError: return error('coords_value_error')
        return ""

    def show_email_input_screen(self):
        self.current_screen = 'show_email_input_screen'
        lang = self.current_lang.get()
        self._clear_widgets()
        content_frame = ttk.Frame(self.master, padding=20); content_frame.pack(expand=True, fill='both')
        self._create_back_button(self.show_data_input_screen)
        ttk.Label(content_frame, text=self.translations[lang]['email_input_title'], font=("Arial", 14)).pack(pady=10)
        self.email_entries = {}
        self.email_entries['dest'] = self._create_validated_entry(content_frame, "email_dest", 320)
        self.email_entries['rem'] = self._create_validated_entry(content_frame, "email_rem", 320)
        self.email_entries['pass'] = self._create_validated_entry(content_frame, "email_pass", 16, show="*")
        self.send_button = ttk.Button(content_frame, text=self.translations[lang]['send_email_btn'], command=self.on_send_email)
        self.send_button.pack(pady=20)
        self.status_label = ttk.Label(content_frame, text=""); self.status_label.pack()
        self._create_github_link()
        
    def on_send_email(self):
        lang = self.current_lang.get()
        dest, rem, senha = self.email_entries['dest'].get().strip(), self.email_entries['rem'].get().strip(), self.email_entries['pass'].get()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, dest): messagebox.showerror(self.translations[lang]['invalid_input_title'], self.translations[lang]['email_dest_invalid']); return
        if not re.match(email_regex, rem): messagebox.showerror(self.translations[lang]['invalid_input_title'], self.translations[lang]['email_rem_invalid']); return
        if not re.match(r'^[a-z]{16}$', senha): messagebox.showerror(self.translations[lang]['invalid_input_title'], self.translations[lang]['app_pass_invalid']); return
        self.send_button.config(state="disabled"); self.status_label.config(text=self.translations[lang]['sending_status'])
        threading.Thread(target=self._send_email_thread, args=(dest, rem, senha)).start()

    def _send_email_thread(self, email_dest, email_rem, senha_rem):
        lang = self.current_lang.get()
        nome_arquivo_qrcode = "qrcode_temp.png"
        self.qr_image_data.save(nome_arquivo_qrcode)
        try:
            msg = EmailMessage(); msg['Subject'] = f"Seu QR Code do tipo: {self.qr_type.get()}"; msg['From'] = email_rem; msg['To'] = email_dest
            msg.set_content(f"Olá!\n\nSegue em anexo o QR Code solicitado.\n\nAtenciosamente,\nGerador de QR Code")
            with open(nome_arquivo_qrcode, 'rb') as f:
                dados_imagem = f.read()
                attachment_filename = self._get_default_filename()
                msg.add_attachment(dados_imagem, maintype='image', subtype='png', filename=attachment_filename)
            contexto_ssl = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto_ssl) as server:
                server.login(email_rem, senha_rem)
                server.send_message(msg)
            messagebox.showinfo(self.translations[lang]['success_title'], self.translations[lang]['email_success_msg'].format(email_dest))
            self.master.after(0, self.show_home_screen)
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror(self.translations[lang]['auth_error_title'], self.translations[lang]['auth_error_msg'])
        except Exception as e:
            messagebox.showerror(self.translations[lang]['generic_error_title'], self.translations[lang]['generic_error_msg'].format(e))
        finally:
            if os.path.exists(nome_arquivo_qrcode): os.remove(nome_arquivo_qrcode)
            self.master.after(0, lambda: self.send_button.config(state="normal"))
            self.master.after(0, lambda: self.status_label.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()

