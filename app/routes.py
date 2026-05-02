from app import app, db
from flask import Response, render_template, url_for, request, jsonify, redirect, session
from app import func
from app.func import validar_cpf
from app.models import CategoriaOracao, Desafios, Oracoes, ProgressoDesafio, Versiculo, FavoritarVersiculo, Usuarios, StatusOracao, Frases, Streak, AberturaIA, PedidosIA, FinaisIA, Anotacoes, Livro, Capitulo, Versiculos
from datetime import date, datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_, text
import asyncio
import edge_tts
import os
import random


context = {
    'title_site': 'VOX BÍBLIA',
    'slogan_site': 'Conectado ao Supremo',
    'version': 'v1.0.0',
    'author': 'Isaac Rocha',
    'email': 'prog.isaac13@gmail.com',
}

@app.route('/api/favoritar', methods=['POST'])
def favoritar_versiculo():
    if 'id_usuario' in session:
        data = request.get_json()

        id_usuario = data['id_usuario']
        id_v = data['id_v']

        existe = FavoritarVersiculo.query.filter_by(
            id_usuario=id_usuario,
            id_v=id_v
        ).first()

        if existe:
            # Remover Toogle
            db.session.delete(existe)
            db.session.commit()
            return jsonify({"status": 'removido'})
        else:
            novo = FavoritarVersiculo(
                id_usuario=id_usuario,
                id_v=id_v,
                data_hora=datetime.now(),
            )
            db.session.add(novo)
            db.session.commit()
            return jsonify({"status": 'adicionado'})
    else:
        return jsonify({"status": 'Não Logado!'})


@app.route('/api/cadastrar', methods=['POST'])
def cadastrarUsuario():

    data = request.get_json()

    nome = data['nome'].capitalize()
    email = data['email']
    cpf = data['cpf']
    senha = data['senha']

    existe_cpf = Usuarios.query.filter_by(
        cpf=cpf
    ).first()

    if not existe_cpf:
        existe_email = Usuarios.query.filter_by(
            email=email
        ).first()
        if not existe_email:
            if func.validar_cpf(cpf):
                email_verificado = func.validar_email(email)
                if email_verificado != "Formato Incopátivel":
                    usuario = Usuarios(
                        nome = nome,
                        email = email,
                        cpf = cpf,
                        senha = generate_password_hash(senha)
                    )
                    db.session.add(usuario)
                    db.session.commit()
                    return jsonify({"status": 'adicionado'})
                else:
                    return jsonify({"status": 'Email Inválido'})
            else:
                return jsonify({"status": 'CPF Não Válido'})
        else:
            return jsonify({"status": 'existe'})
    else:
        return jsonify({"status": 'existe'})


@app.route('/api/logar', methods=['POST'])
def logar():
    data = request.get_json()

    email = data['email']
    senha = data['senha']

    usuario = Usuarios.query.filter_by(
        email=email
    ).first()
    if usuario and check_password_hash(usuario.senha, senha):
        session['id_usuario'] = usuario.id_u
        session['nome_usuario'] = usuario.nome
        
        streak_usuario = Streak.query.filter_by(id_usuario=session['id_usuario']).first()
        
        if not streak_usuario:
            novo_streak = Streak(
                id_usuario=session['id_usuario'],
                streak=0,
                ultimo_dia=None
            )
            
            db.session.add(novo_streak)
            db.session.commit()
        
        return jsonify({"status": 'Logado'})
    else:
        usuario_cpf = Usuarios.query.filter_by(
            cpf=email
        ).first()
        if usuario_cpf and check_password_hash(usuario_cpf.senha, senha):
            session['id_usuario'] = usuario_cpf.id_u
            session['nome_usuario'] = usuario_cpf.nome
            
            streak_usuario = Streak.query.filter_by(id_usuario=session['id_usuario']).first()
            
            if not streak_usuario:
                novo_streak = Streak(
                    id_usuario=session['id_usuario'],
                    streak=0,
                    ultimo_dia=None
                )
                
                db.session.add(novo_streak)
                db.session.commit() 
            
            return jsonify({"status": 'Logado'})
        else:
            return jsonify({"status": 'Inválidos'})


@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    session.pop('nome_usuario', None)
    return redirect(url_for('index'))


