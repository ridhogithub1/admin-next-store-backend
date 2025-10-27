# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# from bson import ObjectId
# from datetime import datetime
# import json

# app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend

# # MongoDB Configuration
# MONGODB_URI = "mongodb+srv://rr6093225_db_user:SlhRyLgrH5VzNMvs@cluster0.ihxeqhh.mongodb.net/?appName=Cluster0"
# DATABASE_NAME = "dropship_db"
# COLLECTION_NAME = "orders"

# # Initialize MongoDB client
# print("🔄 Connecting to MongoDB...")
# try:
#     client = MongoClient(MONGODB_URI)
#     db = client[DATABASE_NAME]
#     orders_collection = db[COLLECTION_NAME]
    
#     # Test connection
#     client.admin.command('ping')
#     print("✅ MongoDB connection successful!")
#     print(f"📊 Database: {DATABASE_NAME}")
#     print(f"📦 Collection: {COLLECTION_NAME}")
# except Exception as e:
#     print(f"❌ MongoDB connection failed: {e}")

# def serialize_doc(doc):
#     """Convert MongoDB document to JSON-serializable format"""
#     if doc is None:
#         return None
    
#     doc['_id'] = str(doc['_id'])
    
#     # Convert datetime objects to ISO format strings
#     if 'createdAt' in doc and isinstance(doc['createdAt'], datetime):
#         doc['createdAt'] = doc['createdAt'].isoformat()
#     if 'updatedAt' in doc and isinstance(doc['updatedAt'], datetime):
#         doc['updatedAt'] = doc['updatedAt'].isoformat()
    
#     return doc

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "success",
#         "message": "Admin Dropship API is running! 🚀",
#         "endpoints": {
#             "GET /api/admin/orders": "Get all orders (with pagination)",
#             "GET /api/admin/orders/<order_id>": "Get order by ID",
#             "PUT /api/admin/orders/<order_id>": "Update order status",
#             "DELETE /api/admin/orders/<order_id>": "Delete order",
#             "GET /api/admin/stats": "Get statistics",
#             "GET /api/admin/recent": "Get recent orders"
#         }
#     })

# @app.route('/api/admin/orders', methods=['GET'])
# def get_all_orders():
#     """Get all orders with pagination and filters"""
#     try:
#         # Get query parameters
#         page = int(request.args.get('page', 1))
#         limit = int(request.args.get('limit', 10))
#         status = request.args.get('status')
#         search = request.args.get('search')
#         sort_by = request.args.get('sortBy', 'createdAt')
#         sort_order = request.args.get('sortOrder', 'desc')
        
#         # Calculate skip
#         skip = (page - 1) * limit
        
#         # Build query
#         query = {}
#         if status and status != 'all':
#             query['status'] = status
        
#         if search:
#             query['$or'] = [
#                 {'nama': {'$regex': search, '$options': 'i'}},
#                 {'orderId': {'$regex': search, '$options': 'i'}},
#                 {'telepon': {'$regex': search, '$options': 'i'}},
#                 {'produk': {'$regex': search, '$options': 'i'}}
#             ]
        
#         # Determine sort direction
#         sort_direction = -1 if sort_order == 'desc' else 1
        
#         # Get orders from MongoDB
#         orders = list(orders_collection.find(query)
#                      .sort(sort_by, sort_direction)
#                      .skip(skip)
#                      .limit(limit))
        
#         # Serialize documents
#         orders = [serialize_doc(order) for order in orders]
        
#         # Get total count
#         total_count = orders_collection.count_documents(query)
#         total_pages = (total_count + limit - 1) // limit
        
#         return jsonify({
#             "status": "success",
#             "data": orders,
#             "pagination": {
#                 "total": total_count,
#                 "page": page,
#                 "limit": limit,
#                 "totalPages": total_pages,
#                 "hasNext": page < total_pages,
#                 "hasPrev": page > 1
#             }
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting orders: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/orders/<order_id>', methods=['GET'])
# def get_order(order_id):
#     """Get order by order ID"""
#     try:
#         order = orders_collection.find_one({"orderId": order_id})
        
