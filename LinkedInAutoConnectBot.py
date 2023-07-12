"""
Wanderson Soares dos Santos - 10-07-2023
Script Developed with Selenium with the capacity of
make automatizaded conections
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get("https://br.linkedin.com/")

time.sleep(5)
pesquisar = driver.find_element(By.ID, 'session_key')
pesquisar.send_keys('email') # put your e-mail

senha = driver.find_element(By.ID, 'session_password')
senha.send_keys('password') # put your password

button = driver.find_element(By.CSS_SELECTOR, '[data-id="sign-in-form__submit-btn"]')
button.click()

time.sleep(20) # time to pass through authentication, if it's necessary

search = driver.find_element(By.CLASS_NAME, 'search-global-typeahead__input')
search.send_keys('python developer flask')
# put in the send keys above which interest you want to research
search.send_keys(Keys.ENTER)

time.sleep(3)
tab_people = driver.find_element(By.XPATH,
                                 '//a[contains(text(), "Ver todos os resultados de pessoas")]')
tab_people.click()

time.sleep(2)
people = driver.find_elements(By.XPATH, "//li[@class='reusable-search__result-container']")

for person in people:
    name = person.find_element(By.XPATH, ".//span[@dir='ltr']//span[@aria-hidden='true']")
    # pegar o nome
    name = name.text.split()
    name = name[0]


    text_span = person.find_element(By.XPATH, ".//span[@class='artdeco-button__text']")
    if text_span.text == 'Conectar':
        conect_button = person.find_element(By.XPATH, ".//button")

        conect_button.click()

        time.sleep(1)

        note = driver.find_element(By.XPATH, "//button[@aria-label='Adicionar nota']")
        # Seleciona o botão Adicionar Nota
        note.click()

        custom_message = driver.find_element(By.XPATH, "//textarea[@id='custom-message']")
        # select the custom message textarea

        custom_message.send_keys(f'Olá {name}, tudo bem? '
        'Eu vi que temos interesses em comum, e seria um prazer estar conectado com você no '
        'LinkedIn. Agradeço a atenção.')
        # put in the send_keys above which message do you want to send to your new connections

        send = driver.find_element(By.XPATH, "//button[@aria-label='Enviar agora']")
        send.click()

        time.sleep(1)

driver.get('https://www.linkedin.com/m/logout/')
# log out of linkedin

time.sleep(3)

driver.quit()
