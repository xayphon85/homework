import React, { useContext } from "react";
import { ThemeContext } from "../context/ThemeContext";

export default function Button({ value, onClick, variant = "num" }) {
  const { theme } = useContext(ThemeContext);

  const baseClasses =
    "flex items-center justify-center cursor-pointer select-none active:scale-95 transition-transform rounded-full font-semibold";

  const variantClasses = {
    op: theme === "light" ? "bg-orange-500 text-white" : "bg-orange-400 text-black",
    func: theme === "light" ? "bg-gray-400 text-white" : "bg-gray-700 text-white",
    num: theme === "light" ? "bg-gray-600 text-white" : "bg-gray-900 text-white",
  };

  return (
    <button
      type="button"
      onClick={() => onClick(value)}
      className={`${baseClasses} ${variantClasses[variant]} h-14 w-14 text-xl`}
    >
      {value}
    </button>
  );
}