#         if not order:
#             return jsonify({
#                 "status": "error",
#                 "message": "Order not found"
#             }), 404
        
#         order = serialize_doc(order)
        
#         return jsonify({
#             "status": "success",
#             "data": order
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting order: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/orders/<order_id>', methods=['PUT'])
# def update_order(order_id):
#     """Update order status"""
#     try:
#         data = request.get_json()
#         new_status = data.get('status')
        
#         if not new_status:
#             return jsonify({
#                 "status": "error",
#                 "message": "Status is required"
#             }), 400
        
#         # Valid statuses
#         valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
#         if new_status not in valid_statuses:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
#             }), 400
        
#         # Update order
#         result = orders_collection.update_one(
#             {"orderId": order_id},
#             {
#                 "$set": {
#                     "status": new_status,
#                     "updatedAt": datetime.utcnow()
#                 }
#             }
#         )
        
#         if result.matched_count == 0:
#             return jsonify({
#                 "status": "error",
#                 "message": "Order not found"
#             }), 404
        
#         # Get updated order
#         updated_order = orders_collection.find_one({"orderId": order_id})
#         updated_order = serialize_doc(updated_order)
        
#         print(f"✅ Order {order_id} status updated to: {new_status}")
        
#         return jsonify({
#             "status": "success",
#             "message": "Order status updated",
#             "data": updated_order
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error updating order: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/orders/<order_id>', methods=['DELETE'])
# def delete_order(order_id):
#     """Delete order"""
#     try:
#         result = orders_collection.delete_one({"orderId": order_id})
        
#         if result.deleted_count == 0:
#             return jsonify({
#                 "status": "error",
#                 "message": "Order not found"
#             }), 404
        
#         print(f"🗑️ Order {order_id} deleted")
        
#         return jsonify({
#             "status": "success",
#             "message": "Order deleted successfully"
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error deleting order: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/stats', methods=['GET'])
# def get_stats():
#     """Get order statistics"""
#     try:
#         total_orders = orders_collection.count_documents({})
#         pending_orders = orders_collection.count_documents({"status": "pending"})
#         processing_orders = orders_collection.count_documents({"status": "processing"})
#         shipped_orders = orders_collection.count_documents({"status": "shipped"})
#         delivered_orders = orders_collection.count_documents({"status": "delivered"})
#         cancelled_orders = orders_collection.count_documents({"status": "cancelled"})
        
#         # Calculate total revenue
#         pipeline = [
#             {"$match": {"status": {"$in": ["delivered", "processing", "shipped"]}}},
#             {"$group": {
#                 "_id": None,
#                 "totalRevenue": {"$sum": "$totalHarga"}
#             }}
#         ]
#         revenue_result = list(orders_collection.aggregate(pipeline))
#         total_revenue = revenue_result[0]['totalRevenue'] if revenue_result else 0
        
#         # Get today's orders
#         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_orders = orders_collection.count_documents({
#             "createdAt": {"$gte": today_start}
#         })
        
#         return jsonify({
#             "status": "success",
#             "data": {
#                 "totalOrders": total_orders,
#                 "pendingOrders": pending_orders,
#                 "processingOrders": processing_orders,
#                 "shippedOrders": shipped_orders,
#                 "deliveredOrders": delivered_orders,
#                 "cancelledOrders": cancelled_orders,
#                 "totalRevenue": total_revenue,
#                 "todayOrders": today_orders
#             }
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting stats: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/recent', methods=['GET'])
# def get_recent_orders():
#     """Get recent orders"""
#     try:
#         limit = int(request.args.get('limit', 5))
        
#         orders = list(orders_collection.find()
#                      .sort('createdAt', -1)
#                      .limit(limit))
        
#         orders = [serialize_doc(order) for order in orders]
        