@app.route('/api/criar_oracao', methods=['POST'])
def salvar_oracao():
    if 'id_usuario' in session:
        data = request.get_json()
        action = data['action'];
        if action == 'criar':
            objetivo = data['objetivo']
            descricao = data['descricao']
            id_categoria = data['id_categoria']
            id_status = data['id_status']
            privacidade = data['privacidade']
            data_termino = data['data_termino']
            
            nova_oracao = Oracoes(
                id_usuario=session['id_usuario'],
                objetivo=objetivo,
                descricao=descricao,
                id_categoria=id_categoria,
                id_status=id_status,
                privacidade=privacidade,
                data_termino=datetime.strptime(data_termino, '%Y-%m-%d') if data_termino else None
            )
            db.session.add(nova_oracao)
            db.session.commit()
            return jsonify({"status": 'Oração Criada'})
        else:
            oracao = Oracoes.query.filter_by(id_oracao=data['id_oracao']).first();

            oracao.descricao = data['descricao']
                
            if oracao.id_categoria != data['id_categoria'] and data['id_categoria'] != "": 
                oracao.id_categoria = data['id_categoria']
                
            if oracao.id_status != data['id_status'] and data['id_status'] != "":
                oracao.id_status = data['id_status']
            
            if oracao.privacidade != data['privacidade'] and data['privacidade'] != "":
                oracao.privacidade = data['privacidade']
            
            db.session.commit()
            
            return jsonify({'status': 'Oração Criada'})
    else:
        return jsonify({"status": 'Não Logado!'})



# Função para a exclusão de uma determinada oração
@app.route('/api/oracoes/excluir', methods=["POST"])
def excluir_oracao():
    data = request.get_json();
    
    oracao = Oracoes.query.filter_by(id_oracao=data['id']).first()
    
    id_usuario = oracao.id_usuario
    
    if id_usuario == session['id_usuario']:
        db.session.delete(oracao)
        db.session.commit()
        return jsonify({'status': 'Oração Excluída com Sucesso!'})
    else:
        return jsonify({'status': 'Só o usuário titular pode fazer a exclusão!'})
    
    
# Função para a pegar os dados a serem editados
@app.route('/api/pegar_dados_oracao', methods=['POST'])
def editar_dados():
    data = request.get_json()
    
    oracao = Oracoes.query.filter_by(id_oracao=data['id_oracao']).first()
    
    if oracao.id_usuario == session['id_usuario']:
        return jsonify({'objetivo': oracao.objetivo, 'descricao': oracao.descricao})
        
# Rota para a Chamada de Ação da Sessão Desafio do Dia
@app.route('/api/frasedodia')
def fraseDia():
    frases = Frases.query.all()
    
    print(frases)
    
    hoje = date.today().toordinal()
    index = hoje % len(frases)
    
    frase = frases[index]
    
    return jsonify({'texto': frase.frase})

# Rota para a Chamada de Ação da Sessão Desafio do Dia
@app.route('/api/desafiodia')
def desafioDia():
    if 'id_usuario' in session:
        desafios = Desafios.query.all()
        
        hoje = date.today().toordinal()
        index = hoje % len(desafios)
        
        desafio = desafios[index]
        
        desafio_concluido = ProgressoDesafio.query.filter_by(id_usuario=session['id_usuario'], id_desafio=desafio.id_desafio).first()
        
        if desafio_concluido:
            return jsonify({'titulo': desafio.titulo, 'descricao': desafio.descricao, 'id_desafio': desafio.id_desafio, 'concluido': True, 'feedback': desafio_concluido.feedback})
        else:
            return jsonify({'titulo': desafio.titulo, 'descricao': desafio.descricao, 'id_desafio': desafio.id_desafio, 'concluido': False, 'feedback': None})
    else :
        return jsonify({'titulo': "Não Logado!", 'descricao': "Login para visualizar o desafio do dia.", 'id_desafio': None, 'concluido': False, 'feedback': None})
    
            
# Rota para a Chamada de Ação da Sessão Desafio do Dia - Conclusão do Desafio
@app.route('/api/concluir_desafio', methods=['POST'])
def concluir_desafio():
    if 'id_usuario' in session:
        data = request.get_json();
        
        id_usuario = session['id_usuario'];
        id_desafio = data['id_desafio'];
        
        desafio = ProgressoDesafio.query.filter_by(id_usuario=id_usuario, id_desafio=id_desafio).first();
        if desafio:
            return jsonify({'status': 'Não é possível concluir o mesmo desafio mais de uma vez!'})
        else:
            novo_desafio = ProgressoDesafio(
                id_usuario=id_usuario,
                id_desafio=id_desafio,
                concluido='Concluído',
                feedback='',
                data_conclusao=datetime.now()
            )
            streak()
            db.session.add(novo_desafio)
            db.session.commit()
            return jsonify({'status': 'concluido'})


