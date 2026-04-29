import json
from app import app, db
from app.models import Livro, Capitulo, Versiculos

with app.app_context():
    with open("app/json/pt_acf.json", encoding="utf-8-sig") as f:
        data = json.load(f)

    for livro_data in data:
        livro = Livro(
            nome=livro_data["name"],
            sigla=livro_data["name"][:3].lower()
        )
        db.session.add(livro)
        db.session.commit()

        for cap_index, capitulo in enumerate(livro_data["chapters"], start=1):
            cap = Capitulo(
                numero=cap_index,
                livro_id=livro.id
            )
            db.session.add(cap)
            db.session.commit()

            for ver_index, texto in enumerate(capitulo, start=1):
                versiculo = Versiculos(
                    numero_vers=ver_index,
                    texto=texto,
                    capitulo_id=cap.id
                )
                db.session.add(versiculo)

    db.session.commit()

print("✅ Bíblia importada com sucesso!")