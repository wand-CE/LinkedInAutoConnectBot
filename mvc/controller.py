import threading
from tkinter.messagebox import showinfo
from customtkinter import CTkImage
from PIL import Image
from mvc.model import ConfigManager, Check_data, TranslationModel, LinkedInBot, resource_path


eye_img = resource_path("images\\eye.png")
eye_slash = resource_path("images\\eye_slash.png")
icon = resource_path("images\\meu_icon.ico")


class BotController:

    should_stop = ""

    def __init__(self):
        self.bot = None
        self.images = [eye_img, eye_slash]
        self.config = ConfigManager.load_config()
        self.app_icon = icon
        self.eye_icon = self.images[0]
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
        self.should_stop = lambda: setattr(session, 'should_stop', True)
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
        self.eye_icon = self.images[0] if self.eye_icon == self.images[1] else self.images[1]
        eye = CTkImage(Image.open(self.eye_icon),
                       size=(20, 20))

        self.password_visible = not self.password_visible
        widget_password.configure(show='' if self.password_visible else '*')
        eye_password.configure(image=eye)

    def stop(self):
        self.should_stop()
        return True