# Rota para a Chamada de Ação da Sessão Desafio do Dia - Feedback do Desafio
@app.route('/api/feedback_desafio', methods=['POST'])
def feedback():
    data = request.get_json();
    id_usuario = data['id_usuario'];
    id_desafio = data['id_desafio'];
    feedback = data['feedback'];
    
    desafio = ProgressoDesafio.query.filter_by(id_usuario=id_usuario, id_desafio=id_desafio).first()
    
    
    if desafio:
        if feedback == 'Não gostou' and desafio.feedback == 'Não gostou':
            feedback = 'Sem Respotas'
            retorno = {'status': 'Feedback Removido'}
            
        if feedback == 'Gostou' and desafio.feedback == 'Gostou':
            feedback = 'Sem Respotas'
            retorno = {'status': 'Feedback Removido'}
            
        if feedback == 'Gostou' and (desafio.feedback == 'Não gostou' or desafio.feedback == 'Sem Respotas'):
            retorno = {'status': 'Gostou'}
        if feedback == 'Não gostou' and (desafio.feedback == 'Gostou' or desafio.feedback == 'Sem Respotas'):
            retorno = {'status': 'Não gostou'}
        desafio.feedback = feedback
        db.session.commit()
        return jsonify(retorno)
    else:
        return jsonify({'status': 'Desafio não encontrado para enviar feedback!'})


def streak():
    if 'id_usuario' in session:
        streak_atual = Streak.query.filter_by(id_usuario=session['id_usuario']).first()
        if streak_atual:
            hoje = date.today()
            
            if streak_atual.ultimo_dia is None:
                # Primeiro dia registrando o streak
                streak_atual.streak = 1
                streak_atual.ultimo_dia = hoje
                db.session.commit()
            elif streak_atual.ultimo_dia == hoje - timedelta(days=1):
                # Fez ontem - Conta Normal
                streak_atual.streak += 1
                streak_atual.ultimo_dia = hoje
                db.session.commit()
            elif streak_atual.ultimo_dia == hoje:
                pass # Já registrou hoje, não faz nada
            
            else:
                # Perdeu o streak
                streak_atual.streak = 1
                streak_atual.ultimo_dia = hoje
                db.session.commit()
                
                
@app.route('/api/streak')
def pegar_streak():
    print(session)
    if 'id_usuario' in session:
        streak = Streak.query.filter_by(id_usuario=session['id_usuario']).first()
        if streak:
            return jsonify({'streak': streak.streak})
        else:
            return jsonify({'streak': 0})
    else:
        return jsonify({'streak': 0})
    

@app.route('/api/oracao_personalizada')
def oracao_personalizada():
    if 'id_usuario' in session:
        aberturaIA = AberturaIA.query.order_by(db.func.rand()).first()
        pedidoIA = PedidosIA.query.order_by(db.func.rand()).first()
        final_ia = FinaisIA.query.order_by(db.func.rand()).first()
        
        tipo_pedido = pedidoIA.tipo.capitalize()
        
        categorias = CategoriaOracao.query.filter_by(categoria=tipo_pedido).first()
        
        if not categorias:
            nova_categoria = CategoriaOracao(categoria=tipo_pedido)
            db.session.add(nova_categoria)
            db.session.commit()
        
        categorias = CategoriaOracao.query.filter_by(categoria=tipo_pedido).first()
        
        id_categoria = categorias.id_cat
        
        descricao = aberturaIA.abertura + ' ' + pedidoIA.pedidos + '. ' + final_ia.final 
        
        if tipo_pedido == 'Fé':
            objetivo = 'Fortalecer a Fé Para Me Alcançar o Impossível'
        elif tipo_pedido == 'Cura':
            objetivo = 'Alcançar a Cura Para Mim ou Para Alguém que Amo'
        elif tipo_pedido == 'Proteção':
            objetivo = 'Alcançar a Proteção Divina para todos os meus não se perderem do Caminho do Senhor'
        elif tipo_pedido == 'Gratidão':
            objetivo = 'Agradecer a Deus por ter me tirado de onde ninguém sabia que eu estava e me colocado onde eu sempre sonhei em estar'
        elif tipo_pedido == 'Sabedoria':
            objetivo = 'Alcançar a Sabedoria Divina para tomar as melhores decisões e ser luz onde quer que eu vá'
        elif tipo_pedido == 'Paz':
            objetivo = 'Alcançar a Paz que excede todo entendimento para acalmar meu coração e minha mente em meio às tempestades da vida'
        elif tipo_pedido == 'Perdão':
            objetivo = 'Alcançar o Perdão Divino para me libertar do peso da culpa e viver plenamente a graça de Deus'
        elif tipo_pedido == 'Força':
            objetivo = 'Alcançar a Força Divina para superar os desafios da vida e me tornar uma pessoa melhor a cada dia'
        elif tipo_pedido == 'Prosperidade':
            objetivo = 'Alcançar a Prosperidade Divina para ser uma bênção na vida das pessoas ao meu redor e honrar a Deus com tudo o que tenho'
        elif tipo_pedido == 'Libertação':
            objetivo = 'Alcançar a Libertação Divina para me livrar de tudo o que me prende e viver a vida abundante que Deus planejou para mim'
        elif tipo_pedido == 'Proposito':
            objetivo = 'Descobrir a Vontade de Deus para a minha vida que é Boa, Perfeita e Agradável e me entregar completamente a Ela'
        elif tipo_pedido == 'Amor':
            objetivo = 'Alcançar o Amor Divino para amar a mim mesmo e aos outros como Deus nos ama, incondicionalmente e eternamente'
        elif tipo_pedido == 'Disciplina':
            objetivo = 'Alcançar a Disciplina Divina para me manter firme no caminho do bem e da verdade, mesmo quando as tentações e dificuldades surgirem'
        else:
            objetivo = 'Alcançar a Benção Divina para transformar minha vida e ser um instrumento de amor e luz no mundo'
        
        if '?' in descricao:
            descricao = descricao.replace('?', '')        
        
        return jsonify({'status': 'Oração Criada!', "objetivo": objetivo, "descricao": descricao, "categoria": categorias.id_cat})
    else:
        return jsonify({"status": 'Não Logado!'})
        

