from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("Conexão com MySQL realizada com sucesso!")


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        nascimento = request.form["nascimento"]
        senha = request.form["senha"]
        senha_hash = generate_password_hash(senha)

        cursor = conexao.cursor()

        comando = """
        INSERT INTO pacientes
        (nome, email, telefone, data_nascimento, senha)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            nome,
            email,
            telefone,
            nascimento,
            senha_hash
        )

        cursor.execute(comando, valores)
        conexao.commit()
        cursor.close()

        return f"Paciente {nome} cadastrada com sucesso!"

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cursor = conexao.cursor(dictionary=True)

        comando = """
        SELECT *
        FROM pacientes
        WHERE email = %s
        """

        cursor.execute(comando, (email,))
        paciente = cursor.fetchone()

        cursor.close()

        if paciente and check_password_hash(paciente["senha"], senha):
            session["paciente_id"] = paciente["id"]
            session["paciente_nome"] = paciente["nome"]

            return render_template(
                "paciente.html",
                nome=paciente["nome"]
            )

        return "E-mail ou senha incorretos."

    return render_template("login.html")

@app.route("/agendar", methods=["GET", "POST"])
def agendar():

    if "paciente_id" not in session:
        return redirect(url_for("login"))

    horarios_clinica = [
        "08:00",
        "08:30",
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "14:00",
        "14:30",
        "15:00",
        "15:30",
        "16:00",
        "16:30",
        "17:00"
    ]

    feriados = [
        "2026-01-01",
        "2026-04-21",
        "2026-05-01",
        "2026-09-07",
        "2026-10-12",
        "2026-11-02",
        "2026-11-15",
        "2026-11-20",
        "2026-12-25"
    ]

    # SALVAR AGENDAMENTO
    if request.method == "POST":

        data_consulta = request.form["data_consulta"]
        horario = request.form["horario"]
        paciente_id = session["paciente_id"]

        data_obj = date.fromisoformat(data_consulta)

        # Impede datas passadas
        if data_obj < date.today():
            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_consulta,
                horarios_disponiveis=[],
                erro="Não é possível agendar uma consulta em uma data passada."
            )

        # Impede sábado e domingo
        if data_obj.weekday() >= 5:
            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_consulta,
                horarios_disponiveis=[],
                erro="A clínica não realiza atendimentos aos sábados e domingos."
            )

        # Impede feriados
        if data_consulta in feriados:
            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_consulta,
                horarios_disponiveis=[],
                erro="A clínica não realiza atendimentos nesta data devido ao feriado."
            )

        cursor = conexao.cursor(dictionary=True)

        # Verifica se a paciente já possui consulta ativa no mesmo dia
        comando_paciente = """
        SELECT id
        FROM agendamentos
        WHERE paciente_id = %s
        AND data_consulta = %s
        AND status = 'Agendada'
        LIMIT 1
        """

        cursor.execute(
            comando_paciente,
            (paciente_id, data_consulta)
        )

        consulta_existente = cursor.fetchone()

        if consulta_existente:
            cursor.close()

            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_consulta,
                horarios_disponiveis=[],
                erro="Você já possui uma consulta agendada para esta data."
            )

        # Verifica se o horário está ocupado
        comando_verificar = """
        SELECT id
        FROM agendamentos
        WHERE data_consulta = %s
        AND horario = %s
        AND status = 'Agendada'
        LIMIT 1
        """

        cursor.execute(
            comando_verificar,
            (data_consulta, horario)
        )

        horario_ocupado = cursor.fetchone()

        if horario_ocupado:
            cursor.close()

            return redirect(
                url_for(
                    "agendar",
                    data=data_consulta
                )
            )

        # Salva o agendamento
        comando = """
        INSERT INTO agendamentos
        (paciente_id, data_consulta, horario)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            comando,
            (paciente_id, data_consulta, horario)
        )

        conexao.commit()
        cursor.close()

        return redirect(url_for("consultas"))

    # MOSTRAR HORÁRIOS DISPONÍVEIS
    data_escolhida = request.args.get("data")

    horarios_disponiveis = horarios_clinica.copy()

    if data_escolhida:

        data_obj = date.fromisoformat(data_escolhida)

        # Impede datas passadas
        if data_obj < date.today():
            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_escolhida,
                horarios_disponiveis=[],
                erro="Não é possível agendar uma consulta em uma data passada."
            )

        # Impede sábado e domingo
        if data_obj.weekday() >= 5:
            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_escolhida,
                horarios_disponiveis=[],
                erro="A clínica não realiza atendimentos aos sábados e domingos."
            )

        # Impede feriados
        if data_escolhida in feriados:
            return render_template(
                "agendar.html",
                hoje=date.today().isoformat(),
                data_escolhida=data_escolhida,
                horarios_disponiveis=[],
                erro="A clínica não realiza atendimentos nesta data devido ao feriado."
            )

        cursor = conexao.cursor(dictionary=True)

        comando = """
        SELECT
            TIME_FORMAT(horario, '%H:%i') AS horario
        FROM agendamentos
        WHERE data_consulta = %s
        AND status = 'Agendada'
        """

        cursor.execute(
            comando,
            (data_escolhida,)
        )

        ocupados = cursor.fetchall()

        cursor.close()

        horarios_ocupados = {
            item["horario"]
            for item in ocupados
        }

        horarios_disponiveis = [
            horario
            for horario in horarios_clinica
            if horario not in horarios_ocupados
        ]

    return render_template(
        "agendar.html",
        hoje=date.today().isoformat(),
        data_escolhida=data_escolhida,
        horarios_disponiveis=horarios_disponiveis
    )