#         return jsonify({
#             "status": "success",
#             "data": orders
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting recent orders: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# if __name__ == '__main__':
#     print("\n" + "="*50)
#     print("🚀 Starting Admin Flask Server...")
#     print("📍 API URL: http://localhost:5001")
#     print("📖 Documentation: http://localhost:5001")
#     print("="*50 + "\n")
    
#     # Nonaktifkan reloader untuk menghindari error socket di Windows
#     app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# from bson import ObjectId
# from datetime import datetime
# import json

# app = Flask(__name__)
# CORS(app)  # Enable CORS for React frontend

# # MongoDB Configuration
# MONGODB_URI = "mongodb+srv://rr6093225_db_user:SlhRyLgrH5VzNMvs@cluster0.ihxeqhh.mongodb.net/?appName=Cluster0"
# DATABASE_NAME = "dropship_db"
# COLLECTION_NAME = "orders"

# # Initialize MongoDB client
# print("🔄 Connecting to MongoDB...")
# try:
#     client = MongoClient(MONGODB_URI)
#     db = client[DATABASE_NAME]
#     orders_collection = db[COLLECTION_NAME]
    
#     # Test connection
#     client.admin.command('ping')
#     print("✅ MongoDB connection successful!")
#     print(f"📊 Database: {DATABASE_NAME}")
#     print(f"📦 Collection: {COLLECTION_NAME}")
# except Exception as e:
#     print(f"❌ MongoDB connection failed: {e}")

# def serialize_doc(doc):
#     """Convert MongoDB document to JSON-serializable format"""
#     if doc is None:
#         return None
    
#     doc['_id'] = str(doc['_id'])
    
#     # Convert datetime objects to ISO format strings
#     if 'createdAt' in doc and isinstance(doc['createdAt'], datetime):
#         doc['createdAt'] = doc['createdAt'].isoformat()
#     if 'updatedAt' in doc and isinstance(doc['updatedAt'], datetime):
#         doc['updatedAt'] = doc['updatedAt'].isoformat()
    
#     return doc

# @app.route('/')
# def home():
#     return jsonify({
#         "status": "success",
#         "message": "Admin Dropship API is running! 🚀",
#         "endpoints": {
#             "GET /api/admin/orders": "Get all orders (with pagination)",
#             "GET /api/admin/orders/<order_id>": "Get order by ID",
#             "PUT /api/admin/orders/<order_id>": "Update order status",
#             "DELETE /api/admin/orders/<order_id>": "Delete order",
#             "GET /api/admin/stats": "Get statistics",
#             "GET /api/admin/recent": "Get recent orders"
#         }
#     })

# @app.route('/api/admin/orders', methods=['GET'])
# def get_all_orders():
#     """Get all orders with pagination and filters"""
#     try:
#         # Get query parameters
#         page = int(request.args.get('page', 1))
#         limit = int(request.args.get('limit', 10))
#         status = request.args.get('status')
#         search = request.args.get('search')
#         sort_by = request.args.get('sortBy', 'createdAt')
#         sort_order = request.args.get('sortOrder', 'desc')
        
#         # Calculate skip
#         skip = (page - 1) * limit
        
#         # Build query
#         query = {}
#         if status and status != 'all':
#             query['status'] = status
        
#         if search:
#             query['$or'] = [
#                 {'nama': {'$regex': search, '$options': 'i'}},
#                 {'orderId': {'$regex': search, '$options': 'i'}},
#                 {'telepon': {'$regex': search, '$options': 'i'}},
#                 {'produk': {'$regex': search, '$options': 'i'}}
#             ]
        
#         # Determine sort direction
#         sort_direction = -1 if sort_order == 'desc' else 1
        
#         # Get orders from MongoDB
#         orders = list(orders_collection.find(query)
#                      .sort(sort_by, sort_direction)
#                      .skip(skip)
#                      .limit(limit))
        