@app.route('/api/salvar_oracao_personalizada', methods=['POST'])
def oracao_custom():
    if 'id_usuario' in session:
        data = request.get_json();
        
        id_usuario = session['id_usuario'];
        objetivo = data['objetivo'];
        descricao = data['descricao'];
        id_categoria = data['id_categoria'];
        privacidade = data['privacidade'];
        data_termino = data['data_termino'];
        status = data['status'];
        
        if data_termino == None or data_termino == "":
            return jsonify({'status': 'Data de término é obrigatória para orações!'})
        
        nova_oracao = Oracoes(
            id_usuario=id_usuario,
            id_desafio=0,
            objetivo=objetivo,
            descricao=descricao,
            id_categoria=id_categoria,
            id_status=status,
            privacidade=privacidade,
            data_termino=datetime.strptime(data_termino, '%Y-%m-%d') if data_termino else None
        )
        db.session.add(nova_oracao)
        db.session.commit()
        return jsonify({'status': 'Oração Criada!'})
    else:
        return jsonify({"status": 'Não Logado!'})


# Rota para Salvar a Anotação do Usuário
@app.route('/api/anotacao', methods=['POST'])
def anotacao_salvar():
    if 'id_usuario' in session:
        data = request.get_json()
        
        id_usuario = session['id_usuario']
        referencia = data['referencia']
        titulo = data['titulo']
        cor_escolhida = data['cor_escolhida']
        anotacao = data['anotacao']
        
        hoje = date.today();
        
        
        if (cor_escolhida == '#2C2C54') or (cor_escolhida == '#1B4332') or (cor_escolhida == '#3C096C') or (cor_escolhida == '#343A40'):
            cor_escolhida_lyrics = '#ffffff'
        else:
            cor_escolhida_lyrics = '#000000'
        
        nova_anotacao = Anotacoes(
            id_usuario = id_usuario,
            referencia = referencia,
            titulo = titulo,
            anotacao = anotacao,
            cor_escolhida = cor_escolhida,
            cor_escolhida_lyrics = cor_escolhida_lyrics,
            data_anotacao = hoje       
        )
        
        db.session.add(nova_anotacao)
        db.session.commit()
        return jsonify({'status': 'Salvo!'})
    else:
        return jsonify({'status': 'Não Logado!'})
    
    
