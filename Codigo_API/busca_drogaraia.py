from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sqlite3


'''Apenas um dos codigos de farmacia esta comentado. 
Pois os outros são apenas adaptações,sendo assim, muito similares'''


def buscadrogaraia(param, number):
    try:
        '''recebe o nome do medicamento e coloca tudo em minusculo,
         cria a url de pesquisa do site'''
        pesquisa = param.lower()
        number = int(number)
        url = "https://busca.drogaraia.com.br/search?w="
        url = url + pesquisa
    except:
        return ("Drogaraia\n"
                "Problema na converção para minusculo da drogaraia "
                "e na geração da URL de pesquisa no site. Provalvelmente entre as linhas 24 à 29")

    conn = sqlite3.connect('Farmala_api.db')
    cur = conn.cursor()
    cur.execute("Select url from Medicamentos_Drogaraia where nmMedicamento = ?", (pesquisa,))
    resultado = cur.fetchall()
    result1 = False
    for row in resultado:
        result = str(row[0])
        result1 = result
    conn.commit()

    if not result1 or number > 1:

        try:
            '''Codigo executado caso seja nescessario 
               mais de um medicamento da farmacia'''

            '''Inicia o selenium em navegador especifico 
            OBS: navegador em background'''
            option = Options()
            option.headless = True
            driver = webdriver.Chrome(options=option)
            driver.get(url)
        except:
            return ("Drogaraia"
                    "Problema na inicialização do Selenium para varios medicamentos."
                    "Provalvelmente entre as linhas 151 à 160")



        '''Codigo que inicia o selenium e captura parte do codigo html do site'''
        elem = driver.find_element_by_xpath('//*[@id="sli_content_wrapper"]/div[1]/div[4]/div[2]/div/ul')

        '''Salva o codigo html do site'''
        source_code = elem.get_attribute("outerHTML")

        '''Efetua o parser para BEATIFULSOUP possibilitanto 
        maior velociade de resposta'''
        soup = BeautifulSoup(source_code, "html.parser")


        '''Inicia algumas variasveis e arrays '''
        i = 0
        quant = number
        resp1 = []
        resp2 = []
        resp3 = []
        retorn = []

        '''Estrutura de repetição para capturar todas as tags
         especificas e nescessaria para a resposta'''
        for limp in soup:
            ulList = limp.find_all('li')
            for li in ulList:

                '''Efetua parte do tratamento para captura do nome, preco e link do medicamento '''
                nome = li.find_all('h2', class_="product-name sli_title")
                try:
                    preco = li.find_all('p', class_="special-price")
                except:
                    preco = li.find_all('span', class_="regular-price")

                '''limpa e concatena o nome, preco  e link do medicamento '''
                for li1 in nome:
                    resp1 = li1.text
                for li2 in preco:
                    resp2 = li2.text
                    resp2 = resp2.replace(",", ".")
                for li4 in nome:
                    resp3 = li4.a['title']

                    '''Concatena e trata para facilitar o tratamento da resposta final'''
                for li3 in preco:
                    if i < quant:
                        resp1 = resp1.replace("\n\n", "")
                        resp1 = resp1.replace("\n","")
                        resp1 = resp1.strip()
                        retorn.append({'Farmacia' : 'Drogaraia',
                                        'nome' : resp1,
                                        'preco' : resp2,
                                       'Link' : resp3})
                        i = i + 1
                        if quant == 1:
                            link1 = resp3
                            entities = (pesquisa, link1)
                            cur.execute('INSERT INTO Medicamentos_Drogaraia (nmMedicamento,url) VALUES(?, ?)',
                                        entities)
                            conn.commit()
        '''Finaliza o tratamento da resposta final'''
        retorn = str(retorn)
        retorn = retorn.replace("[", "")
        retorn = retorn.replace("]", "")
        retorn = retorn.replace("{", " \n")
        retorn = retorn.replace("}", "")
        retorn = retorn.replace(",", "\n")
        retorn = retorn.strip()
        retorn = '{' + retorn + '}'
        driver.quit()
        '''retorna a resposta final '''

        return retorn

    else:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

        site = requests.get(result1, headers=headers)

        soup = BeautifulSoup(site.content, "html.parser")
        nome = soup.find('span', property="name", ).get_text().strip()
        preco = soup.find('p', class_="special-price", ).get_text().strip()
        linkcom = result1
        retorno = ("{\"nome\"" ":" + "\"" + nome + "\"" + "\n" + "\"preco\"" ":" + "\"" + preco + "\"" + "\n" + "\"Link\"" ":" + "\"" + linkcom + "\"}" )

        return retorno