#         # Serialize documents
#         orders = [serialize_doc(order) for order in orders]
        
#         # Get total count
#         total_count = orders_collection.count_documents(query)
#         total_pages = (total_count + limit - 1) // limit
        
#         return jsonify({
#             "status": "success",
#             "data": orders,
#             "pagination": {
#                 "total": total_count,
#                 "page": page,
#                 "limit": limit,
#                 "totalPages": total_pages,
#                 "hasNext": page < total_pages,
#                 "hasPrev": page > 1
#             }
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting orders: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/orders/<order_id>', methods=['GET'])
# def get_order(order_id):
#     """Get order by order ID"""
#     try:
#         order = orders_collection.find_one({"orderId": order_id})
        
#         if not order:
#             return jsonify({
#                 "status": "error",
#                 "message": "Order not found"
#             }), 404
        
#         order = serialize_doc(order)
        
#         return jsonify({
#             "status": "success",
#             "data": order
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting order: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/orders/<order_id>', methods=['PUT'])
# def update_order(order_id):
#     """Update order status"""
#     try:
#         data = request.get_json()
#         new_status = data.get('status')
        
#         if not new_status:
#             return jsonify({
#                 "status": "error",
#                 "message": "Status is required"
#             }), 400
        
#         # Valid statuses
#         valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
#         if new_status not in valid_statuses:
#             return jsonify({
#                 "status": "error",
#                 "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
#             }), 400
        
#         # Update order
#         result = orders_collection.update_one(
#             {"orderId": order_id},
#             {
#                 "$set": {
#                     "status": new_status,
#                     "updatedAt": datetime.utcnow()
#                 }
#             }
#         )
        
#         if result.matched_count == 0:
#             return jsonify({
#                 "status": "error",
#                 "message": "Order not found"
#             }), 404
        
#         # Get updated order
#         updated_order = orders_collection.find_one({"orderId": order_id})
#         updated_order = serialize_doc(updated_order)
        
#         print(f"✅ Order {order_id} status updated to: {new_status}")
        
#         return jsonify({
#             "status": "success",
#             "message": "Order status updated",
#             "data": updated_order
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error updating order: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/orders/<order_id>', methods=['DELETE'])
# def delete_order(order_id):
#     """Delete order"""
#     try:
#         result = orders_collection.delete_one({"orderId": order_id})
        
#         if result.deleted_count == 0:
#             return jsonify({
#                 "status": "error",
#                 "message": "Order not found"
#             }), 404
        
#         print(f"🗑️ Order {order_id} deleted")
        
#         return jsonify({
#             "status": "success",
#             "message": "Order deleted successfully"
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error deleting order: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/stats', methods=['GET'])
# def get_stats():
#     """Get order statistics"""
#     try:
#         total_orders = orders_collection.count_documents({})
#         pending_orders = orders_collection.count_documents({"status": "pending"})
#         processing_orders = orders_collection.count_documents({"status": "processing"})
#         shipped_orders = orders_collection.count_documents({"status": "shipped"})
#         delivered_orders = orders_collection.count_documents({"status": "delivered"})
#         cancelled_orders = orders_collection.count_documents({"status": "cancelled"})
        
#         # Calculate total revenue
#         pipeline = [
#             {"$match": {"status": {"$in": ["delivered", "processing", "shipped"]}}},
#             {"$group": {
#                 "_id": None,
#                 "totalRevenue": {"$sum": "$totalHarga"}
#             }}
#         ]
#         revenue_result = list(orders_collection.aggregate(pipeline))
#         total_revenue = revenue_result[0]['totalRevenue'] if revenue_result else 0
        
#         # Get today's orders
#         today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#         today_orders = orders_collection.count_documents({
#             "createdAt": {"$gte": today_start}
#         })
        
