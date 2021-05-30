from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import sqlite3

def buscaultrafarma(param):
    conn = sqlite3.connect('Farmala_api.db')
    cur = conn.cursor()
    pesquisa = param.lower()
    url = "https://www.ultrafarma.com.br/busca?q="
    url = url + pesquisa

    cur.execute("Select url from Medicamentos_Ultrafarma where nmMedicamento = ?", (pesquisa,))
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
            button = driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[4]/div/div/div/div/div/div[1]/div/div/a[1]').click()
            time.sleep(2)
            linkcom = (driver.current_url)
            nome = driver.find_element_by_xpath('/html/body/div[1]/section[1]/div[1]/div/div[2]/div/div[2]/h1').text
            preco = driver.find_element_by_xpath('/html/body/div[1]/section[1]/div[1]/div/div[2]/div/div[2]/div[2]/p[2]/span[2]').text
        except:
            falta = "A Drograria Ultrafarma não possui esse medicamento"
            return falta
        entities = (pesquisa, linkcom)
        cur.execute('INSERT INTO Medicamentos_Ultrafarma (nmMedicamento,url) VALUES(?, ?)', entities)
        conn.commit()

        retorno = ("\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"" "\n" )
        return retorno
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

        site = requests.get(result1, headers=headers)

        soup = BeautifulSoup(site.content, "html.parser")
        nome = soup.find('h1', class_="product-name").get_text().strip()
        preco = soup.find('p', class_="product-price-new",).get_text().strip()
        linkcom = result1
        retorno = ("\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"" "\n" )
        return retorno
