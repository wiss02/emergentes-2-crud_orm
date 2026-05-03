from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_super_seguro'

# Configurar base de datos SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear base de datos
with app.app_context():
    db.create_all()

# READ ALL (List)
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# CREATE
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form.get('stock', 0))
        
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        
        flash('Producto creado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

# READ ONE (View)
@app.route('/view/<int:id>')
def view(id):
    product = Product.query.get_or_404(id)
    return render_template('view.html', product=product)

# UPDATE (Edit)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.stock = int(request.form.get('stock', 0))
        
        db.session.commit()
        flash('Producto actualizado exitosamente!', 'info')
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

# DELETE
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
