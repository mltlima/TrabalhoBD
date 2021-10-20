from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from . import connection
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    with connection.cursor() as cursor:
        query_args = []
        query_extra = ""
        if request.args.get("search"):
            query_extra = """
                WHERE LOWER(`nome`) LIKE LOWER(%s)
            """
            search = "%{}%".format(request.args["search"])
            query_args = [search]
        sql = """
            SELECT
                `escola`.*,
                `endereço`.`distrito` as distrito
            FROM `escola`
            INNER JOIN `endereço` ON `escola`.`fk_cep` = `endereço`.`cep`
            {}
            ORDER BY `nome` ASC
            """.format(query_extra)
        cursor.execute(sql, query_args)
        result = cursor.fetchall()  

    return render_template("home.html", escola=result, search=request.args.get("search"), user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/escola")
def escola():
    with connection.cursor() as cursor:
        query_args = []
        query_extra = ""
        if request.args.get("search"):
            query_extra = """
                WHERE LOWER(`nome`) LIKE LOWER(%s)
            """
            search = "%{}%".format(request.args["search"])
            query_args = [search]
        sql = """
            SELECT
                `escola`.*,
                `Telefone`.`Telefone` as telefone
            FROM `escola`
            INNER JOIN `telefone` ON `escola`.`Código` = `telefone`.`fk_Escola_Código`
            {}
            ORDER BY `nome` ASC
            """.format(query_extra)
        cursor.execute(sql, query_args)
        result = cursor.fetchall()
    return render_template("escola.html", escola=result, search=request.args.get("search"), user=current_user)


@views.route("/endereco")
def endereco():
    with connection.cursor() as cursor:
        query_args = []
        query_extra = ""
        if request.args.get("search"):
            query_extra = """
                WHERE LOWER(`nome`) LIKE LOWER(%s)
            """
            search = "%{}%".format(request.args["search"])
            query_args = [search]
        sql = """
            SELECT
                `escola`.*,
                `endereço`.*
            FROM `escola`
            INNER JOIN `endereço` ON `escola`.`fk_cep` = `endereço`.`cep`
            {}
            ORDER BY `nome` ASC
            """.format(query_extra)
        cursor.execute(sql, query_args)
        result = cursor.fetchall()
    return render_template("endereco.html", endereco=result, search=request.args.get("search"), user=current_user)


@views.route("/recurso")
def recurso():
    with connection.cursor() as cursor:
        query_args = []
        query_extra = ""
        if request.args.get("search"):
            query_extra = """
                WHERE LOWER(`nome`) LIKE LOWER(%s)
            """
            search = "%{}%".format(request.args["search"])
            query_args = [search]
        sql = """
            SELECT
                `escola`.`nome` as `NomeEscola`,
                `Recurso`.*
            FROM `escola`
            INNER JOIN `Escola_Recurso` ON `Escola_Recurso`.`fk_Escola_Código` = `escola`.`código`
            INNER JOIN `Recurso` ON `Recurso`.`ID` = `Escola_Recurso`.`fk_Recurso_ID`
            {}
            ORDER BY `NomeEscola` ASC
            """.format(query_extra)
        cursor.execute(sql, query_args)
        result = cursor.fetchall()
    return render_template("recurso.html", recurso=result, search=request.args.get("search"), user=current_user)