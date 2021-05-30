from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import sqlite3


def buscadrogaraia(param):
    conn = sqlite3.connect('Farmala_api.db')
    cur = conn.cursor()
    pesquisa = param.lower()
    url = "https://busca.drogaraia.com.br/search?w="
    url = url + pesquisa

    cur.execute("Select url from Medicamentos_Drogaraia where nmMedicamento = ?", (pesquisa,))
    resultado = cur.fetchall()
    result1 = False
    for row in resultado:
        result = str(row[0])
        result1 = result
    conn.commit()

    if not result1:
        option = Options()
        option.headless = True
        driver = webdriver.Firefox(options=option)
        driver.get(url)
        try:
            button = driver.find_element_by_xpath('//*[@id="sli_content_wrapper"]/div[1]/div[4]/div[2]/div/ul/li[1]/div/div[3]/h2/a').click()
            time.sleep(2)
            linkcom = (driver.current_url)
            nome = driver.find_element_by_xpath('//*[@id="product_addtocart_form"]/div[2]/div[2]/div/div[4]/div[1]/div[1]/h1/span').text
            preco = driver.find_element_by_xpath('//*[@id="product_addtocart_form"]/div[2]/div[2]/div/div[2]/div/div/div/span/p[2]').text
            entities = (pesquisa, linkcom)
        except:
            falta = "A Drograria Raia não possui esse medicamento"
            return falta
        cur.execute('INSERT INTO Medicamentos_Drogaraia (nmMedicamento,url) VALUES(?, ?)', entities)
        conn.commit()

        retorno =  ("\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"" "\n" )
        driver.quit()

        return retorno
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

        site = requests.get(result1, headers=headers)

        soup = BeautifulSoup(site.content, "html.parser")
        nome = soup.find('span', property="name",).get_text().strip()
        preco = soup.find('p', class_="special-price", ).get_text().strip()
        linkcom = result1
        retorno = ("\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"" "\n" )

        return retorno

