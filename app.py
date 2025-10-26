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
from bson import ObjectId
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# MongoDB Configuration
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://rr6093225_db_user:SlhRyLgrH5VzNMvs@cluster0.ihxeqhh.mongodb.net/?appName=Cluster0")
DATABASE_NAME = "dropship_db"
COLLECTION_NAME = "orders"

# Initialize MongoDB client (lazy connection)
client = None
db = None
orders_collection = None

def get_db():
    """Get database connection (lazy initialization)"""
    global client, db, orders_collection
    
    if orders_collection is None:
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            db = client[DATABASE_NAME]
            orders_collection = db[COLLECTION_NAME]
            # Test connection
            client.admin.command('ping')
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            raise
    
    return orders_collection

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    
    doc['_id'] = str(doc['_id'])
    
    # Convert datetime objects to ISO format strings
    if 'createdAt' in doc and isinstance(doc['createdAt'], datetime):
        doc['createdAt'] = doc['createdAt'].isoformat()
    if 'updatedAt' in doc and isinstance(doc['updatedAt'], datetime):
        doc['updatedAt'] = doc['updatedAt'].isoformat()
    
    return doc

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Admin Dropship API is running! 🚀",
        "endpoints": {
            "GET /api/admin/orders": "Get all orders (with pagination)",
            "GET /api/admin/orders/<order_id>": "Get order by ID",
            "PUT /api/admin/orders/<order_id>": "Update order status",
            "DELETE /api/admin/orders/<order_id>": "Delete order",
            "GET /api/admin/stats": "Get statistics",
            "GET /api/admin/recent": "Get recent orders"
        }
    })

@app.route('/api/admin/orders', methods=['GET'])
def get_all_orders():
    """Get all orders with pagination and filters"""
    try:
        collection = get_db()
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        status = request.args.get('status')
        search = request.args.get('search')
        sort_by = request.args.get('sortBy', 'createdAt')
        sort_order = request.args.get('sortOrder', 'desc')
        
        # Calculate skip
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
        
        # Determine sort direction
        sort_direction = -1 if sort_order == 'desc' else 1
        
        # Get orders from MongoDB
        orders = list(collection.find(query)
                     .sort(sort_by, sort_direction)
                     .skip(skip)
                     .limit(limit))
        
        # Serialize documents
        orders = [serialize_doc(order) for order in orders]
        
        # Get total count
        total_count = collection.count_documents(query)
        total_pages = (total_count + limit - 1) // limit
        
        return jsonify({
            "status": "success",
            "data": orders,
            "pagination": {
                "total": total_count,
                "page": page,
                "limit": limit,
                "totalPages": total_pages,
                "hasNext": page < total_pages,
                "hasPrev": page > 1
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting orders: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by order ID"""
    try:
        collection = get_db()
        order = collection.find_one({"orderId": order_id})
        
        if not order:
            return jsonify({
                "status": "error",
                "message": "Order not found"
            }), 404
        
        order = serialize_doc(order)
        
        return jsonify({
            "status": "success",
            "data": order
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting order: {e}")
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
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({
                "status": "error",
                "message": "Status is required"
            }), 400
        
        # Valid statuses
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                "status": "error",
                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            }), 400
        
        # Update order
        result = collection.update_one(
            {"orderId": order_id},
            {
                "$set": {
                    "status": new_status,
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            return jsonify({
                "status": "error",
                "message": "Order not found"
            }), 404
        
        # Get updated order
        updated_order = collection.find_one({"orderId": order_id})
        updated_order = serialize_doc(updated_order)
        
        return jsonify({
            "status": "success",
            "message": "Order status updated",
            "data": updated_order
        }), 200
        
    except Exception as e:
        print(f"❌ Error updating order: {e}")
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
            "message": "Order deleted successfully"
        }), 200
        
    except Exception as e:
        print(f"❌ Error deleting order: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """Get order statistics"""
    try:
        collection = get_db()
        
        total_orders = collection.count_documents({})
        pending_orders = collection.count_documents({"status": "pending"})
        processing_orders = collection.count_documents({"status": "processing"})
        shipped_orders = collection.count_documents({"status": "shipped"})
        delivered_orders = collection.count_documents({"status": "delivered"})
        cancelled_orders = collection.count_documents({"status": "cancelled"})
        
        # Calculate total revenue
        pipeline = [
            {"$match": {"status": {"$in": ["delivered", "processing", "shipped"]}}},
            {"$group": {
                "_id": None,
                "totalRevenue": {"$sum": "$totalHarga"}
            }}
        ]
        revenue_result = list(collection.aggregate(pipeline))
        total_revenue = revenue_result[0]['totalRevenue'] if revenue_result else 0
        
        # Get today's orders
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_orders = collection.count_documents({
            "createdAt": {"$gte": today_start}
        })
        
        return jsonify({
            "status": "success",
            "data": {
                "totalOrders": total_orders,
                "pendingOrders": pending_orders,
                "processingOrders": processing_orders,
                "shippedOrders": shipped_orders,
                "deliveredOrders": delivered_orders,
                "cancelledOrders": cancelled_orders,
                "totalRevenue": total_revenue,
                "todayOrders": today_orders
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/admin/recent', methods=['GET'])
def get_recent_orders():
    """Get recent orders"""
    try:
        collection = get_db()
        limit = int(request.args.get('limit', 5))
        
        orders = list(collection.find()
                     .sort('createdAt', -1)
                     .limit(limit))
        
        orders = [serialize_doc(order) for order in orders]
        
        return jsonify({
            "status": "success",
            "data": orders
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting recent orders: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# For Vercel serverless function
if __name__ != '__main__':
    # This is needed for Vercel
    app = app
