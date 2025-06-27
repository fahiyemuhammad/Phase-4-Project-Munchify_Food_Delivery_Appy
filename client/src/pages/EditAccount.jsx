import React, { useEffect, useState } from "react";
import "./EditAccount.css";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";

function EditAccount({ setIsLoggedIn }) {
  const token = localStorage.getItem("token");
  const storedUsername = localStorage.getItem("username");
  const navigate = useNavigate();

  const [initialValues, setInitialValues] = useState({
    username: "",
    password: "",
    confirmPassword: "",
  });

  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (storedUsername) {
      setInitialValues({
        username: storedUsername,
        password: "",
        confirmPassword: "",
      });
    }
  }, [storedUsername]);

  const validationSchema = Yup.object({
    username: Yup.string()
      .min(3, "Must be at least 3 characters")
      .required("Required"),
    password: Yup.string()
      .min(6, "Must be at least 6 characters")
      .required("Required"),
    confirmPassword: Yup.string()
      .oneOf([Yup.ref("password")], "Passwords must match")
      .required("Required"),
  });

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      const { username, password } = values;

      const res = await fetch("http://localhost:5000/auth/update", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("username", username);

        Swal.fire({
          title: "Success!",
          text: data.message,
          icon: "success",
          showConfirmButton: false,
          timer: 1500,
        }).then(() => {
          window.location.reload(); // reload page after update
        });

        resetForm({ values: { username, password: "", confirmPassword: "" } });
      } else {
        Swal.fire("Update Failed", data.error || "Try again later", "error");
      }
    } catch (err) {
      console.error(err);
      Swal.fire("Error", "Something went wrong", "error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    Swal.fire({
      title: "Are you sure?",
      text: "Your account will be permanently deleted!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Yes, delete it!",
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const res = await fetch("http://localhost:5000/auth/delete", {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          const data = await res.json();
          if (res.ok) {
            Swal.fire(
              "Deleted!",
              "Your account has been removed.",
              "success"
            ).then(() => {
              localStorage.removeItem("token");
              localStorage.removeItem("username");
              if (setIsLoggedIn) setIsLoggedIn(false);
              navigate("/");
            });
          } else {
            Swal.fire("Failed", data.error || "Try again later", "error");
          }
        } catch (err) {
          console.error(err);
          Swal.fire("Error", "Something went wrong", "error");
        }
      }
    });
  };

  if (!token) {
    return <p>Please log in to edit your account.</p>;
  }

  return (
    <div className="edit-account-container">
      <h2>Edit Account</h2>
      <Formik
        enableReinitialize
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form className="edit-form">
            <label>New Username</label>
            <Field name="username" type="text" />
            <ErrorMessage name="username" component="div" className="error" />

            <label>New Password</label>
            <div className="password-toggle-wrapper">
              <Field
                name="password"
                type={showPassword ? "text" : "password"}
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword((prev) => !prev)}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
            <ErrorMessage name="password" component="div" className="error" />

            <label>Confirm Password</label>
            <Field
              name="confirmPassword"
              type={showPassword ? "text" : "password"}
            />
            <ErrorMessage
              name="confirmPassword"
              component="div"
              className="error"
            />

            <button type="submit" disabled={isSubmitting}>
              Update Account
            </button>
          </Form>
        )}
      </Formik>

      <button className="delete-btn" onClick={handleDelete}>
        Delete Account
      </button>
    </div>
  );
}

export default EditAccount;