#         return jsonify({
#             "status": "success",
#             "data": {
#                 "totalOrders": total_orders,
#                 "pendingOrders": pending_orders,
#                 "processingOrders": processing_orders,
#                 "shippedOrders": shipped_orders,
#                 "deliveredOrders": delivered_orders,
#                 "cancelledOrders": cancelled_orders,
#                 "totalRevenue": total_revenue,
#                 "todayOrders": today_orders
#             }
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting stats: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# @app.route('/api/admin/recent', methods=['GET'])
# def get_recent_orders():
#     """Get recent orders"""
#     try:
#         limit = int(request.args.get('limit', 5))
        
#         orders = list(orders_collection.find()
#                      .sort('createdAt', -1)
#                      .limit(limit))
        
#         orders = [serialize_doc(order) for order in orders]
        
#         return jsonify({
#             "status": "success",
#             "data": orders
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error getting recent orders: {e}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500

# if __name__ == '__main__':
#     print("\n" + "="*50)
#     print("🚀 Starting Admin Flask Server...")
#     print("📍 API URL: http://localhost:5001")
#     print("📖 Documentation: http://localhost:5001")
#     print("="*50 + "\n")
    
#     # Nonaktifkan reloader untuk menghindari error socket di Windows
#     app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from bson import ObjectId
from datetime import datetime
import os
import traceback
import certifi
import ssl
from flask import make_response

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB Configuration
MONGODB_URI = os.environ.get(
    "MONGODB_URI", 
    "mongodb+srv://rr6093225_db_user:SlhRyLgrH5VzNMvs@cluster0.ihxeqhh.mongodb.net/dropship_db?retryWrites=true&w=majority"
)
DATABASE_NAME = "dropship_db"
COLLECTION_NAME = "orders"
PRODUCT_COLLECTION = "products"

# Global variables
_client = None
_db = None
_collection = None

def get_db():
    """Get database connection with proper SSL handling for serverless"""
    global _client, _db, _collection
    
    if _collection is None:
        try:
            # Konfigurasi SSL yang lebih robust untuk Vercel
            _client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                maxPoolSize=1,
                minPoolSize=0,
                retryWrites=True,
                w='majority',
                tls=True,
                tlsAllowInvalidCertificates=False,
                tlsCAFile=certifi.where()  # Gunakan certifi untuk CA certificates
            )
            
            # Test connection
            _client.admin.command('ping')
            _db = _client[DATABASE_NAME]
            _collection = _db[COLLECTION_NAME]
            print("✅ MongoDB connected successfully")
            
        except ServerSelectionTimeoutError as e:
            print(f"❌ MongoDB timeout: {str(e)}")
            traceback.print_exc()
            raise Exception(f"Database connection timeout. Please check MongoDB Atlas settings.")
        except ConnectionFailure as e:
            print(f"❌ MongoDB connection failed: {str(e)}")
            traceback.print_exc()
            raise Exception(f"Database connection failed. Please verify credentials.")
        except Exception as e:
            print(f"❌ MongoDB error: {str(e)}")
            traceback.print_exc()
            raise Exception(f"Database error: {str(e)}")
    
    return _collection
def get_product_collection():
    """Get product collection"""
    global _db
    if _db is None:
        get_db()
    return _db[PRODUCT_COLLECTION]

