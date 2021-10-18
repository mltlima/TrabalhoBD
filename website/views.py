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
                `endereço`.`distrito` as distrito
            FROM `escola`
            INNER JOIN `endereço` ON `escola`.`fk_cep` = `endereço`.`cep`
            {}
            ORDER BY `nome` ASC
            """.format(query_extra)
        cursor.execute(sql, query_args)
        result = cursor.fetchall()
    return render_template("escola.html", escola=result, search=request.args.get("search"), user=current_user)