@app.route('/api/anotacoes', methods=['POST', 'GET'])
def get_notes():
    if 'id_usuario' in session:
        page = request.args.get("page", 1, type=int)
        antiguidade = request.args.get('order')
        search = request.args.get('search').strip()
        

        notes = Anotacoes.query.filter_by(id_usuario=session['id_usuario']).first()

        dados = []
        if notes:
            print(search)
            if search == '':
                if antiguidade == "asc":
                    anotacoes = Anotacoes.query\
                    .filter_by(id_usuario=session['id_usuario'])\
                    .order_by(Anotacoes.id_anotacao.asc())\
                    .paginate(page=page, per_page=6)
                elif antiguidade == "desc":
                    anotacoes = Anotacoes.query\
                    .filter_by(id_usuario=session['id_usuario'])\
                    .order_by(Anotacoes.id_anotacao.desc())\
                    .paginate(page=page, per_page=6)
            else:
                search = f"%{search}%"
                anotacoes = Anotacoes.query\
                .filter_by(id_usuario=session['id_usuario'])\
                .filter(
                    or_(
                        Anotacoes.titulo.like(search),
                        Anotacoes.anotacao.like(search)
                    )
                ).all()
        
            for a in anotacoes:
                dados.append({
                    "id_anotacao": a.id_anotacao,
                    "titulo": a.titulo,
                    "referencia": a.referencia,
                    "anotacao": a.anotacao[:250] + '...' if len(a.anotacao) > 250 else a.anotacao,
                    'cor_escolhida': a.cor_escolhida,
                    'cor_escolhida_lyrics': a.cor_escolhida_lyrics,
                    'data_anotacao': a.data_anotacao.strftime("%d/%m/%Y")
                })
                
            if search == '':
                return {
                    "anotacoes": dados,
                    "has_next": anotacoes.has_next,
                    "next_page": anotacoes.next_num
                }
            else:
                return {
                    "anotacoes": dados,
                }
        else:
            dados.append({
                "id_anotacao": 0,
                'titulo': 'Suas Anotações aparecerão Aqui!',
                'referencia': 'Crie uma anotação e teste!',
                'anotacao': 'Deus falou com você? Precisa anotar uma coisa importante? Anote aqui.',
                'cor_escolhida': '#F8BBD0',
                'data_anotacao': '0000-00-00'
            })
            
            return {
                'anotacoes': dados
            }
    else:
        dados = []
        dados.append({
            "id_anotacao": 0,
            'titulo': 'Faça login para criar anotaações!',
            'referencia': 'Crie uma anotação e teste!',
            'anotacao': 'Deus falou com você? Precisa anotar uma coisa importante? Anote aqui.',
            'cor_escolhida': '#F8BBD0',
            'data_anotacao': '0000-00-00'
        })
        
        return {
            'anotacoes': dados
        }
            
            
@app.route('/api/open_notes', methods=['POST'])
def open_note():
    if 'id_usuario' in session:
        data = request.get_json()

        id_anotacao = data['id_anotacao']

        anotacao = Anotacoes.query.filter_by(id_anotacao=id_anotacao).first()
        
        dados = []
        dados.append({
            'id_anotacao': anotacao.id_anotacao,
            'titulo': anotacao.titulo,
            'referencia': anotacao.referencia,
            'anotacao': anotacao.anotacao,
            'cor_escolhida': anotacao.cor_escolhida,
            'cor_escolhida_lyrics': anotacao.cor_escolhida_lyrics,
            'data_anotacao': anotacao.data_anotacao.strftime("%d/%m/%Y"),
            'visibilidade': anotacao.visibilidade
        })
    
        return jsonify({'status': 'tudo certo!', 'dados': dados})
    

@app.route('/api/note-visibilidade', methods=['POST'])
def visibilidade():
    if 'id_usuario' in session:
        data = request.get_json()
        
        id_anotacao = data['id_anotacao']
        
        anotacao = Anotacoes.query.filter_by(id_anotacao=id_anotacao).first()
        
        if anotacao.visibilidade == 1:
            anotacao.visibilidade = 0
            db.session.commit()
            return jsonify({'status': 0})
        else:
            if anotacao.visibilidade == 0:
                anotacao.visibilidade = 1
                db.session.commit()
                return jsonify({'status': 1})
            return jsonify({'status': 'Visibilidade já desabilitada'}) 
           
    
@app.route('/api/note-del', methods=['POST'])
def note_del():
    if 'id_usuario' in session:
        data = request.get_json();
        
        id_anotacao = data['id_anotacao']
        
        anotacao = Anotacoes.query.filter_by(id_anotacao=id_anotacao).first();
        
        if anotacao:
            db.session.delete(anotacao)
            db.session.commit()
            return jsonify({'status': 'Exclusão'})
        else:
            return jsonify({'status': 'Anotação Já Excluída'})
    
    
