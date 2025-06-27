import React, { useContext, useState } from "react";
import "./PlaceOrder.css";
import { StoreContext } from "../../context/StoreContext";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

function PlaceOrder() {
  const { getTotalCartAmount, cartItems, food_list, clearCart } =
    useContext(StoreContext);
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    street: "",
    city: "",
    county: "",
    zip: "",
    country: "",
    phone: "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const total = getTotalCartAmount();
  const deliveryFee = total === 0 ? 0 : 2;
  const grandTotal = total + deliveryFee;

  const handleInputChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    if (!token || !username) {
      MySwal.fire(
        "Not Logged In",
        "Please log in to place an order",
        "warning"
      );
      return;
    }

    if (total === 0) {
      MySwal.fire("Empty Cart", "Please add items to your cart", "info");
      return;
    }

    const selectedItems = Object.entries(cartItems)
      .filter(([id, qty]) => qty > 0)
      .map(([id, qty]) => {
        const product = food_list.find((f) => f.id === parseInt(id));
        return {
          id: product?.id || parseInt(id),
          name: product?.name || "Unknown",
          quantity: qty,
          price: product?.price || 0,
        };
      });

    const payload = {
      contact_info: {
        ...formData,
        username,
      },
      items: selectedItems,
      total: grandTotal,
    };

    try {
      setIsSubmitting(true);

      const res = await fetch("http://localhost:5000/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        clearCart();
        setFormData({
          firstName: "",
          lastName: "",
          email: "",
          street: "",
          city: "",
          county: "",
          zip: "",
          country: "",
          phone: "",
        });

        MySwal.fire({
          toast: true,
          position: "top-end",
          icon: "success",
          title: "Order placed successfully!",
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
        });

        setTimeout(() => navigate("/"), 2000);
      } else {
        MySwal.fire("Order Failed", data.error || "Try again later", "error");
      }
    } catch (err) {
      console.error(err);
      MySwal.fire("Error", "Something went wrong. Try again later.", "error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="place-order" onSubmit={handleSubmit}>
      <div className="place-order-left">
        <p className="title">Delivery Information</p>
        <div className="multi-fields">
          <input
            name="firstName"
            type="text"
            placeholder="First name"
            required
            onChange={handleInputChange}
            value={formData.firstName}
          />
          <input
            name="lastName"
            type="text"
            placeholder="Last name"
            required
            onChange={handleInputChange}
            value={formData.lastName}
          />
        </div>
        <input
          name="email"
          type="email"
          placeholder="Email address"
          required
          onChange={handleInputChange}
          value={formData.email}
        />
        <input
          name="street"
          type="text"
          placeholder="Street"
          required
          onChange={handleInputChange}
          value={formData.street}
        />
        <div className="multi-fields">
          <input
            name="city"
            type="text"
            placeholder="City"
            required
            onChange={handleInputChange}
            value={formData.city}
          />
          <input
            name="county"
            type="text"
            placeholder="County"
            required
            onChange={handleInputChange}
            value={formData.county}
          />
        </div>
        <div className="multi-fields">
          <input
            name="zip"
            type="text"
            placeholder="Zip code"
            required
            onChange={handleInputChange}
            value={formData.zip}
          />
          <input
            name="country"
            type="text"
            placeholder="Country"
            required
            onChange={handleInputChange}
            value={formData.country}
          />
        </div>
        <input
          name="phone"
          type="text"
          placeholder="Phone"
          required
          onChange={handleInputChange}
          value={formData.phone}
        />
      </div>

      <div className="place-order-right">
        <div className="cart-total">
          <h2>Cart Totals</h2>
          <div className="cart-total-details">
            <p>Subtotal</p>
            <p>${total}</p>
          </div>
          <hr />
          <div className="cart-total-details">
            <p>Delivery Fee</p>
            <p>${deliveryFee}</p>
          </div>
          <hr />
          <div className="cart-total-details">
            <p>Total</p>
            <p>${grandTotal}</p>
          </div>
          <button type="submit" disabled={isSubmitting || total === 0}>
            {isSubmitting
              ? "Placing Order..."
              : total === 0
              ? "Cart is still empty"
              : "CONFIRM ORDER"}
          </button>
        </div>
      </div>
    </form>
  );
}

export default PlaceOrder;
