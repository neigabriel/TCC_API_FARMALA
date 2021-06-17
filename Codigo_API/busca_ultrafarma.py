from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import sqlite3
import requests

def buscaultrafarma(param, number):
    try:
        pesquisa = param.lower()
        url = "https://www.ultrafarma.com.br/busca?q="
        number = int(number)
        url = url + pesquisa

        conn = sqlite3.connect('Farmala_api.db')
        cur = conn.cursor()
        cur.execute("Select url from Medicamentos_Ultrafarma where nmMedicamento = ?", (pesquisa,))
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


            elem = driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[4]/div/div/div/div/div')
            source_code = elem.get_attribute("outerHTML")
            soup = BeautifulSoup(source_code, "html.parser")
            i = 0
            quant = number
            resp1 = []
            resp2 = []
            resp3 = []
            retorn = []
            for limp in soup:
                ulList = limp.find_all('div', class_="col-xs-6 col-sm-6 col-lg-2 prd-list-item")
                for li in ulList:
                    nome = li.find_all('h3', class_="product-name")
                    preco = li.find_all('span', class_="product-price-sell")
                    link = li.find_all('a', class_="product-item-link in_stock")
                    for li1 in nome:
                        resp1 = li1.text
                    for li2 in preco:
                        resp2 = li2.text
                        resp2 = resp2.replace(",", ".")
                    for li4 in link:
                        resp3 = li4['href']
                    for li3 in preco:
                        if i < quant:
                            retorn.append({'Farmacia' : 'Ultrafarma',
                                            'nome' : resp1,
                                            'preco' : resp2,
                                           'Link' : resp3})
                            i = i + 1
                            if quant == 1:
                                link1 = resp3
                                entities = (pesquisa, link1)
                                cur.execute('INSERT INTO Medicamentos_Ultrafarma (nmMedicamento,url) VALUES(?, ?)',entities)
                                conn.commit()

            retorn = str(retorn)
            retorn = retorn.replace("[", "")
            retorn = retorn.replace("]", "")
            retorn = retorn.replace("{", " \n")
            retorn = retorn.replace("}", "")
            retorn = retorn.replace(",", "\n")
            retorn = retorn.strip()
            retorn = '{' + retorn + '}'
            arquivo = open('resultadoultra.txt', 'w')
            arquivo.write(retorn)
            arquivo.close()
            return 0



        else:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

            site = requests.get(result1, headers=headers)

            soup = BeautifulSoup(site.content, "html.parser")
            nome = soup.find('h1', class_="product-name").get_text().strip()
            preco = soup.find('p', class_="product-price-new", ).get_text().strip()
            linkcom = result1
            retorno = ("{\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"}")
            arquivo = open('resultadoultra.txt', 'w')
            arquivo.write(retorno)
            arquivo.close()
            return 0
    except:
        retorn = ("\n\nProblemas na Ultrafarma ou não possui o medicamento\n\n" )
        arquivo = open('resultadoultra.txt', 'w')
        arquivo.write(retorn)
        arquivo.close()
        return 0