@app.route('/api/editar_nota', methods=['POST'])
def editar_nota():
    if 'id_usuario' in session:
        data = request.get_json()
        id_anotacao = data['id_anotacao']
        
        titulo = data['titulo']
        referencia = data['referencia']
        anotacao = data['anotacao']
        
        anotacoes = Anotacoes.query.filter_by(id_anotacao=id_anotacao).first()
        
        if anotacoes:
            anotacoes.titulo = titulo
            anotacoes.referencia = referencia
            anotacoes.anotacao = anotacao
            db.session.commit()
            return jsonify({'status': 'Editado!'})
        else:
            return jsonify({'status': 'Não foi Possível fazer a Edição!'})
    else:
        return jsonify({'status': 'Não Logado!'})


@app.route('/api/editNote_colors', methods=['POST'])
def bgNote():
    if 'id_usuario' in session:
        data = request.get_json()
        
        id_anotacao = data['id_anotacao']
        color = data['cor_escolhida']
        tipo = data['tipo']
        
        anotacoes = Anotacoes.query.filter_by(id_anotacao=id_anotacao).first()
        print(tipo)
        
        if anotacoes:
            if tipo == 'bg':
                anotacoes.cor_escolhida = color
                db.session.commit()
            else:
                anotacoes.cor_escolhida_lyrics = color
                db.session.commit()
            return jsonify(['OK'])
        
        
@app.route("/api/devocional")
def get_devocionar():
    if 'id_usuario' in session:
        # sql_versiculos = text("SELECT * FROM versiculos limit 2;")
        # versiculo = db.session.execute(sql_versiculos).fetchone()
        # capitulo_id = versiculo.capitulo_id
        
        
        # sql_capitulos = text(f"SELECT * FROM capitulo WHERE id = '{capitulo_id}'")
        # capitulo = db.session.execute(sql_capitulos).fetchone()
        # livro_id = capitulo.livro_id
        
        # sql_livro = text(f"SELECT * FROM livro WHERE id = '{livro_id}'")
        # livro = db.session.execute(sql_livro).fetchone()
        
        # dados.append({
        #     'nome_livro': livro.nome,
        #     'sigla': livro.sigla,
        #     'capitulo': capitulo.numero,
        #     'versiculo': versiculo.numero_vers,
        #     'text': versiculo.texto
        # })
        dados = []
        
        
        sql_capitulo = text(f"SELECT c.id, c.numero AS capitulo, l.nome AS livro FROM capitulo c JOIN livro l ON c.livro_id = l.id WHERE l.nome = 'Provérbios' AND c.numero = 31 ORDER BY RAND() LIMIT 1")
        capitulo = db.session.execute(sql_capitulo).fetchone()
        
        sql_quant = text(f"SELECT * FROM versiculos WHERE capitulo_id = {capitulo.id} order by numero_vers desc limit 1")
        total = db.session.execute(sql_quant).fetchone()
        qtd = random.randint(3, 8)
        inicio = random.randint(1, total.numero_vers - qtd)
        fim = inicio + qtd - 1
        
        sql_versiculo = text(f"SELECT numero_vers, texto FROM versiculos WHERE capitulo_id = :cap_id AND numero_vers BETWEEN :inicio AND :fim ORDER BY numero_vers")
        versiculos = db.session.execute(sql_versiculo, {
            "cap_id": capitulo.id,
            "inicio": inicio,
            "fim": fim
        }).fetchall()
        
        textos = []
        numeros_vers = []
        for linha in versiculos:
            textos.append(f'{linha.numero_vers}. {linha.texto}')
            numeros_vers.append(f'{linha.numero_vers}')
        
        dados.append({
            'nome_livro': capitulo.livro,
            'capitulo': capitulo.capitulo,
            'text': textos,
            'versiculos_inicio': numeros_vers[0],
            'versiculos_fim': numeros_vers[-1]
        })        
        
        return jsonify({'status': 1, 'source': dados})
        
    
@app.route('/api/carregar_livros')
def livros():
    if 'id_usuario' in session:
        nomes = []
        
        sql_livros = text("SELECT * FROM livro;");
        livros = db.session.execute(sql_livros).fetchall();
        
        for n in livros:
            nomes.append({
                'nome': n.nome
            })
            
        return jsonify({'dados': nomes})
    
    
    
