import React, { useEffect, useState } from "react";
import "./Orders.css";
import { useNavigate } from "react-router-dom";

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await fetch("http://localhost:5000/orders", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await res.json();
        if (res.ok) {
          setOrders(data);
        } else {
          console.error("Failed to fetch orders:", data.error);
        }
      } catch (err) {
        console.error("Error fetching orders:", err);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchOrders();
    }
  }, [token]);

  const handleEditAccount = () => {
    navigate("/edit-account");
  };

  const handleDeleteAccount = () => {
    const confirmed = window.confirm(
      "Are you sure you want to delete your account?"
    );
    if (confirmed) {
      fetch("http://localhost:5000/auth/delete", {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => {
          if (res.ok) {
            localStorage.removeItem("token");
            localStorage.removeItem("username");
            alert("Account deleted. Logging out...");
            navigate("/");
            window.location.reload();
          } else {
            alert("Failed to delete account.");
          }
        })
        .catch((err) => {
          console.error(err);
          alert("Something went wrong.");
        });
    }
  };

  if (!token) {
    return <p className="orders-message">Please log in to view your orders.</p>;
  }

  if (loading) {
    return <p className="orders-message">Loading orders...</p>;
  }

  return (
    <div className="orders-container">
      <div className="orders-header">
        <h2 className="orders-title">Your Order History</h2>
        <div className="account-buttons">
          <button onClick={handleEditAccount} className="edit-btn">
            Edit Account
          </button>
          <button onClick={handleDeleteAccount} className="delete-btn">
            Delete Account
          </button>
        </div>
      </div>

      {orders.length === 0 ? (
        <p className="orders-message">You have no past orders.</p>
      ) : (
        <div className="orders-list">
          {orders.map((order) => (
            <div key={order.id} className="order-card">
              <p>
                <strong>Order ID:</strong> {order.id}
              </p>
              <p>
                <strong>Date:</strong>{" "}
                {new Date(order.created_at).toLocaleString()}
              </p>
              <p>
                <strong>Total:</strong> ${order.total.toFixed(2)}
              </p>

              <p>
                <strong>Delivery Info:</strong>
              </p>
              <p>
                {order.contact_info.firstName} {order.contact_info.lastName}
              </p>
              <p>{order.contact_info.email}</p>
              <p>
                {order.contact_info.street}, {order.contact_info.city},{" "}
                {order.contact_info.county}
              </p>
              <p>
                {order.contact_info.zip}, {order.contact_info.country}
              </p>
              <p>{order.contact_info.phone}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Orders;
