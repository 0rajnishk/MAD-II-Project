from flask import jsonify
from backend import app
from backend.models import User
from backend import db
from flask_restful import reqparse
from backend.dto import Response
# from backend.tasks import export_products_csv

@app.route('/api/upload-image/<int:userId>', methods=['POST'])
def uploadImage(userId):
    parser = reqparse.RequestParser()
    parser.add_argument('image', type=str)
    args = parser.parse_args()
    if args['image']:
        user = User.query.get(userId)
        user.image = args['image']
        db.session.commit()
        return Response('Image uploaded...!').serialize(), 200
    return Response('Please choose a valid image').serialize(), 400


# @app.route('/api/product/<int:catId>')
# def productByCateId(catId):
#     products = Product.query.all()
#     result=[]
#     for product in products:
#         if product.category_id == int(catId):
#             result.append(product)

#     return [p.serialize() for p in result]

# @app.route('/api/search/<query>')
# def search(query):
#     data = {}
#     units = Unit.query.filter(Unit.name.like(f'%{query}%')).all()
#     if units:
#         data['units'] = [u.serialize() for u in units]
#     categories = Category.query.filter(Category.name.like(f'%{query}%')).all()
#     if categories:
#         data['categories'] =  [c.serialize() for c in categories]
#     products = Product.query.filter(db.or_(Product.name.like(f'%{query}%'), Product.unit_price.like(f'%{query}%'), Product.id.like(f'%{query}%'))).all()
#     if products:
#         data['products'] = [p.serialize() for p in products]
#     return data

# @app.route('/api/export_products', methods=['POST'])
# def export_products():
#     # Trigger the Celery task for CSV export
#     # task = export_products_csv.apply_async()
#     # export_products_csv()
#     # Send a response to the client with the task ID
#     return jsonify({"task_id": task.id}), 202