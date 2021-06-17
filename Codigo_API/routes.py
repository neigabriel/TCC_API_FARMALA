import time
from busca_pa import busca
from testar import teste
import threading
from busca_ultrafarma import buscaultrafarma
from busca_drogaraia import buscadrogaraia
from flask_restx import Api,Resource,fields
from flask import Flask,request
from flask_cors import CORS,cross_origin

'''Carrega o FLASK'''
app = Flask(__name__)

'''Libera o cabeçalho CORS'''
CORS(app)

'''Define a rota e o metodo HTTP'''
@app.route("/pesquisa", methods = ["POST"])
@cross_origin("*")
def buscar():
    if request.get_json():
        resp = request.get_json()
        '''Cria uma variavel para verificação futura'''
        inva = 0
        '''Cada variavel pega sua respectiva parte do json'''

        nome = resp["Nome do Medicamento"]
        quant_geral = resp["Quantidade geral(Maximo 15)"]
        quant_pa = resp["Quantidade Pacheco(Ignore para quantidade geral ou Maximo 15)"]
        quant_ultra = resp["Quantidade UltraFarma(Ignore para quantidade geral ou Maximo 15)"]
        quant_raia = resp["Quantidade Drogaraia(Ignore para quantidade geral ou Maximo 15)"]
        test = resp['Digite 1 para efetuar o auto teste o ignore para executar normalmente']
        try:
            test = int(test)
        except:
            test = test
        if test == 1:
            return teste()
        else:
            '''Efetua algumas verificações simples em relação aos dados recebidos'''

            '''Geral'''
            if quant_geral == "" or quant_geral == "string" or quant_geral == "0":
                quant_ver = 16
            else:
                quant_ver = int(quant_geral)
            if quant_ver > 15 :
                inva = 1
                quant_geral = 1

            '''Pacheco'''
            if quant_pa == "" or quant_pa == "string" or quant_pa == "0":
                quant_ver = 16
            else:
                quant_ver = int(quant_pa)
            if quant_ver >15:
                quant_pa = quant_geral

            '''UltraFarma'''
            if quant_ultra == "" or quant_ultra == "string" or quant_ultra == "0":
                quant_ver = 16
            else:
                quant_ver = int(quant_ultra)
            if quant_ver > 15:
                quant_ultra = quant_geral

            '''DrogaRaia'''
            if quant_raia == "" or quant_raia == "string" or quant_raia == "0":
                quant_ver = 16
            else:
                quant_ver = int(quant_raia)
            if quant_ver > 15:
                quant_raia = quant_geral

            '''Efetua a chamada das funções nescessarias para o retorno da API'''

            ini = time.time()
            threading.Thread(target = buscaultrafarma, args=(nome, quant_ultra)).start()
            threading.Thread(target = busca, args=(nome, quant_pa)).start()
            buscarRaia = buscadrogaraia(nome, quant_raia)
            if quant_geral or quant_pa or quant_raia or quant_ultra == 1:
                time.sleep(4)

            init_ultra = open("resultadoultra.txt", "r")
            buscarUltra = init_ultra.read()
            init_ultra.close()

            init_pacheco = open("resultadopacheco.txt", "r")
            buscarPacheco = init_pacheco.read()
            init_pacheco.close()

            '''Verifica se os dados recebidos são validos '''
            if inva == 0:
                fim = time.time()
                print(ini - fim)
                return buscarUltra + '\n' + buscarPacheco + '\n\n' + buscarRaia
            else:

                '''Retorna um aviso e uma resposta DEFAULT'''
                return('Quantidade geral invalida. Sera definida quantidade Default\n\n' + buscarRaia + "\n" + buscarUltra + "\n" + buscarPacheco )




'''Inicio do Flaskrestx nescessario para o uso do swagger,
com os dados da API'''

api = Api(app,
        version = '1.0',
        title = 'Famala_API',
        description = 'Busca de medicamento ',
        doc ='/doc')

'''Configuração da exibição dos dados no swagger '''

template = api.model('template', {
'Nome do Medicamento' : fields.String(description = 'o nome do remedio'),
'Quantidade geral(Maximo 15)' : fields.String(description = 'Numero real'),
'Quantidade Pacheco(Ignore para quantidade geral ou Maximo 15)' : fields.String(description = 'Numero real'),
'Quantidade UltraFarma(Ignore para quantidade geral ou Maximo 15)' : fields.String(description = 'Numero real'),
'Quantidade Drogaraia(Ignore para quantidade geral ou Maximo 15)' : fields.String(description = 'Numero real'),
'Digite 1 para efetuar o auto teste o ignore para executar normalmente' : fields.String(description = 'numerol real')
})

'''Rota do swagger não e ultilizada esta presente apenas 
para que o FLASK_RESTX reconheça os metodos da API '''

@api.route("/pesquisa")
class documentation(Resource):
    @api.expect(template)
    def post(self, ):
        if request.get_json():
            resp = request.get_json()
            nome = resp["Nome do Medicamento"]
            quant = resp["Quantidade de cada farmacia(Maximo 15)"]
            buscarPacheco = busca(resp, quant)
            buscarUltra = buscaultrafarma(nome, quant)
            buscarRaia = buscadrogaraia(nome, quant)

            return buscarRaia
        else:
            return {"Erro": "Um Nome Deve Ser Pesquisado"}