import time

from busca_pa import busca
from busca_ultrafarma import buscaultrafarma
from busca_drogaraia import buscadrogaraia
import sqlite3
import threading

teste_um={
    "Nome do Medicamento": "paracetamol",
    "Quantidade geral(Maximo 15)": "1",
}
nome = teste_um["Nome do Medicamento"]
quant_pa = teste_um["Quantidade geral(Maximo 15)"]
quant_ultra = teste_um["Quantidade geral(Maximo 15)"]
quant_raia = teste_um["Quantidade geral(Maximo 15)"]


def teste():
    ini = time.time()
    test1 = testar_salvo()
    test2 = testar_novo()
    test3 = testar_varios()
    if test2 == 0:
        return(test2)
    else:
        result = ("Resultado dos testes:\n" + "\nTeste de uma valor e um medicamento ja salvo no banco de cada farmacia: \n\n" + test1 + "" \
            "\n\nTeste de um valor com medicamento não salvo no banco das farmacias:\n\n" + test2 + "" \
            "\nTeste de varios valores em cada farmacia:\n" + test3 )
        fim = time.time()
        print(ini - fim)
        return result


def testar_salvo():

    threading.Thread(target=buscaultrafarma, args=(nome, quant_ultra)).start()
    threading.Thread(target=busca, args=(nome, quant_pa)).start()
    buscarRaia = buscadrogaraia(nome, quant_raia)
    time.sleep(5)

    init_ultra = open("resultadoultra.txt", "r")
    buscarUltra = init_ultra.read()
    init_ultra.close()

    init_pacheco = open("resultadopacheco.txt", "r")
    buscarPacheco = init_pacheco.read()
    init_pacheco.close()

    return buscarUltra + '\n' + buscarPacheco + '\n\n' + buscarRaia

def testar_novo():
    try:
        conn = sqlite3.connect('Farmala_api.db')
        cur = conn.cursor()
        cur.execute("""DELETE FROM Medicamentos_Drogaraia WHERE nmMedicamento = ?""", (nome,))
        cur.execute("""DELETE FROM Medicamentos_pacheco WHERE Nome_Medicamento = ?""", (nome,))
        cur.execute("""DELETE FROM Medicamentos_Ultrafarma WHERE nmMedicamento = ?""", (nome,))
        conn.commit()

    except:
        init_ultra = open("resultadoultra.txt", "w")
        init_ultra.write(("\nProblema no teste de deletar dados da farmacia\n"))
        init_ultra.close()
        init_ultra = open("resultadopacheco.txt", "w")
        init_ultra.write(("\nProblema no teste de deletar dados da farmacia\n"))
        init_ultra.close()
        return 0

    threading.Thread(target=buscaultrafarma, args=(nome, quant_ultra)).start()
    threading.Thread(target=busca, args=(nome, quant_pa)).start()
    buscarRaia = buscadrogaraia(nome, quant_raia)
    time.sleep(5)

    init_ultra = open("resultadoultra.txt", "r")
    buscarUltra = init_ultra.read()
    init_ultra.close()

    init_pacheco = open("resultadopacheco.txt", "r")
    buscarPacheco = init_pacheco.read()
    init_pacheco.close()

    return buscarUltra + '\n' + buscarPacheco + '\n\n' + buscarRaia

def testar_varios():
    teste_varios = {
        "Nome do Medicamento": "paracetamol",
        "Quantidade geral(Maximo 15)": "15"
    }
    nome = teste_varios["Nome do Medicamento"]
    quant_geral = teste_varios["Quantidade geral(Maximo 15)"]


    threading.Thread(target=buscaultrafarma, args=(nome, quant_geral)).start()
    threading.Thread(target=busca, args=(nome, quant_geral)).start()
    buscarRaia = buscadrogaraia(nome, quant_geral)
    time.sleep(5)

    init_ultra = open("resultadoultra.txt", "r")
    buscarUltra = init_ultra.read()
    init_ultra.close()

    init_pacheco = open("resultadopacheco.txt", "r")
    buscarPacheco = init_pacheco.read()
    init_pacheco.close()

    return buscarUltra + '\n' + buscarPacheco + '\n\n' + buscarRaia






