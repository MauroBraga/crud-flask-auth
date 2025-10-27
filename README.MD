# Crud Flask Auth

Repositório para um CRUD simples utilizando Flask com autenticação básica. Utilizando  SQLite como banco de dados.


Repositório criado para armazenar o código da Api autenticação banco de dados

pip instal -r requirements.txt pip3 install Flask==2.3.0

flask shell 
db.create_all() 
db.session() <sqlalchemy.orm.session.Session object at 0x7fcea8448ac0> 
db.session.commit()

Criar tabela 
db.create_all() 
db.session.commit()

user = User(username="admin",password="123") db.session.add(user) db.session.commit()