import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar/Navbar";
import { Route, Routes } from "react-router-dom";
import PlaceOrder from "./pages/PlaceOrder/PlaceOrder";
import Home from "./pages/Home/Home";
import Cart from "./pages/Cart/Cart";
import Footer from "./components/Footer/Footer";
import LoginPopup from "./components/LoginPopup/LoginPopup";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; // Toastify styles
import Orders from "./pages/Orders";
import EditAccount from "./pages/EditAccount";

const App = () => {
  const [showLogin, setShowLogin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  return (
    <>
      {/* ✅ Global Toast Notification Container */}
      <ToastContainer position="top-center" autoClose={2000} />

      {/* ✅ Conditional Login Form */}
      {showLogin && (
        <LoginPopup setShowLogin={setShowLogin} setIsLoggedIn={setIsLoggedIn} />
      )}

      <div className="app">
        <Navbar
          setShowLogin={setShowLogin}
          isLoggedIn={isLoggedIn}
          setIsLoggedIn={setIsLoggedIn}
        />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/order" element={<PlaceOrder />} />
          <Route path="/orders" element={<Orders />} />
          <Route
            path="/edit-account"
            element={<EditAccount setIsLoggedIn={setIsLoggedIn} />}
          />
        </Routes>
      </div>

      <Footer />
    </>
  );
};

export default App;
