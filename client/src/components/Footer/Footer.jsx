import React from "react";
import "./Footer.css";
import { assets } from "../../assets/assets";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <div className="footer" id="footer">
      <div className="footer-content">
        <div className="footer-content-left">
          <Link to="/">
            <h2 className="logo-text">Munchify.</h2>
          </Link>
          <p>
            We’re here to make food ordering effortless, enjoyable, and
            delicious. By partnering with trusted restaurants and prioritizing
            user satisfaction, we aim to be your go-to app for every craving.
            Hungry? Download Munchify today!
          </p>
          <div className="footer-social-icons">
            <a
              href="https://www.facebook.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-icons"
            >
              <img src={assets.facebook_icon} alt="Facebook" />
            </a>
            <a
              href="https://twitter.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-icons"
            >
              <img src={assets.twitter_icon} alt="Twitter" />
            </a>
            <a
              href="https://www.linkedin.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="social-icons"
            >
              <img src={assets.linkedin_icon} alt="LinkedIn" />
            </a>
          </div>
        </div>
        <div className="footer-content-center">
          <h2>COMPANY</h2>
          <ul>
            <li>Home</li>
            <li>About us</li>
            <li>Delivery</li>
            <li>Privacy policy</li>
          </ul>
        </div>
        <div className="footer-content-right">
          <h2>GET IN TOUCH</h2>
          <ul>
            <li>+254-743-611-649</li>
            <li>munchifyorg@gmail.com</li>
          </ul>
        </div>
      </div>

      {/* ✅ Map Section */}
      <div className="footer-map">
        <iframe
          title="Munchify Map"
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3963.1095659742064!2d3.5102375759242386!3d6.63331249336112!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x62f10c3d2a81695f%3A0xd690b8ac0905045a!2sMunchify%20Cakes%20and%20Dairy!5e0!3m2!1sen!2ske!4v1750842731083!5m2!1sen!2ske"
          width="500px"
          height="250"
          style={{ border: 0 }}
          allowFullScreen=""
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        ></iframe>
      </div>

      <hr />
      <p className="foter-copyright">
        Copyright 2024 @ Munchify.com - All Right Reserved.
      </p>
    </div>
  );
};

export default Footer;