# Rotas de Renderização de Páginas
@app.route('/')
def index():  # put application's code here
    # Verificar se o usuário está logado e atualizar o contexto para exibir as informações corretas no template    
    if not 'id_usuario' in session:
        context.update({'Status': 'Não Logado!'})
    else:
        context.update({'Status': 'Logado!'})
    
    context.update({
        'id_usuario': session['id_usuario'] if 'id_usuario' in session else None,
        'nome_usuario': session['nome_usuario'].capitalize() if 'nome_usuario' in session else None,
    })
    
    
    
    # Selecionar um versículo aleatório para exibir na página inicial
    versiculo = Versiculo.query.order_by(db.func.rand()).first()

    favorito = FavoritarVersiculo.query.filter_by(
        id_usuario=session['id_usuario'] if 'id_usuario' in session else None,
        id_v=versiculo.id_v
    ).first()

    favoritos = {
        'icon': 'regular',
        'color': '#f8fafc'
    }
    if favorito:
        favoritos = {
            'icon': 'solid',
            'color': '#FF0000'
        }



    # Verificar os versículos favoritos do usuário logado
    versiculos_favoritos = []
    if 'id_usuario' in session:
        fav = FavoritarVersiculo.query.filter_by(id_usuario=session['id_usuario']).all()
        for item in fav:
            versiculo_fav = Versiculo.query.filter_by(id_v=item.id_v).first()
            if versiculo_fav:
                versiculos_favoritos.append(versiculo_fav)
            if len(versiculos_favoritos) >= 5:
                break
            
    oracoes_usuario = []
    if 'id_usuario' in session:
        oracoes = Oracoes.query.filter_by(id_usuario=session['id_usuario']).all()
        
        for oracao in oracoes:
            status = StatusOracao.query.filter_by(id_status=oracao.id_status).first()
            categoria = CategoriaOracao.query.filter_by(id_cat=oracao.id_categoria).first()
            oracoes_usuario.append({
                'id_oracao': oracao.id_oracao,
                'objetivo': oracao.objetivo[:35] + '...' if len(oracao.objetivo) > 35 else oracao.objetivo,
                'descricao': oracao.descricao[:50] + '...' if len(oracao.descricao) > 50 else oracao.descricao,
                'data_inicio': oracao.data_inicio,
                'data_termino': oracao.data_termino,
                'privacidade': oracao.privacidade,
                'status': status.status if status else None,
                'categoria': categoria.categoria if categoria else None
            })
            if len(oracoes_usuario) >= 3:
                break
            
    status_oracao = []
    status_oracao = StatusOracao.query.all()
    
    # Pega as categorias de oração para a área de oração do Usuário
    categoria_oracao = []
    categoria_oracao = CategoriaOracao.query.all()
    
    # Exibir a página inicial com o versículo selecionado
    return render_template('index.html', context=context, versiculo=versiculo, favoritos=favoritos, versiculos_favoritos=versiculos_favoritos,
    oracoes_usuario=oracoes_usuario, status_oracao=status_oracao, categoria_oracao=categoria_oracao)



@app.route('/devocional')
def devocional():
    if 'id_usuario' in session:
        context.update({'Status': 'Logado!', 'id_usuario': 'btn-usuario', 'class': 'btn-primary me-2', 'text_btn': 'Seja bem vindo(a), ' + session['nome_usuario'] + "!", 'link_usuario': url_for('index'), 'btn_sair-class': 'd-block'})
    
        context.update({
            'id_usuario': session['id_usuario'] if 'id_usuario' in session else None,
            'nome_usuario': session['nome_usuario'] if 'nome_usuario' in session else None,
        })
        return render_template('devocional/index.html', context=context)


@app.route('/notes')
def notes():
    if not 'id_usuario' in session:
        context.update({'Status': 'Não Logado!', 'id_usuario': 'btn-logar', 'class': 'btn-light text-dark me-2', 'text_btn': 'Login/Cadastro', 'link_usuario': url_for('login'), 'btn_sair-class': 'd-none'})
    else:
        context.update({'Status': 'Logado!', 'id_usuario': 'btn-usuario', 'class': 'btn-primary me-2', 'text_btn': 'Seja bem vindo(a), ' + session['nome_usuario'] + "!", 'link_usuario': url_for('index'), 'btn_sair-class': 'd-block'})
    
    context.update({
        'id_usuario': session['id_usuario'] if 'id_usuario' in session else None,
        'nome_usuario': session['nome_usuario'] if 'nome_usuario' in session else None,
    })
    
    return render_template('anotacoes/notas.html', context=context);


