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
  const [isSubmitting, setIsSubmitting] = useState(false); // Prevent double submits

  const resetForm = () => {
    setUsername("");
    setEmail("");
    setPassword("");
  };

  const handleSubmit = async (e, isRetry = false) => {
    e.preventDefault();
    if (isSubmitting) return; // Prevent multiple submissions

    setIsSubmitting(true);

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

      // Successful login
      if (res.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", data.username || username);
        setIsLoggedIn(true);
        setShowLogin(false);
        toast.success(`Welcome${data.username ? `, ${data.username}` : ""}! 🎉`);
        resetForm();
      }
      // Successful signup
      else if (res.ok && currentState === "Sign Up") {
        toast.success("Account created successfully! Please log in.");
        setCurrentState("Login");
        resetForm();
      }
      // Temporary DB issue (Render waking up) — auto-retry once
      else if (res.status === 503 && !isRetry) {
        toast.info("Database waking up — retrying...");
        setTimeout(() => handleSubmit(e, true), 2000); // Retry after 2s
      }
      // Known errors from backend
      else if (data.error) {
        toast.error(data.error);
      }
      // Unknown error
      else {
        toast.error("Authentication failed. Please try again.");
      }
    } catch (err) {
      console.error("Network error:", err);
      toast.error("Network error. Check your connection and try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const closePopup = () => {
    setShowLogin(false);
    resetForm();
  };

  return (
    <>
      <ToastContainer position="top-center" autoClose={3000} />

      <div className="login-popup">
        <form className="login-popup-container" onSubmit={handleSubmit}>
          <div className="login-popup-title">
            <h2>{currentState}</h2>
            <img
              onClick={closePopup}
              src={assets.cross_icon}
              alt="close"
              style={{ cursor: "pointer" }}
            />
          </div>

          <div className="login-popup-inputs">
            {currentState === "Sign Up" && (
              <input
                type="text"
                placeholder="Your Name"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={isSubmitting}
              />
            )}
            <input
              type="email"
              placeholder="Your Email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isSubmitting}
            />
            <input
              type="password"
              placeholder="Password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isSubmitting}
            />
          </div>

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting
              ? "Processing..."
              : currentState === "Sign Up"
              ? "Create account"
              : "Login"}
          </button>

          <div className="login-popup-condition">
            <input type="checkbox" required disabled={isSubmitting} />
            <p>
              By continuing I agree to the{" "}
              <a className="terms-link" href="#" onClick={(e) => e.preventDefault()}>
                terms of use & privacy policy
              </a>
              .
            </p>
          </div>

          {currentState === "Login" ? (
            <p>
              Create a new account?{" "}
              <span onClick={() => setCurrentState("Sign Up")}>Click here</span>
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