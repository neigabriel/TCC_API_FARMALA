from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
import requests

def busca(param, number):
    try:
        number = int(number)
        pesq = param.lower()
        url = "https://www.drogariaspacheco.com.br/pesquisa?q="
        url = url + pesq

        conn = sqlite3.connect('Farmala_api.db')
        cur = conn.cursor()
        cur.execute("Select URL from Medicamentos_pacheco where Nome_medicamento = ?", (pesq,))
        resultado = cur.fetchall()
        result1 = False
        for row in resultado:
            result = str(row[0])
            result1 = result
        conn.commit()

        if not result1 or number > 1:
            option = Options()
            option.headless = True
            driver = webdriver.Chrome(options=option)
            driver.get(url)

            elem = driver.find_element_by_xpath('/html/body/main/div[4]/div/div/div/div[2]/div[1]/ul')
            source_code = elem.get_attribute("outerHTML")
            soup = BeautifulSoup(source_code, "html.parser")
            i = 0
            quant = number
            resp1 = []
            resp2 = []
            resp3 = []
            retorn = []
            for limp in soup:
                ulList = limp.find_all('li')
                for li in ulList:
                    nome = li.find_all('a', class_="collection-link")
                    preco = li.find_all('a', class_="valor-por")

                    for li1 in nome:
                        resp1 = li1.text
                    for li2 in preco:
                        resp2 = li2.text
                        resp2 = resp2.replace(",", ".")
                    for li3 in preco:
                        resp3 = li3['href']
                    for li4 in preco:
                        if i < quant:
                            retorn.append({'Farmacia' : 'Pacheco',
                                            'nome' : resp1,
                                            'preco' : resp2,
                                           'Link' : resp3})
                            i = i + 1
                            if quant == 1:
                                resp3 = str(resp3)
                                resp3 = resp3.replace('//', 'http://')
                                resp3.strip()
                                link1 = resp3
                                entities = (pesq, link1)
                                cur.execute('INSERT INTO Medicamentos_pacheco (Nome_Medicamento,url) VALUES(?, ?)',entities)
                                conn.commit()

            retorn = str(retorn)
            retorn = retorn.replace("[", "")
            retorn = retorn.replace("]", "")
            retorn = retorn.replace("{", " \n")
            retorn = retorn.replace("}", "")
            retorn = retorn.replace(",", "\n")
            retorn = retorn.replace("//", "")
            retorn = '{' + retorn + '}'
            arquivo = open('resultadopacheco.txt', 'w')
            arquivo.write(retorn)
            arquivo.close()
            driver.quit()
            return 0
        else:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

            site = requests.get(result1, headers=headers)

            soup = BeautifulSoup(site.content, "html.parser")
            nome = soup.find('h1').get_text()
            preco = soup.find('strong', class_="skuBestPrice").get_text().strip()
            linkcom = result1
            retorno = ("{\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"}")
            arquivo = open('resultadopacheco.txt', 'w')
            arquivo.write(retorno)
            arquivo.close()
            return 0
    except:
        arquivo = open('resultadopacheco.txt', 'w')
        arquivo.write("\n\nproblemas na pacheco ou  não possui esse medicamento\n\n")
        arquivo.close()
        return 0