@app.route('/oracoes')
def oracoes():
    # Verificar se o usuário está logado e atualizar o contexto para exibir as informações corretas no template    
    if not 'id_usuario' in session:
        context.update({'Status': 'Não Logado!', 'id_usuario': 'btn-logar', 'class': 'btn-light text-dark me-2', 'text_btn': 'Login/Cadastro', 'link_usuario': url_for('login'), 'btn_sair-class': 'd-none'})
    else:
        context.update({'Status': 'Logado!', 'id_usuario': 'btn-usuario', 'class': 'btn-primary me-2', 'text_btn': 'Seja bem vindo(a), ' + session['nome_usuario'] + "!", 'link_usuario': url_for('index'), 'btn_sair-class': 'd-block'})
    
    context.update({
        'id_usuario': session['id_usuario'] if 'id_usuario' in session else None,
        'nome_usuario': session['nome_usuario'] if 'nome_usuario' in session else None,
    })
    
    # Pega os status de oração para a área de oração do Usuário
    status_oracao = []
    status_oracao = StatusOracao.query.all()
    
    # Pega as categorias de oração para a área de oração do Usuário
    categoria_oracao = []
    categoria_oracao = CategoriaOracao.query.all()
    
    # Orações do Usuario
    oracoes = Oracoes.query.filter_by(id_usuario=session['id_usuario']).order_by(Oracoes.id_oracao.desc()).all()
    
    l = []
    
    for linha in oracoes:
        l.append({
            'id_oracao': linha.id_oracao,
            'objetivo': linha.objetivo[:15] + '...' if len(linha.objetivo) > 15 else linha.objetivo,
            'objetivo_title': linha.objetivo, 
            'descricao': linha.descricao[:50] + '...' if len(linha.descricao) > 50 else linha.descricao,
            'descricao_title': linha.descricao,
            'data_inicio': linha.data_inicio,
            'data_termino': linha.data_termino,
            'categoria': CategoriaOracao.query.filter_by(id_cat=linha.id_categoria).first().categoria,
            'status': StatusOracao.query.filter_by(id_status=linha.id_status).first().status,
        })
    
    return render_template('oracao/oracoes.html', context=context, status_oracao=status_oracao, categoria_oracao=categoria_oracao, lista=l)


@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastra.html', context=context)


@app.route('/login')
def login():
    return render_template('login.html', context=context)


@app.route('/versiculos/tema/<string:tema>')
def versiculos_tema(tema):
    versiculos_salvos = []
    class_fav = []
    if tema != 'todos':
        versiculos = Versiculo.query.filter_by(tema=tema).all()
        quantidade_versiculos = Versiculo.query.filter_by(tema=tema).count()
        
        tema = 'para o tema "' + tema + '"'
    else:
        versiculos = Versiculo.query.all()
        quantidade_versiculos = Versiculo.query.count()
        tema = 'para todos os temas'
                
    for versiculo in versiculos:
        favorito = FavoritarVersiculo.query.filter_by(
            id_usuario=session['id_usuario'] if 'id_usuario' in session else None,
            id_v=versiculo.id_v
        ).first()
        if favorito:
            class_fav.append({'icone': 'solid', 'color': '#FF0000', 'id_v': versiculo.id_v})
        else:
            class_fav.append({'icone': 'regular', 'color': '#f8fafc', 'id_v': versiculo.id_v})

    return render_template('versiculos/versiculos_tema.html', context=context, versiculos=versiculos, quantidade_versiculos=quantidade_versiculos,
    tema=tema, class_fav=class_fav)
    
# Rota para a gereção de aúdios em versículos
# @app.route('/tts')
# def tts():
#     texto = request.args.get('texto')
#     nome = request.args.get('nome')
    
#     caminho_arquivo = f'app/static/audio/{nome}.mp3'
    
#     if not os.path.exists(caminho_arquivo):
#         tts = gTTS(text=texto, lang='pt-br')
#         tts.save(caminho_arquivo)
        
#     with open(caminho_arquivo, 'rb') as f:
#         return Response(f.read(), mimetype='audio/mpeg')


async def gerar_audio(texto, nome):
    caminho_arquivo = f'app/static/audio/{nome}.mp3'
    
    if not os.path.exists(caminho_arquivo):
        communicate = edge_tts.Communicate(texto, 'pt-BR-AntonioNeural')
        await communicate.save(caminho_arquivo)
        
    return caminho_arquivo
    

@app.route('/tts')
def tts():
    texto = request.args.get('texto')
    nome = request.args.get('nome')
    
    caminho_arquivo = asyncio.run(gerar_audio(texto, nome))
    
    with open(caminho_arquivo, 'rb') as f:
        return Response(f.read(), mimetype='audio/mpeg')

