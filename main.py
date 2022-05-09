from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json
from datetime import datetime

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # создание виртуальной бд в памяти запуска программы (с пропиской драйвера бд)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///16.2_homework_base.db"  # создание в текущей директории файла бд (с пропиской драйвера бд)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False
app.url_map.strict_slashes = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)



class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    # start_date = db.Column(db.Date)
    # end_date = db.Column(db.Date)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    adress = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))



class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    user = relationship("User")
    order = relationship("Order")


db.create_all()  # создание всех моделей таблиц в бд






# Заполнение таблиц из JSON файлов

with open("users.json", "r") as file:  # считываем json файл в python словарь
    data = json.load(file)
for user in data:  # создаем объекты и записываем в таблицу бд
    new_user = User(
        #id = user['id'],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    )
    db.session.add(new_user)
    db.session.commit()


with open("orders.json", "r") as file:  # считываем json файл в python словарь
    data = json.load(file)
for order in data:  # создаем объекты и записываем в таблицу бд
    new_order = Order(
        #id=order['id'],
        description=order['description'],
        #start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),  # форматирование считываемой даты (строка)в питоновскую дату
        #end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'), # форматирование считываемой даты (строка) в питоновскую дату
        start_date=order['start_date'],
        end_date=order['end_date'],
        adress=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )
    db.session.add(new_order)
    db.session.commit()


with open("offers.json", "r") as file:  # считываем json файл в python словарь
    data = json.load(file)
for offer in data:  # создаем объекты и записываем в таблицу бд
    new_offer = Offer(
        #id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id']
    )
    db.session.add(new_offer)
    db.session.commit()

# db.drop_all()  # удаление всех моделей таблиц в бд






# Делаем представления для работы с бд

@app.route('/users/', methods=['GET', 'POST'])
def users_page_index():
    if request.method == "GET":
        rows = db.session.query(User).all()
        users = []
        for row in rows:
            new_row = {"id": row.id,
                       "first_name": row.first_name,
                       "last_name": row.last_name,
                       "age": row.age,
                       "email": row.email,
                       "role": row.role,
                       "phone": row.phone,
                       }
            users.append(new_row)
        return jsonify(users)

    elif request.method == "POST":  # добавление нового пользователя
        new_json = request.json
        new_user = User(
            #id=new_json['id'],
            first_name=new_json['first_name'],
            last_name=new_json['last_name'],
            age=new_json['age'],
            email=new_json['email'],
            role=new_json['role'],
            phone=new_json['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return 'данные JSON записаны'

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def show_id_user_page(id):
    if request.method == "GET":
        try:
            row = User.query.get(id)
            data = list()
            new_row = {"id": row.id,
                       "first_name": row.first_name,
                       "last_name": row.last_name,
                       "age": row.age,
                       "email": row.email,
                       "role": row.role,
                       "phone": row.phone,
                       }
            data.append(new_row)
            return jsonify(data)
        except:
            return f'user id:{id} не обнаружен'

    elif request.method == "PUT":  # перезапись полей при изместном id
        new_json = request.json
        new_json_user = User(
            # id=new_json['id'],
            first_name=new_json['first_name'],
            last_name=new_json['last_name'],
            age=new_json['age'],
            email=new_json['email'],
            role=new_json['role'],
            phone=new_json['phone']
        )
        old_id_user = User.query.get(id)

        old_id_user.first_name = new_json_user.first_name
        old_id_user.last_name = new_json_user.last_name
        old_id_user.age = new_json_user.age
        old_id_user.email = new_json_user.email
        old_id_user.role = new_json_user.role
        old_id_user.phone = new_json_user.phone

        db.session.add(old_id_user)
        db.session.commit()
        return f'данные user id:{id} обновлены'

    elif request.method == "DELETE":  # удаление user при известном id
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return f'user id:{id} удален'








@app.route("/orders", methods=["GET", "POST"])
def orders_page_index():
    if request.method == "GET":
        rows = db.session.query(Order).all()
        orders = []
        for row in rows:
            new_row = {"id": row.id,
                       "description": row.description,
                       "start_date": row.start_date,
                       "end_date": row.end_date,
                       "adress": row.adress,
                       "price": row.price,
                       "customer_id": row.customer_id,
                       "executor_id": row.executor_id
                       }
            orders.append(new_row)
        return jsonify(orders)

    elif request.method == "POST":   # добавление нового order
        new_json = request.json
        new_order = Order(
            #id=new_json['id'],
            description=new_json['description'],
            start_date=new_json['start_date'],
            end_date=new_json['end_date'],
            adress=new_json['adress'],
            price=new_json['price'],
            customer_id=new_json['customer_id'],
            executor_id=new_json['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()
        return 'данные JSON записаны'


@app.route('/orders/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def show_id_order_page(id):
    if request.method == "GET":
        try:
            row = Order.query.get(id)
            data = list()
            new_row = {"id": row.id,
                       "description": row.description,
                       "start_date": row.start_date,
                       "end_date": row.end_date,
                       "adress": row.adress,
                       "price": row.price,
                       "customer_id": row.customer_id,
                       "executor_id": row.executor_id
                       }
            data.append(new_row)
            return jsonify(data)
        except:
            return f'order id:{id} не обнаружен'

    elif request.method == "PUT":    # перезапись полей при изместном id
        new_json = request.json
        new_json_user = Order(
            # id=new_json['id'],
            description=new_json['description'],
            start_date=new_json['start_date'],
            end_date=new_json['end_date'],
            adress=new_json['adress'],
            price=new_json['price'],
            customer_id=new_json['customer_id'],
            executor_id=new_json['executor_id']
        )
        old_id_order = Order.query.get(id)

        old_id_order.description = new_json_user.description
        old_id_order.start_date = new_json_user.start_date
        old_id_order.end_date = new_json_user.end_date
        old_id_order.adress = new_json_user.adress
        old_id_order.price = new_json_user.price
        old_id_order.customer_id = new_json_user.customer_id
        old_id_order.executor_id = new_json_user.executor_id

        db.session.add(old_id_order)
        db.session.commit()
        return f'данные order id:{id} обновлены'

    elif request.method == "DELETE":   # удаление order при известном id
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return f'order id:{id} удален'








@app.route("/offers", methods=["GET", "POST"])
def offers_page_index():
    if request.method == "GET":
        rows = db.session.query(Offer).all()
        offers = []
        for row in rows:
            new_row = {"id": row.id,
                       "order_id": row.order_id,
                       "executor_id": row.executor_id
                       }
            offers.append(new_row)
        return jsonify(offers)

    elif request.method == "POST":   #добавление нового offer
        new_json = request.json
        new_offer = Offer(
            #id=new_json['id'],
            order_id=new_json['order_id'],
            executor_id=new_json['executor_id']
        )
        db.session.add(new_offer)
        db.session.commit()
        return 'данные JSON записаны'


@app.route('/offers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def show_id_offer_page(id):
    if request.method == "GET":
        try:
            row = Offer.query.get(id)
            data = list()
            new_row = {"id": row.id,
                       "order_id": row.order_id,
                       "executor_id": row.executor_id
                       }
            data.append(new_row)
            return jsonify(data)
        except:
            return f'offer id:{id} не обнаружен'

    elif request.method == "PUT":    # перезапись полей при изместном id
        new_json = request.json
        new_json_offer = Offer(
            # id=new_json['id'],
            order_id=new_json['order_id'],
            executor_id=new_json['executor_id']
        )
        old_id_offer = Offer.query.get(id)

        old_id_offer.order_id = new_json_offer.order_id
        old_id_offer.executor_id = new_json_offer.executor_id

        db.session.add(old_id_offer)
        db.session.commit()
        return f'данные offer id:{id} обновлены'

    elif request.method == "DELETE":   # удаление offer при известном id
        offer = Offer.query.get(id)
        db.session.delete(offer)
        db.session.commit()
        return f'offer id:{id} Удален'



# для теста

if __name__ == "__main__":
    app.run(debug=True)
