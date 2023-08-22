import time
import json
import os
from re import match
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


class LinkedInBot:
    def __init__(self, num_of_connections):
        self.driver = webdriver.Chrome()
        self.actual_page = 1
        self.num_of_connections = int(num_of_connections)
        self.counter = 0

    def start_bot(self):
        self.driver.get("https://br.linkedin.com/")

    def login(self, email, password):
        try:
            user = self.driver.find_element(By.ID, 'session_key')
            password_element = self.driver.find_element(By.ID, 'session_password')
            button = self.driver.find_element(By.CSS_SELECTOR, '[data-id="sign-in-form__submit-btn"]')
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
    EC.presence_of_element_located((By.CLASS_NAME, 'search-global-typeahead__input')))

        search.send_keys(search_term)
        search.send_keys(Keys.ENTER)

        people_tab = WebDriverWait(self.driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Ver todos os resultados de pessoas")]')))
        people_tab.click()

    def connect(self, custom_message):
        while self.num_of_connections > self.counter:
            time.sleep(5)
            people = self.driver.find_elements(By.XPATH, "//li[@class='reusable-search__result-container']//*[text()='Conectar']/parent::*")
            for person in people:
                try:
                    time.sleep(5)
                    text_span = person.find_element(By.XPATH, ".//span[@class='artdeco-button__text']")
                    if 'Conectar' in text_span.text:
                        name = person.find_element(By.XPATH, "./../../..//span[@dir='ltr']//span[@aria-hidden='true']")
                        
                        name = name.text.split()
                        name = name[0]

                        conect_button = person
                        conect_button.click()

                        time.sleep(5)
                        self.select_note(custom_message, name)

                        send = self.driver.find_element(By.XPATH, "//button[@aria-label='Enviar agora']")
                        send.click()
                        time.sleep(5)
                        self.counter += 1
                except:
                    pass
                if self.num_of_connections == self.counter:
                    break
            self.actual_page += 1
            time.sleep(10)
            page = self.driver.find_element(By.XPATH, f'//li[@data-test-pagination-page-btn="{self.actual_page}"]')            
            page.click()

    def select_note(self, custom_message, name):
        time.sleep(1)
        note = self.driver.find_element(By.XPATH, "//button[@aria-label='Adicionar nota']")
        note.click()

        time.sleep(1)
        select_custom_message = self.driver.find_element(By.XPATH, "//textarea[@id='custom-message']")

        time.sleep(1)
        message = f'Olá {name}, tudo bem? ' + custom_message
        select_custom_message.send_keys(message)

        time.sleep(1)


    def logout(self):
        self.driver.get('https://www.linkedin.com/m/logout/')
        self.driver.quit()


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
            'start_btn' : 'START',
            'stop_btn' : 'STOP',
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
            'start_btn' : 'INICIAR',
            'stop_btn' : 'PARAR',
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
 