
function fazPost(url, body) {
    console.log("Body=", body)
    let request = new XMLHttpRequest()
    request.open("POST", url, true)
    request.setRequestHeader("Content-type", "application/json")
    request.send(JSON.stringify(body))

    request.onload = function() {
        alert(this.responseText)
    }

    return request.responseText
}


function cadastraUsuario() {
    event.preventDefault()
    let url = "http://localhost:5000/pesquisa"
    let nome = document.getElementById("nome").value
    let quant = document.getElementById("quant").value
    console.log(nome)
    console.log(quant)
    res = 'string'

    body = {
        "Nome do Medicamento": nome,
        "Quantidade geral(Maximo 15)": quant,
        "Quantidade Pacheco(Ignore para quantidade geral ou Maximo 15)": res,
        "Quantidade UltraFarma(Ignore para quantidade geral ou Maximo 15)": res,
        "Quantidade Drogaraia(Ignore para quantidade geral ou Maximo 15)": res,
        "Digite 1 para efetuar o auto teste o ignore para executar normalmente": res
      }
    

    fazPost(url, body)
}