@app.route('/api/admin/products', methods=['GET'])
def get_all_products():
    """Get all products with pagination"""
    try:
        collection = get_product_collection()
        
        page = max(1, int(request.args.get('page', 1)))
        limit = min(100, max(1, int(request.args.get('limit', 10))))
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        
        skip = (page - 1) * limit
        
        # Build query
        query = {}
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}},
                {'sku': {'$regex': search, '$options': 'i'}}
            ]
        
        if category and category != 'all':
            query['category'] = category
        
        total = collection.count_documents(query)
        
        products = list(collection.find(query)
                       .sort('createdAt', -1)
                       .skip(skip)
                       .limit(limit))
        
        products = [serialize_doc(p) for p in products]
        
        total_pages = max(1, (total + limit - 1) // limit)
        
        return jsonify({
            "status": "success",
            "data": products,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": total_pages,
                "hasNext": page < total_pages,
                "hasPrev": page > 1
            }
        }), 200
        
        response = jsonify({
            "status": "success",
            "data": products,
            "pagination": {...}
        })
        
        # Tambahkan header CORS secara manual
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    try:
        collection = get_product_collection()
        product = collection.find_one({"_id": ObjectId(product_id)})
        
        if not product:
            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": serialize_doc(product)
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/products', methods=['POST'])
def create_product():
    """Create new product"""
    try:
        collection = get_product_collection()
        data = request.get_json()
        
        required = ['name', 'price', 'stock']
        for field in required:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"{field} is required"
                }), 400
        
        product = {
            "name": data['name'],
            "description": data.get('description', ''),
            "price": float(data['price']),
            "stock": int(data['stock']),
            "category": data.get('category', 'Uncategorized'),
            "sku": data.get('sku', ''),
            "image": data.get('image', ''),
            "isActive": data.get('isActive', True),
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        result = collection.insert_one(product)
        product['_id'] = result.inserted_id
        
        return jsonify({
            "status": "success",
            "message": "Product created",
            "data": serialize_doc(product)
        }), 201
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product"""
    try:
        collection = get_product_collection()
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'price' in data:
            update_data['price'] = float(data['price'])
        if 'stock' in data:
            update_data['stock'] = int(data['stock'])
        if 'category' in data:
            update_data['category'] = data['category']
        if 'sku' in data:
            update_data['sku'] = data['sku']
        if 'image' in data:
            update_data['image'] = data['image']
        if 'isActive' in data:
            update_data['isActive'] = data['isActive']
        
        update_data['updatedAt'] = datetime.utcnow()
        
        result = collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404
        
        product = collection.find_one({"_id": ObjectId(product_id)})
        
        return jsonify({
            "status": "success",
            "message": "Product updated",
            "data": serialize_doc(product)
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    try:
        collection = get_product_collection()
        result = collection.delete_one({"_id": ObjectId(product_id)})
        
        if result.deleted_count == 0:
            return jsonify({
                "status": "error",
                "message": "Product not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Product deleted"
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/products/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    try:
        collection = get_product_collection()
        categories = collection.distinct("category")
        
        return jsonify({
            "status": "success",
            "data": categories
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    
    doc['_id'] = str(doc['_id'])
    
    if 'createdAt' in doc and isinstance(doc['createdAt'], datetime):
        doc['createdAt'] = doc['createdAt'].isoformat()
    if 'updatedAt' in doc and isinstance(doc['updatedAt'], datetime):
        doc['updatedAt'] = doc['updatedAt'].isoformat()
    
    return doc

@app.route('/')
@app.route('/api')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "Admin Dropship API is running! 🚀",
        "version": "2.0.1",
        "endpoints": {
            # Orders
            "GET /api/admin/orders": "Get all orders",
            "GET /api/admin/orders/<order_id>": "Get order by ID",
            "PUT /api/admin/orders/<order_id>": "Update order",
            "DELETE /api/admin/orders/<order_id>": "Delete order",
            # Stats
            "GET /api/admin/stats": "Get statistics",
            "GET /api/admin/recent": "Get recent orders",
            # Products
            "GET /api/admin/products": "Get all products",
            "GET /api/admin/products/<product_id>": "Get product by ID",
            "POST /api/admin/products": "Create product",
            "PUT /api/admin/products/<product_id>": "Update product",
            "DELETE /api/admin/products/<product_id>": "Delete product",
            "GET /api/admin/products/categories": "Get product categories"
        }
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Detailed health check including DB connection"""
    try:
        collection = get_db()
        collection.find_one()
        return jsonify({
            "status": "success",
            "message": "All systems operational",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Database connection failed",
            "error": str(e)
        }), 500

@app.route('/api/admin/orders', methods=['GET'])
def get_all_orders():
    """Get all orders with pagination"""
    try:
        collection = get_db()
        
        # Get parameters
        page = max(1, int(request.args.get('page', 1)))
        limit = min(100, max(1, int(request.args.get('limit', 10))))
        status = request.args.get('status', '')
        search = request.args.get('search', '').strip()
        
        skip = (page - 1) * limit
        
        # Build query
        query = {}
        if status and status != 'all':
            query['status'] = status
        
        if search:
            query['$or'] = [
                {'nama': {'$regex': search, '$options': 'i'}},
                {'orderId': {'$regex': search, '$options': 'i'}},
                {'telepon': {'$regex': search, '$options': 'i'}},
                {'produk': {'$regex': search, '$options': 'i'}}
            ]
        
        # Get count
        total = collection.count_documents(query)
        
        # Get orders
        orders = list(collection.find(query)
                     .sort('createdAt', -1)
                     .skip(skip)
                     .limit(limit))
        
        orders = [serialize_doc(o) for o in orders]
        
        total_pages = max(1, (total + limit - 1) // limit)
        
        return jsonify({
            "status": "success",
            "data": orders,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": total_pages,
                "hasNext": page < total_pages,
                "hasPrev": page > 1
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get single order"""
    try:
        collection = get_db()
        order = collection.find_one({"orderId": order_id})
        
        if not order:
            return jsonify({
                "status": "error",
                "message": "Order not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": serialize_doc(order)
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status"""
    try:
        collection = get_db()
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({
                "status": "error",
                "message": "Status required"
            }), 400
        
        new_status = data['status']
        valid = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        
        if new_status not in valid:
            return jsonify({
                "status": "error",
                "message": "Invalid status"
            }), 400
        
        result = collection.update_one(
            {"orderId": order_id},
            {"$set": {
                "status": new_status,
                "updatedAt": datetime.utcnow()
            }}
        )
        
        if result.matched_count == 0:
            return jsonify({
                "status": "error",
                "message": "Order not found"
            }), 404
        
        order = collection.find_one({"orderId": order_id})
        
        return jsonify({
            "status": "success",
            "message": "Updated",
            "data": serialize_doc(order)
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete order"""
    try:
        collection = get_db()
        result = collection.delete_one({"orderId": order_id})
        
        if result.deleted_count == 0:
            return jsonify({
                "status": "error",
                "message": "Order not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Deleted"
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    try:
        collection = get_db()
        
        total = collection.count_documents({})
        pending = collection.count_documents({"status": "pending"})
        processing = collection.count_documents({"status": "processing"})
        shipped = collection.count_documents({"status": "shipped"})
        delivered = collection.count_documents({"status": "delivered"})
        cancelled = collection.count_documents({"status": "cancelled"})
        
        # Revenue
        pipeline = [
            {"$match": {"status": {"$in": ["delivered", "processing", "shipped"]}}},
            {"$group": {"_id": None, "total": {"$sum": "$totalHarga"}}}
        ]
        
        result = list(collection.aggregate(pipeline))
        revenue = result[0]['total'] if result else 0
        
        # Today
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = collection.count_documents({"createdAt": {"$gte": today}})
        
        return jsonify({
            "status": "success",
            "data": {
                "totalOrders": total,
                "pendingOrders": pending,
                "processingOrders": processing,
                "shippedOrders": shipped,
                "deliveredOrders": delivered,
                "cancelledOrders": cancelled,
                "totalRevenue": revenue,
                "todayOrders": today_count
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/recent', methods=['GET'])
def get_recent():
    """Get recent orders"""
    try:
        collection = get_db()
        limit = min(20, max(1, int(request.args.get('limit', 5))))
        
        orders = list(collection.find()
                     .sort('createdAt', -1)
                     .limit(limit))
        
        return jsonify({
            "status": "success",
            "data": [serialize_doc(o) for o in orders]
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "Server error"}), 500

# For local dev
if __name__ == '__main__':
    app.run(debug=True, port=5001)
