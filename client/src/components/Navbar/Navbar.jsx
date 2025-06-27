import React, { useContext, useState, useEffect } from "react";
import "./Navbar.css";
import { assets } from "../../assets/assets";
import { Link } from "react-router-dom";
import { StoreContext } from "../../context/StoreContext";
import Swal from "sweetalert2";

function Navbar({ setShowLogin, isLoggedIn, setIsLoggedIn }) {
  const [menu, setmenu] = useState("menu");
  const [username, setUsername] = useState("");
  const { getTotalCartAmount } = useContext(StoreContext);

  useEffect(() => {
    const storedUser = localStorage.getItem("username");
    if (storedUser) {
      setUsername(storedUser);
    }
  }, [isLoggedIn]);

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
            <Link to="/orders" className="username-link">
              <img className="profile_icon" src={assets.profile_icon} alt="" />
            </Link>
            <Link to="/orders" className="username-link">
              <span className="username"> Hello {username}</span>
            </Link>
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
