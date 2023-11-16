from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    numero = float(request.form['numero'])
    tipo_logaritmo = request.form['tipo_logaritmo']

    if tipo_logaritmo == 'log':
        resultado = np.log10(numero)
    elif tipo_logaritmo == 'ln':
        resultado = np.log(numero)
    else:
        return "Tipo de logaritmo inválido"

    # Criação do gráfico
    x = np.linspace(0.01, 2, 100)
    y1 = np.log10(x) if numero > 1 else -np.log10(x)

    fig, ax = plt.subplots()
    ax.plot(x, y1, label=f'f(x) = log(x){"+" if numero > 1 else "-"}')

    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)

    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    # Salva a imagem do gráfico em um buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Converte a imagem para base64
    grafico_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return render_template('resultado.html', resultado=resultado, grafico_base64=grafico_base64)

if __name__ == '__main__':
    app.run(debug=True)
