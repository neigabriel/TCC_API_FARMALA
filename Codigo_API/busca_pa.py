from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sqlite3
import time




def busca(param):
    conn = sqlite3.connect('Farmala_api.db')
    cur = conn.cursor()

    pesq = param.lower()
    url = "https://www.drogariaspacheco.com.br/pesquisa?q="
    url = url + pesq

    cur.execute("Select URL from Medicamentos_pacheco where Nome_medicamento = ?", (pesq,))
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
            button = driver.find_element_by_xpath('/html/body/main/div[4]/div/div/div/div[2]/div[1]/ul/li[1]/div[1]').click()
            time.sleep(2)
            linkcom = driver.current_url
            entities = (pesq, linkcom)
            cur.execute('INSERT INTO Medicamentos_pacheco (Nome_medicamento,URL) VALUES(?, ?)', entities)
            conn.commit()
            nome = driver.find_element_by_xpath('/html/body/main/div[1]/div/div/div[1]/div/div[2]/h1/div').text
            preco = driver.find_element_by_xpath('/html/body/main/div[1]/div/div/div[2]/div/div[1]/div[2]/div/p[1]/em[1]/strong').text
            preco = str(preco)
        except:
            falta = "A Drograria Pacheco não possui esse medicamento"
            return falta
        retorno = ("\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"" "\n" )
        driver.quit()
        return retorno
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

        site = requests.get(result1, headers=headers)

        soup = BeautifulSoup(site.content, "html.parser")
        nome = soup.find('h1').get_text()
        preco = soup.find('strong', class_="skuBestPrice").get_text().strip()
        linkcom = result1
        retorno = ("\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"" "\n" )
        return retorno

