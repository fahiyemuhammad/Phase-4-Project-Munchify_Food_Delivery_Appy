from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import Order
from server.extensions import db, mail
from flask_mail import Message
import datetime

orders_bp = Blueprint("orders_bp", __name__)

@orders_bp.route("/orders", methods=["POST", "OPTIONS"])
@jwt_required()
def create_order():
    if request.method == "OPTIONS":
        return '', 200

    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        contact_info = data.get("contact_info", {})
        items = data.get("items", [])
        total = data.get("total", 0)

        if not items or total == 0:
            return jsonify(error="Invalid order: cart is empty or total is zero."), 400

        # Save order
        new_order = Order(
            user_id=user_id,
            contact_info=contact_info,
            items=items,  # List of dicts: {name, quantity, price}
            total=total,
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(new_order)
        db.session.commit()

        # Send confirmation email
        email = contact_info.get("email")
        first_name = contact_info.get("firstName", "Customer")

        if email:
            item_lines = "\n".join([
                f"- {item.get('quantity', 1)} x {item.get('name', 'Unknown')} - ${item.get('price', 0)}"
                for item in items
            ])
            msg = Message(
                subject="Your Order Confirmation",
                sender="munchifyorg@gmail.com",
                recipients=[email],
                body=(
                    f"Hi {first_name},\n\n"
                    f"Thanks for placing your order with Munchify!\n\n"
                    f"Total: ${total}\n\n"
                    f"You'll pay on delivery. We'll reach out if there's anything else needed.\n\n"
                    f"Feel free to contact us: +254-754-354-649 \n\n"
                    f"Cheers,\nThe Munchify Team"
                )
            )
            mail.send(msg)

        return jsonify(message="Order placed successfully and email sent"), 201

    except Exception as e:
        db.session.rollback()
        print("Error while placing order:", str(e))
        return jsonify(error="Something went wrong while placing your order."), 400


@orders_bp.route("/orders", methods=["GET"])
@jwt_required()
def get_user_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

    return jsonify([
        {
            "id": o.id,
            "total": o.total,
            "created_at": o.created_at.isoformat(),
            "items": o.items,
            "contact_info": o.contact_info,
        } for o in orders
    ]), 200
