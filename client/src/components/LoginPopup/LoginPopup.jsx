import React, { useState } from "react";
import "./LoginPopup.css";
import { assets } from "../../assets/assets";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const LoginPopup = ({ setShowLogin, setIsLoggedIn }) => {
  const [currentState, setCurrentState] = useState("Login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  //  Reset all form fields and state
  const resetForm = () => {
    setUsername("");
    setEmail("");
    setPassword("");
    setCurrentState("Login");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const url =
      currentState === "Login"
        ? "https://munchify-backend.onrender.com/auth/login"
        : "https://munchify-backend.onrender.com/auth/register";

    const payload =
      currentState === "Login"
        ? { email, password }
        : { username, email, password };

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", data.username);
        setIsLoggedIn(true);
        setShowLogin(false); //  Close popup
        toast.success("Login successful!");
        resetForm(); //  Clear form after login
      } else if (res.ok && currentState === "Sign Up") {
        toast.success("Account created! Please log in.");
        setCurrentState("Login");
        resetForm(); //  Clear form after signup
      } else {
        toast.error(data.error || "Authentication failed");
      }
    } catch (err) {
      console.error(err);
      toast.error("Something went wrong. Please try again.");
    }
  };

  return (
    <>
      <ToastContainer position="top-center" autoClose={2000} />
      <div className="login-popup">
        <form className="login-popup-container" onSubmit={handleSubmit}>
          <div className="login-popup-title">
            <h2>{currentState}</h2>
            <img
              onClick={() => {
                setShowLogin(false);
                resetForm(); //  Clear form when popup is closed
              }}
              src={assets.cross_icon}
              alt="close"
            />
          </div>

          <div className="login-popup-inputs">
            {currentState === "Login" ? null : (
              <input
                type="text"
                placeholder="Your Name"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            )}
            <input
              type="email"
              placeholder="Your Email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit">
            {currentState === "Sign Up" ? "Create account" : "Login"}
          </button>

          <div className="login-popup-condition">
            <input type="checkbox" required />
            <p>
              By continuing I agree to the{" "}
              <a className="terms-link" href="">
                terms of use & privacy policy.
              </a>
            </p>
          </div>

          {currentState === "Login" ? (
            <p>
              Create a new account?{" "}
              <span onClick={() => setCurrentState("Sign Up")}>Click Here</span>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <span onClick={() => setCurrentState("Login")}>Login here</span>
            </p>
          )}
        </form>
      </div>
    </>
  );
};

export default LoginPopup;