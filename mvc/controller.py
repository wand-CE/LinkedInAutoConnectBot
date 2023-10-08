import threading
from mvc.model import ConfigManager, Check_data, TranslationModel, LinkedInBot
from tkinter.messagebox import showinfo
from customtkinter import CTkImage
from PIL import Image


class BotController:
    def __init__(self):
        self.bot = None
        self.config = ConfigManager.load_config()
        self.eye_icon = "images/eye.png"
        self.loggin_out = ""
        self.password_visible = False

    def check_elements(self, email, password, search, note, num_of_connections, view):
        if not Check_data.validate_email(email):
            showinfo(message="Email inválido")
            return False

        if not Check_data.validate_password(password):
            showinfo(message="Senha inválida")
            return False

        if not Check_data.search_bar(search):
            showinfo(message="Barra vazia")
            return False

        length = Check_data.length_note(note)
        if length not in [True, False] and isinstance(length, int):
            showinfo(message=f"Nota muito grande.{length}/250")
            return False

        if not length:
            showinfo(message="Nota vazia")
            return False

        process = threading.Thread(target=self.init_bot, args=(
            email.strip(), password, search, note.strip(), num_of_connections, view))
        process.daemon = True
        process.start()
        return True

    def init_bot(self, email, password, search, note, num_of_connections, view):
        session = LinkedInBot(num_of_connections, self.config['language'])
        session.add_observer(view)
        self.loggin_out = lambda: [session.logout()]
        try:
            session.start_bot()
            session.login(email, password)
            session.search(search)
            session.connect(note)
            session.logout()
        except:
            pass

    def change_language(self, language, elements):
        self.config['language'] = language
        ConfigManager.save_config(self.config)
        TranslationModel.set_translation(language, elements)

    def change_theme(self, theme):
        self.config['theme'] = theme
        ConfigManager.save_config(self.config)

    def show_password(self, widget_password, eye_password):
        self.eye_icon = "images/eye.png" if self.eye_icon == "images/eye-slash.png" else "images/eye-slash.png"
        eye = CTkImage(Image.open(self.eye_icon),
                       size=(20, 20))

        self.password_visible = not self.password_visible
        widget_password.configure(show='' if self.password_visible else '*')
        eye_password.configure(image=eye)
