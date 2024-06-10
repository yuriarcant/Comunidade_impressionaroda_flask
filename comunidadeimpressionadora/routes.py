from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil,FormCrairPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image




@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template("contato.html")


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios= Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios= lista_usuarios)

@app.route('/login', methods=['get', 'post'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario= Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            parametro_next= request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'falha no login, e-mail ou senha incorretos', 'alert-danger')
    
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_criptografada= bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criarconta.username.data, email= form_criarconta.email.data, senha=senha_criptografada)
        database.session.add(usuario)
        database.session.commit()
        flash(f'conta criada com sucesso com o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login= form_login, form_criarconta=form_criarconta )



@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'logout feito com sucesso','alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['get', 'post'])
@login_required
def criar_post():
    form = FormCrairPost()
    if form.validate_on_submit():
        post = Post(titulo= form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(f'Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)



def salvar_imagem(imagem):
    #adicionar cod na imagem
    codigo= secrets.token_hex(8)
    #separando nome da extensao
    nome, extensao= os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    #reduzir a imagem
    tamanho= (400,400)
    imagem_reduzida= Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    #salvar a imagem
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_dados(form):
    lista_curso =[]
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_curso.append(campo.label.text) 
    return ";".join(lista_curso)

@app.route('/perfil/editar', methods=['get', 'post'])
@login_required
def editar_perfil():
    form= FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username= form.username.data
        if form.fotoperfil.data:
            nome_imagem= salvar_imagem(form.fotoperfil.data)
            current_user.foto_perfil= nome_imagem
        current_user.cursos= atualizar_dados(form)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)  


@app.route('/post/<post_id>', methods=['get', 'post'])
@login_required
def exibir_post(post_id):
    post= Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCrairPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form= None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['get', 'post'])
@login_required
def excluir_post(post_id):
    post= Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com sucesso', 'alert-success')
        return redirect(url_for('home'))
    else:
        abort(403)
