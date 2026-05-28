from app import db

class Versiculo(db.Model):
    id_v = db.Column(db.Integer, primary_key=True)
    data_inclusao= db.Column(db.DateTime, nullable=False, default=db.func.now())
    texto = db.Column(db.Text)
    referencia = db.Column(db.String(40))
    tema = db.Column(db.String(50))


class FavoritarVersiculo(db.Model):
    id_fav = db.Column(db.Integer, primary_key=True, nullable=False)
    id_v = db.Column(db.Integer, nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)


class Usuarios(db.Model):
    id_u = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(50), nullable=False)


class StatusOracao(db.Model):
    id_status = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    
class CategoriaOracao(db.Model):
    id_cat = db.Column(db.Integer, primary_key=True, nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    
    
class Oracoes(db.Model):
    id_oracao = db.Column(db.Integer, primary_key=True, nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_desafio = db.Column(db.Integer, nullable=True, default=0)
    data_inicio = db.Column(db.DateTime, nullable=False, default=db.func.now())
    data_termino = db.Column(db.DateTime, nullable=True)
    id_categoria = db.Column(db.Integer, nullable=False)
    id_status = db.Column(db.Integer, nullable=False)
    objetivo = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    privacidade = db.Column(db.String(20), nullable=False)
    

class Frases(db.Model):
    id_frase = db.Column(db.Integer, primary_key=True, nullable=False)
    frase = db.Column(db.Text, nullable=False)
    

class Desafios(db.Model):
    id_desafio = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    
    
class ProgressoDesafio(db.Model):
    id_pd = db.Column(db.Integer, primary_key=True, nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    id_desafio = db.Column(db.Integer, nullable=False)
    concluido = db.Column(db.String(20), nullable=False, default=False)
    feedback = db.Column(db.String(50), nullable=True)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    

class Streak(db.Model):
    id_streak = db.Column(db.Integer, primary_key=True, nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    streak = db.Column(db.Integer, nullable=False, default=0)
    ultimo_dia = db.Column(db.DateTime, nullable=True)
    
    
class AberturaIA(db.Model):
    id_abertura = db.Column(db.Integer, primary_key=True, nullable=False)
    abertura = db.Column(db.String(100), nullable=False, unique=True)
    tipo = db.Column(db.String(30), nullable=False)
    
    
class PedidosIA(db.Model):
    id_pedidos = db.Column(db.Integer, primary_key=True, nullable=False)
    pedidos = db.Column(db.String(200), nullable=False, unique=True)
    tipo = db.Column(db.String(30), nullable=True)
    

class FinaisIA(db.Model):
    id_final = db.Column(db.Integer, primary_key=True, nullable=False)
    final = db.Column(db.String(200), nullable=False, unique=True)
    tipo = db.Column(db.String(30), nullable=True)
    
    
class Anotacoes(db.Model):
    id_anotacao = db.Column(db.Integer, primary_key=True, nullable=False)
    id_usuario = db.Column(db.Integer, nullable=False)
    referencia = db.Column(db.String(80), nullable=False, default='Sem Referência')
    titulo = db.Column(db.String(80), nullable=False, default='Sem Tìtulo')
    anotacao = db.Column(db.Text)
    cor_escolhida = db.Column(db.Text)
    cor_escolhida_lyrics = db.Column(db.String(20), default='#000000')
    data_anotacao = db.Column(db.Date)
    visibilidade = db.Column(db.Integer, default=1)
    

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    sigla = db.Column(db.String(10))
    capitulos = db.relationship("Capitulo", backref="livro")

class Capitulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer)
    livro_id = db.Column(db.Integer, db.ForeignKey("livro.id"))
    versiculos = db.relationship("Versiculos", backref="capitulo")

class Versiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_vers = db.Column(db.Integer)
    texto = db.Column(db.Text)
    capitulo_id = db.Column(db.Integer, db.ForeignKey("capitulo.id"))
    

class Devocionais(db.Model):
    id_devocional  = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    referencia = db.Column(db.String(50))   
    data = db.Column(db.Date)
    
class Backgrounds(db.Model):
    id_img = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    
class RegristroOracao(db.Model):
    id_registro = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    data_oracao = db.Column(db.Date)
    duracao = db.Column(db.String(50))