@app.route("/consultas")
def consultas():

    if "paciente_id" not in session:
        return redirect(url_for("login"))

    paciente_id = session["paciente_id"]

    cursor = conexao.cursor(dictionary=True)

    comando_atualizar = """
    UPDATE agendamentos
    SET status = 'Realizada'
    WHERE paciente_id = %s
    AND status = 'Agendada'
    AND (
        data_consulta < CURDATE()
        OR (
            data_consulta = CURDATE()
            AND horario < CURTIME()
        )
    )
    """

    cursor.execute(
        comando_atualizar,
        (paciente_id,)
    )

    conexao.commit()

    comando = """
    SELECT
        id,
        paciente_id,
        DATE_FORMAT(data_consulta, '%d/%m/%Y') AS data_formatada,
        TIME_FORMAT(horario, '%H:%i') AS horario_formatado,
        status
    FROM agendamentos
    WHERE paciente_id = %s
    ORDER BY
        CASE
            WHEN status = 'Agendada' THEN 1
            WHEN status = 'Realizada' THEN 2
            WHEN status = 'Cancelada' THEN 3
            ELSE 4
        END,
        data_consulta,
        horario
    """

    cursor.execute(
        comando,
        (paciente_id,)
    )

    consultas = cursor.fetchall()

    cursor.close()

    return render_template(
        "consultas.html",
        consultas=consultas
    )
@app.route("/cancelar/<int:id>", methods=["POST"])
def cancelar_consulta(id):

    if "paciente_id" not in session:
        return redirect(url_for("login"))

    paciente_id = session["paciente_id"]

    cursor = conexao.cursor()

    comando = """
    UPDATE agendamentos
    SET status = 'Cancelada'
    WHERE id = %s
    AND paciente_id = %s
    """

    cursor.execute(
        comando,
        (id, paciente_id)
    )

    conexao.commit()
    cursor.close()

    return redirect(url_for("consultas"))

@app.route("/dados")
def dados():

    if "paciente_id" not in session:
        return redirect(url_for("login"))

    paciente_id = session["paciente_id"]

    cursor = conexao.cursor(dictionary=True)

    comando = """
    SELECT
        nome,
        email,
        telefone,
        DATE_FORMAT(data_nascimento, '%d/%m/%Y') AS data_formatada
    FROM pacientes
    WHERE id = %s
    """

    cursor.execute(comando, (paciente_id,))
    paciente = cursor.fetchone()

    cursor.close()

    return render_template(
        "dados.html",
        paciente=paciente
    )


@app.route("/paciente")
def paciente():
    if "paciente_id" not in session:
        return redirect(url_for("login"))

    nome = session.get("paciente_nome")

    return render_template(
        "paciente.html",
        nome=nome
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/editar-dados", methods=["GET", "POST"])
def editar_dados():

    if "paciente_id" not in session:
        return redirect(url_for("login"))

    paciente_id = session["paciente_id"]

    cursor = conexao.cursor(dictionary=True)

    if request.method == "POST":

        nome = request.form["nome"]
        telefone = request.form["telefone"]
        data_nascimento = request.form["data_nascimento"]

        comando = """
        UPDATE pacientes
        SET nome = %s,
            telefone = %s,
            data_nascimento = %s
        WHERE id = %s
        """

        valores = (
            nome,
            telefone,
            data_nascimento,
            paciente_id
        )

        cursor.execute(comando, valores)
        conexao.commit()

        session["paciente_nome"] = nome

        cursor.close()

        return redirect(url_for("dados"))

    comando = """
    SELECT *
    FROM pacientes
    WHERE id = %s
    """

    cursor.execute(comando, (paciente_id,))
    paciente = cursor.fetchone()

    cursor.close()

    return render_template(
        "editar_dados.html",
        paciente=paciente
    )

if __name__ == "__main__":
    app.run(debug=True)
