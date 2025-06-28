import React, { useContext, useState, useEffect } from "react";
import "./Navbar.css";
import { assets } from "../../assets/assets";
import { Link } from "react-router-dom";
import { StoreContext } from "../../context/StoreContext";
import Swal from "sweetalert2";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

function Navbar({ setShowLogin, isLoggedIn, setIsLoggedIn }) {
  const [menu, setmenu] = useState("menu");
  const [username, setUsername] = useState("");
  const [hasOrders, setHasOrders] = useState(false);
  const [loadingOrders, setLoadingOrders] = useState(false);

  const { getTotalCartAmount, orderPlaced, setOrderPlaced } =
    useContext(StoreContext);

  // Fetch username from token (fallback if localStorage missing)
  useEffect(() => {
    const localUsername = localStorage.getItem("username");
    const token = localStorage.getItem("token");

    if (localUsername) {
      setUsername(localUsername);
    } else if (token) {
      fetch(`${API_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.username) {
            setUsername(data.username);
            localStorage.setItem("username", data.username);
          }
        })
        .catch(() => {});
    }
  }, [isLoggedIn]);

  // Fetch orders
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    setLoadingOrders(true);

    fetch(`${API_URL}/orders`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (res.status === 401) {
          console.warn("Token expired. Logging out.");
          localStorage.removeItem("token");
          localStorage.removeItem("username");
          setIsLoggedIn(false);
          return [];
        }
        return res.json();
      })
      .then((data) => {
        setHasOrders(Array.isArray(data) && data.length > 0);
      })
      .catch((err) => {
        console.error("Error fetching orders:", err);
        setHasOrders(false);
      })
      .finally(() => {
        setLoadingOrders(false);
        setOrderPlaced(false);
      });
  }, [isLoggedIn, getTotalCartAmount(), orderPlaced]);

  const handleLogout = () => {
    Swal.fire({
      title: "Are you sure?",
      text: "You will be logged out.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Yes, log me out!",
    }).then((result) => {
      if (result.isConfirmed) {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setIsLoggedIn(false);
        setUsername("");
        Swal.fire("Logged out!", "You have been logged out.", "success");
      }
    });
  };

  const handleBlockedClick = () => {
    Swal.fire({
      icon: "info",
      title: "Access Denied",
      text: "You need to place at least one order to view the orders section.",
    });
  };

  return (
    <div className="navbar">
      <Link to="/">
        <h2 className="logo-text">Munchify.</h2>
      </Link>

      <ul className="navbar-menu">
        <Link
          to="/"
          onClick={() => setmenu("home")}
          className={menu === "home" ? "active" : ""}
        >
          home
        </Link>
        <a
          href="#explore-menu"
          onClick={() => setmenu("menu")}
          className={menu === "menu" ? "active" : ""}
        >
          menu
        </a>
        <a
          href="#app-download"
          onClick={() => setmenu("mobile-app")}
          className={menu === "mobile-app" ? "active" : ""}
        >
          mobile-app
        </a>
        <a
          href="#footer"
          onClick={() => setmenu("contact us")}
          className={menu === "contact us" ? "active" : ""}
        >
          contact us
        </a>
      </ul>

      <div className="navbar-right">
        <div className="navbar-search-icon">
          <Link to="/cart">
            <img src={assets.basket_icon} alt="cart" />
          </Link>
          <div className={getTotalCartAmount() === 0 ? "" : "dot"}></div>
        </div>

        {isLoggedIn ? (
          <div className="user-info">
            <Link to="/account" className="username-link">
              <img
                className="profile_icon"
                src={assets.profile_icon}
                alt="Profile"
              />
            </Link>

            {loadingOrders ? (
              <span className="username loading-spinner">Checking...</span>
            ) : hasOrders ? (
              <Link to="/orders" className="username-link">
                <span className="username"> Hello {username}</span>
              </Link>
            ) : (
              <div
                className="username-link blocked"
                onClick={handleBlockedClick}
                title="Place an order to view your orders"
              >
                <span className="username"> Hello {username}</span>
              </div>
            )}

            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        ) : (
          <button onClick={() => setShowLogin(true)}>Sign In</button>
        )}
      </div>
    </div>
  );
}

export default Navbar;
