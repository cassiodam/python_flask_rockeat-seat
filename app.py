from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
#onde fica o BD?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)
# Modelagem

# Produto (id, name, price, descruption)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data.get("name", ""), price=data.get("price", ""), description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"}) #200
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    # Recuperar o produto da base de dados
    # Verificar se o produto existe
    # Se existe, apagar da base de dados
    # Se nao existe, retornar 404 not found
    product = Product.query.get(product_id)
    if product: # ou > if product != None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}) #200
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
            product.price = data['price']
            
    if 'name' in data:
            product.description = data['price']
      
    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 404

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
      poduct_data  {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
      }
      product_list.append(produt_data)
    return jsonify(product_list)


# Rotas // Definir rota raiz (pagina inicial) e sua função
@app.route('/')
def hello_world():
    return 'Hello World'
if __name__ == "__main__":
    app.run(debug=True) #Utilizado somente em ambiente de produção
