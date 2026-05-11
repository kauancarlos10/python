from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('/') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def ola_mundo():
    return 'O decorator é!' # Isso é o que será retornado quando a rota '/' for acessada

@app.route('/decorator') # Isso é outro decorator, mapeando a função abaixo para a rota '/hello'
def hello():
    return 'Um decorator em Python é uma função que modifica ou estende o comportamento de outra função, método ou classe sem alterar seu código-fonte original \n Um decorator em Python é uma ferramenta poderosa e elegante que permite modificar ou aprimorar o comportamento de funções, métodos ou classes sem alterar o seu código-fonte original. ' # Isso é o que será retornado quando a rota '/hello' for acessada

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolviment1
    