// src/pages/AccountPage.jsx
import React from "react";
import EditAccount from "./EditAccount"; // assuming it's in the same folder
import "./AccountPage.css";

function AccountPage({ setIsLoggedIn }) {
  return (
    <div className="account-page">
      <h2>Account Settings</h2>

      <section className="edit-section">
        <EditAccount setIsLoggedIn={setIsLoggedIn} />
      </section>
    </div>
  );
}

export default AccountPage;
