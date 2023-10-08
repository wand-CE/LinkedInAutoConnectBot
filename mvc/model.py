import time
import json
import os
from re import match
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


messages_to_show = {
    "en-US": {
        "starting_bot": "Starting session...\n",
        "login": "Trying to login on account...\n",
        "logged": "Logged on account!\n",
        "search": "Searching",
        "connection": "Send invite to ",
        "num_connect": ["out of", "invites made"],
        "logout": "Session ended.\n",
    },
    "pt-BR": {
        "starting_bot": "Iniciando sessão...\n",
        "login": "Tentando se conectar a conta\n",
        "logged": "Logado na conta!\n",
        "search": "Pesquisando",
        "connection": "Enviado convite para ",
        "num_connect": ["de", "convites enviados\n"],
        "logout": "Sessão encerrada.\n",
    }
}


class ConfigManager:
    DEFAULT_CONFIG = {
        'theme': 'light',
        'language': 'en-US'
    }

    CONFIG_PATH = "config.json"

    @classmethod
    def load_config(cls):
        if os.path.exists(cls.CONFIG_PATH):
            with open(cls.CONFIG_PATH, 'r') as file:
                config = json.load(file)
                return config
        return cls.DEFAULT_CONFIG

    @classmethod
    def save_config(cls, config):
        with open(cls.CONFIG_PATH, 'w') as file:
            json.dump(config, file, indent=4, sort_keys=True)


class TranslationModel:
    translations = {
        'en-US': {
            'theme': "Dark Mode",
            'email': "E-mail: ",
            'password': "Password: ",
            'email_place_holder': "Your E-mail",
            'password_place_holder': "Your Password",
            'profession': "Profession to Search:",
            'custom message': "Custom Message to send:",
            'num_connections': "Number of Connections:",
            'start_btn': 'START',
            # disabled for now 'stop_btn' : 'STOP',
        },
        'pt-BR': {
            'theme': "Modo Escuro",
            'email': "E-mail:",
            'password': "Senha:",
            'email_place_holder': "Seu E-mail",
            'password_place_holder': "Sua Senha",
            'profession': "Profissão para pesquisar:",
            'custom message': "Mensagem customizada:",
            'num_connections': "Numero de conexões:",
            'start_btn': 'INICIAR',
            # disabled for now 'stop_btn' : 'PARAR',
        },
    }

    @classmethod
    def set_translation(cls, language, elements):
        dict_lang = cls.translations.get(language, {})
        if dict_lang:
            i = 0
            for element in dict_lang:
                if 'place_holder' in element:
                    elements[i].configure(placeholder_text=dict_lang[element])
                else:
                    elements[i].configure(text=dict_lang[element])
                i += 1


class Check_data:
    @classmethod
    def validate_email(cls, email):
        if len(email.strip()) > 0:
            return match(r"^\w+@\w+\.\w+$", email)

    @classmethod
    def validate_password(cls, password):
        return bool(len(password))

    @classmethod
    def search_bar(cls, search):
        return bool(len(search.strip()))

    @classmethod
    def length_note(cls, nota):
        length = len(nota.strip())
        if length > 250:
            return int(length)
        return bool(length <= 250 and length > 0)


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update_message(message)

    def disable_stop_button(self):
        for observer in self._observers:
            observer.disable_stop_button()


