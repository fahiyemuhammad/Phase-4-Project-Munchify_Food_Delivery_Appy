import { createContext, useState } from "react";
import { food_list } from "../assets/assets";

export const StoreContext = createContext(null);

const StoreContextProvider = (props) => {
  const [cartItems, setCartItems] = useState({});

  const addToCart = (itemId) => {
    setCartItems((prev) => ({
      ...prev,
      [itemId]: (prev[itemId] || 0) + 1,
    }));
  };

  const removeFromCart = (itemId) => {
    setCartItems((prev) => {
      const updated = { ...prev };
      updated[itemId] = (updated[itemId] || 1) - 1;
      if (updated[itemId] <= 0) delete updated[itemId];
      return updated;
    });
  };

  const clearCart = () => setCartItems({});

  const getTotalCartAmount = () => {
    let total = 0;
    for (const id in cartItems) {
      const product = food_list.find((item) => item._id.toString() === id);
      if (product) total += product.price * cartItems[id];
    }
    return total;
  };

  return (
    <StoreContext.Provider
      value={{
        cartItems,
        setCartItems,
        food_list,
        addToCart,
        removeFromCart,
        getTotalCartAmount,
        clearCart,
      }}
    >
      {props.children}
    </StoreContext.Provider>
  );
};

export default StoreContextProvider;
