from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username= StringField('nome de usuario', validators=[DataRequired(), ])
    email= StringField('email', validators=[DataRequired(), Email()])
    senha=PasswordField('senha', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha=PasswordField('confirmação de senha',validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta=SubmitField('criar conta')

    #essa função tem q começar com validate_ para quando rodar o programa ela fazer a verificação automatica com o validade_on_submit
    def validate_email(self, email):
        usuario= Usuario.query.filter_by(email= email.data).first()
        if usuario:
            raise ValidationError('O e-mail já foi cadastrado, utilize outro e-mail ou faça login para continuar!!!')



class FormLogin(FlaskForm):
    email= StringField('email', validators=[DataRequired(), Email()])
    senha=PasswordField('senha', validators=[DataRequired(), Length(6,20)])
    lembrar_dados = BooleanField('lembrar dados')
    botao_submit_login=SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username= StringField('nome de usuario', validators=[DataRequired()])
    email= StringField('email', validators=[DataRequired(), Email()])
    fotoperfil= FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg','png'])])
    curso_excel = BooleanField('Excel impressionador')
    curso_vba = BooleanField('Vba impressionador')
    curso_powerbi = BooleanField('Power bi impressionador')
    curso_python = BooleanField('Python impressionador')
    curso_ppt = BooleanField('Apresentação impressionadoras')
    curso_saq = BooleanField('sql impressionador')
    botao_submit_editarperfil=SubmitField('Confirmar edição')

    def validate_editarperfil(self, email):
        if current_user.email != email.data:
            usuario= Usuario.query.filter_by(email= email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuario com esse e-mail, cadastre outro e-mail!!!')

class FormCrairPost(FlaskForm):
    titulo= StringField('Titulo do post', validators=[DataRequired(), Length(2,140)])
    corpo= TextAreaField('Escreva seu post aqui!', validators=[DataRequired()])
    botao_submit_post=SubmitField('Confirmar post')
