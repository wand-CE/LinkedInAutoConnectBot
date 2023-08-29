import threading
import re
from mvc.model import ConfigManager, Check_data, TranslationModel, LinkedInBot
from tkinter.messagebox import showinfo


class BotController:
    def __init__(self, view):
        self.view = view
        self.config = ConfigManager.load_config()
        self.state = True
        self.loggin_out = ""

    def check_elements(self, email, password, search, note, num_of_connections):
        if not Check_data.validate_email(email):
            showinfo(message="Email inválido")
            return ''

        if not Check_data.validate_password(password):
            showinfo(message="Senha inválida")
            return ''

        if not Check_data.search_bar(search):
            showinfo(message="Barra vazia")
            return ''

        length = Check_data.length_note(note)
        if length not in [True, False] and isinstance(length, int):
            showinfo(message=f"Nota muito grande.{length}/250")
            return ''
        elif not length:
            showinfo(message="Nota vazia")
            return ''
        process = threading.Thread(target=self.init_bot,args=(email.strip(), password, search, note.strip(), num_of_connections))
        process.start()

    def init_bot(self, email, password, search, note, num_of_connections):
        self.widgets_state()
        session = LinkedInBot(num_of_connections)
        self.loggin_out = lambda: [self.widgets_state(), session.logout()]
        session.start_bot()
        session.login(email, password)
        session.search(search)
        session.connect(note)
        session.logout()

    def change_language(self, language, elements):
        self.config['language'] = language
        ConfigManager.save_config(self.config)
        TranslationModel.set_translation(language, elements)

    def change_theme(self, theme):
        self.config['theme'] = theme
        ConfigManager.save_config(self.config)

    def widgets_state(self):
        children = [child.winfo_children() for child in self.view.winfo_children()]
        buttons = []
        states = []
        for child in children[0]:            
            if 'label' not in str(child):
                if re.search(r'(?=entry|textbox)', str(child)):
                    child.configure(state="disabled" if self.state else 'normal')
                elif 'optionmenu' in str(child):
                    if '5' in child.cget('values'):
                        child.configure(state="disabled" if self.state else 'normal')
                elif 'button' in str(child):
                    buttons.append(child)
                    states.append(child.cget('state'))
        states = states[::-1]
        lista = [button.configure(state=states[i]) for i, button in enumerate(buttons)]
        del lista

        self.state = not self.state
