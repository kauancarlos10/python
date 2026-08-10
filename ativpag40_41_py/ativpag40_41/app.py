import os
import sqlite3
from functools import wraps

import requests
from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-troque-em-producao"),
    DATABASE=os.path.join(app.instance_path, "tarefas.sqlite3"),
)
os.makedirs(app.instance_path, exist_ok=True)

STATUS_VALIDOS = {"pendente", "andamento", "concluida"}
FILTROS_VALIDOS = {"todas", *STATUS_VALIDOS}


def banco():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def encerrar_banco(exc=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def preparar_banco():
    banco().executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'pendente'
                CHECK(status IN ('pendente', 'andamento', 'concluida')),
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        """
    )
    banco().commit()


@app.cli.command("init-db")
def inicializar_comando():
    with app.app_context():
        preparar_banco()
    print("Banco de dados inicializado.")


def exige_login(funcao):
    @wraps(funcao)
    def protegida(*args, **kwargs):
        if g.usuario is None:
            flash("Entre na sua conta para continuar.", "warning")
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)

    return protegida


@app.before_request
def carregar_usuario():
    g.usuario = None
    identificador = session.get("user_id")
    if identificador is not None:
        g.usuario = banco().execute(
            "SELECT id, nome, email FROM usuarios WHERE id = ?", (identificador,)
        ).fetchone()


@app.context_processor
def dados_globais():
    return {"current_user": g.usuario}


def dados_tarefa_formulario():
    return (
        request.form.get("titulo", "").strip(),
        request.form.get("descricao", "").strip(),
        request.form.get("status", "pendente"),
    )


def buscar_tarefa_propria(tarefa_id):
    return banco().execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
        (tarefa_id, g.usuario["id"]),
    ).fetchone()


@app.route("/registro", methods=("GET", "POST"))
def registro():
    if g.usuario is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmacao = request.form.get("confirmar_senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
        elif senha != confirmacao:
            flash("As senhas precisam ser iguais.", "danger")
        elif len(senha) < 6:
            flash("A senha precisa ter pelo menos 6 caracteres.", "danger")
        else:
            try:
                cursor = banco().execute(
                    "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                    (nome, email, generate_password_hash(senha)),
                )
                banco().commit()
                session.clear()
                session["user_id"] = cursor.lastrowid
                flash("Cadastro realizado. Seja bem-vindo!", "success")
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                flash("Esse e-mail já possui cadastro.", "danger")

    return render_template("auth/registro.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if g.usuario is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = banco().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

        if usuario is None or not check_password_hash(usuario["senha"], senha):
            flash("Confira seu e-mail e sua senha.", "danger")
        else:
            session.clear()
            session["user_id"] = usuario["id"]
            flash("Login efetuado com sucesso!", "success")
            return redirect(url_for("dashboard"))

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("login"))


@app.route("/")
def index():
    return redirect(url_for("dashboard" if g.usuario else "login"))


@app.route("/dashboard")
@exige_login
def dashboard():
    filtro = request.args.get("status", "todas")
    if filtro not in FILTROS_VALIDOS:
        filtro = "todas"

    consulta = "SELECT * FROM tarefas WHERE usuario_id = ?"
    parametros = [g.usuario["id"]]
    if filtro != "todas":
        consulta += " AND status = ?"
        parametros.append(filtro)
    consulta += " ORDER BY id DESC"

    tarefas = banco().execute(consulta, parametros).fetchall()
    return render_template("dashboard.html", tarefas=tarefas, status_filter=filtro)


@app.route("/nova_tarefa", methods=("GET", "POST"))
@exige_login
def nova_tarefa():
    if request.method == "POST":
        titulo, descricao, status = dados_tarefa_formulario()
        if not titulo:
            flash("Informe um título para a tarefa.", "danger")
        elif status not in STATUS_VALIDOS:
            flash("O status informado não é válido.", "danger")
        else:
            banco().execute(
                "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)",
                (titulo, descricao, status, g.usuario["id"]),
            )
            banco().commit()
            flash("Tarefa adicionada ao seu painel.", "success")
            return redirect(url_for("dashboard"))

    return render_template("tarefa_form.html", tarefa=None)


@app.route("/editar/<int:task_id>", methods=("GET", "POST"))
@exige_login
def editar(task_id):
    tarefa = buscar_tarefa_propria(task_id)
    if tarefa is None:
        flash("Não encontramos essa tarefa.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        titulo, descricao, status = dados_tarefa_formulario()
        if not titulo:
            flash("Informe um título para a tarefa.", "danger")
        elif status not in STATUS_VALIDOS:
            flash("O status informado não é válido.", "danger")
        else:
            banco().execute(
                "UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?",
                (titulo, descricao, status, task_id, g.usuario["id"]),
            )
            banco().commit()
            flash("Alterações salvas.", "success")
            return redirect(url_for("dashboard"))

    return render_template("tarefa_form.html", tarefa=tarefa)


@app.post("/excluir/<int:task_id>")
@exige_login
def excluir(task_id):
    tarefa = buscar_tarefa_propria(task_id)
    if tarefa is None:
        flash("Não encontramos essa tarefa.", "danger")
    else:
        banco().execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (task_id, g.usuario["id"]),
        )
        banco().commit()
        flash("Tarefa removida.", "success")
    return redirect(url_for("dashboard"))


@app.post("/concluir/<int:task_id>")
@exige_login
def concluir(task_id):
    tarefa = buscar_tarefa_propria(task_id)
    if tarefa is None:
        flash("Não encontramos essa tarefa.", "danger")
    else:
        destino = "pendente" if tarefa["status"] == "concluida" else "concluida"
        banco().execute(
            "UPDATE tarefas SET status = ? WHERE id = ? AND usuario_id = ?",
            (destino, task_id, g.usuario["id"]),
        )
        banco().commit()
        flash("Status atualizado.", "success")
    return redirect(url_for("dashboard"))


@app.get("/api/progresso")
@exige_login
def api_progresso():
    linhas = banco().execute(
        "SELECT status, COUNT(*) AS total FROM tarefas WHERE usuario_id = ? GROUP BY status",
        (g.usuario["id"],),
    ).fetchall()
    resultado = {"pendente": 0, "andamento": 0, "concluida": 0}
    for linha in linhas:
        resultado[linha["status"]] = linha["total"]
    return jsonify(resultado)


@app.route("/dashboard/progresso")
@exige_login
def dashboard_progresso():
    return render_template("progresso.html")


@app.get("/api/frase")
@exige_login
def api_frase():
    frase_padrao = "Um passo de cada vez também é progresso."
    try:
        resposta = requests.get(
            "https://api.adviceslip.com/advice",
            timeout=5,
            headers={"Accept": "application/json"},
        )
        resposta.raise_for_status()
        conteudo = resposta.json().get("slip", {}).get("advice", "")
        if conteudo:
            return jsonify({"frase": conteudo})
    except (requests.RequestException, ValueError, TypeError):
        pass
    return jsonify({"frase": frase_padrao})


if __name__ == "__main__":
    with app.app_context():
        preparar_banco()
    app.run(debug=True)