class LinkedInBot(Observable):
    def __init__(self, num_of_connections, language):
        super().__init__()
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)

        self.driver.maximize_window()
        screen_width = self.driver.get_window_rect().get("width")
        screen_height = self.driver.get_window_rect().get("height")
        window_width = 800
        position_x = screen_width - window_width
        self.driver.set_window_size(window_width, screen_height)
        self.driver.set_window_position(position_x, 0)

        self.actual_page = 1
        self.num_of_connections = int(num_of_connections)
        self.counter = 0
        # self.message = ""
        self.language = language

    def add_message(self, new_message):
        # self.message += new_message
        self.notify_observers(new_message)

    def start_bot(self):
        self.add_message(messages_to_show[self.language]["starting_bot"])
        self.driver.get("https://br.linkedin.com/")

    def login(self, email, password):
        try:
            self.add_message(messages_to_show[self.language]["login"])
            user = self.driver.find_element(By.ID, "session_key")
            password_element = self.driver.find_element(
                By.ID, "session_password")
            button = self.driver.find_element(
                By.CSS_SELECTOR, '[data-id="sign-in-form__submit-btn"]')
            time.sleep(2)
        except NoSuchElementException:
            self.start_bot()
            return self.login(email, password)

        user.send_keys(email)
        password_element.send_keys(password)
        time.sleep(2)
        button.click()

    def search(self, search_term):
        search = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-global-typeahead")))
        search.click()
        search = search.find_element(
            By.CLASS_NAME, "search-global-typeahead__input")

        search.send_keys(search_term)

        self.add_message(messages_to_show[self.language]["logged"])
        self.add_message(
            f'{messages_to_show[self.language]["search"]} {search_term}\n')
        search.send_keys(Keys.ENTER)

        people_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button')))
        people_tab.click()

    def connect(self, custom_message):
        while self.num_of_connections > self.counter:
            self.scroll_page(duration=6)
            time.sleep(5)
            people = self.driver.find_elements(
                By.XPATH, "//li[@class='reusable-search__result-container']//*[text()='Conectar']/parent::*")
            for person in people:
                try:
                    time.sleep(5)
                    text_span = person.find_element(
                        By.XPATH, ".//span[@class='artdeco-button__text']")
                    if "Conectar" in text_span.text:
                        name = person.find_element(
                            By.XPATH, "./../../..//span[@dir='ltr']//span[@aria-hidden='true']")

                        name = name.text.split()
                        name = name[0]

                        conect_button = person
                        conect_button.click()

                        time.sleep(5)
                        self.select_note(custom_message, name)

                        send = self.driver.find_element(
                            By.XPATH, "//button[@aria-label='Enviar agora']")
                        send.click()
                        self.add_message(
                            messages_to_show[self.language]["connection"] + name + "\n")
                        self.counter += 1

                        self.add_message(
                            f"{str(self.counter)} {messages_to_show[self.language]['num_connect'][0]} {self.num_of_connections} {messages_to_show[self.language]['num_connect'][1]}\n")
                        time.sleep(5)
                except:
                    pass
                if self.num_of_connections == self.counter:
                    break
                if person == people[-1]:
                    self.actual_page += 1
                    time.sleep(5)
                    pages = self.driver.find_elements(
                        By.CLASS_NAME, 'artdeco-pagination__indicator--number')
                    for page in pages:
                        if str(self.actual_page) in page.text:
                            page.click()
                            break
                    time.sleep(5)

    def select_note(self, custom_message, name):
        time.sleep(1)
        note = self.driver.find_element(
            By.XPATH, "//button[@aria-label='Adicionar nota']")
        note.click()

        time.sleep(1)
        select_custom_message = self.driver.find_element(
            By.XPATH, "//textarea[@id='custom-message']")

        time.sleep(1)
        message = f'Olá {name}, tudo bem? ' + custom_message
        select_custom_message.send_keys(message)

        time.sleep(1)

    def logout(self):
        self.disable_stop_button()
        self.driver.get('https://www.linkedin.com/m/logout/')
        time.sleep(3)
        self.driver.quit()
        self.add_message(messages_to_show[self.language]["logout"])

    def scroll_page(self, duration=5):
        start = time.time()

        init_scroll = 0
        final_scroll = 1000

        while True:
            self.driver.execute_script(
                f"window.scrollTo({init_scroll}, {final_scroll})")
            init_scroll = final_scroll
            final_scroll += 1000
            time.sleep(3)

            end = time.time()

            if round(end - start) > duration:
                break
