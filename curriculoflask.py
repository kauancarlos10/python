from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Currículo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
            background-color: #f4f4f9;
        }
        .container {
            background: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        header {
            border-bottom: 2px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }
        h1 { margin: 0; color: #2c3e50; }
        .contato { color: #7f8c8d; font-size: 0.9em; }
        
        h2 { 
            color: #3498db; 
            text-transform: uppercase; 
            font-size: 1.2em; 
            border-left: 4px solid #3498db;
            padding-left: 10px;
            margin-top: 30px;
        }
        
        .item { margin-bottom: 15px; }
        .item-titulo { font-weight: bold; color: #2c3e50; }
        .item-detalhe { font-style: italic; color: #555; }
        
        ul { padding-left: 20px; }
        .idiomas span {
            background: #3498db;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            margin-right: 5px;
        }
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1>Kauan carlos carneiro dos santos</h1>
        <div class="contato">
            <span>📞 (31) 9999-9999</span> | 
            <span>✉️ 12402516@aluno.cotemig.com.br</span>
        </div>
    </header>

    <section>
        <h2>🎓 Formação Acadêmica</h2>
        <div class="item">
            <div class="item-titulo">colegio e faculdade cotemig</div>
            <div class="item-detalhe">Curso em andamento | iniciado em 2023 </div>
        </div>
    </section>

    <section>
        <h2>💼 Experiência Profissional</h2>
        <div class="item">
            <div class="item-titulo">Nome da Empresa</div>
            <div class="item-detalhe">Cargo Ocupado | Jan/2022 – Atualmente</div>
            <p>Descrição breve das atividades e conquistas no cargo.</p>
        </div>
    </section>

    <section>
        <h2>📜 Cursos e Certificações</h2>
        <ul>
            <li>Desenvolvimento Web com Python e Flask</li>
            <li>Banco de Dados SQL</li>
        </ul>
    </section>

    <section>
        <h2>🌐 Idiomas</h2>
        <div class="idiomas">
            <p><strong>Inglês:</strong> <span>Avançado</span></p>
            <p><strong>Espanhol:</strong> <span>Intermediário</span></p>
        </div>
    </section>
</div>

</body>
</html>

'''
if __name__ == '__main__':
    app.run(debug=True)