import { useState, useEffect, useContext } from "react";
import Button from "./Button";
import { ThemeContext } from "../context/ThemeContext";

const API_BASE = "http://localhost:8000";

export default function Calculator() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const [input, setInput] = useState("");
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch history when component mounts
  useEffect(() => {
    fetchHistory();
  }, []);

  async function fetchHistory() {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/history?limit=50`);
      const data = await res.json();
      setHistory(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleCalculate() {
    try {
      const expr = input.replaceAll("÷", "/").replaceAll("×", "*").replaceAll("−", "-");
      const res = await fetch(`${API_BASE}/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expr }),
      });
      const data = await res.json();
      if (data.ok) {
        setInput(String(data.result));
        fetchHistory();
      } else {
        setInput("Error");
      }
    } catch {
      setInput("Error");
    }
  }

  async function clearHistory() {
    try {
      await fetch(`${API_BASE}/history`, { method: "DELETE" });
      setHistory([]);
    } catch (err) {
      console.error("Failed to clear history:", err);
    }
  }

  const handleClick = (value) => {
    if (value === "AC") return setInput("");
    if (value === "⌫") return setInput((cur) => cur.slice(0, -1));
    if (value === "=") return handleCalculate();

    setInput((cur) => (cur === "Error" ? value : cur + value));
  };

  const buttons = [
    { label: "⌫", variant: "func" },
    { label: "AC", variant: "func" },
    { label: "%", variant: "func" },
    { label: "±", variant: "func" },
    { label: "7", variant: "num" },
    { label: "8", variant: "num" },
    { label: "9", variant: "num" },
    { label: "÷", variant: "op" },
    { label: "4", variant: "num" },
    { label: "5", variant: "num" },
    { label: "6", variant: "num" },
    { label: "×", variant: "op" },
    { label: "1", variant: "num" },
    { label: "2", variant: "num" },
    { label: "3", variant: "num" },
    { label: "-", variant: "op" },
    { label: "0", variant: "num" },
    { label: ".", variant: "num" },
    { label: "=", variant: "op" },
    { label: "+", variant: "op" },
  ];

  const bg = theme === "light" ? "bg-gray-200 text-black" : "bg-gray-900 text-white";

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center ${bg}`}>
      {/* Theme Toggle */}
      <div className="flex justify-end w-full max-w-xs mb-3 pr-4">
        <button onClick={toggleTheme} className="text-2xl">
          {theme === "light" ? "🌙" : "☀️"}
        </button>
      </div>

      <div className="bg-gray-800 rounded-3xl p-6 w-[320px] shadow-lg">
        {/* Display */}
        <div className="text-right text-4xl mb-6 min-h-[50px] overflow-x-auto bg-gray-700 px-3 py-2 rounded-lg">
          {input || "0"}
        </div>

        {/* Buttons */}
        <div className="grid grid-cols-4 gap-4">
          {buttons.map(({ label, variant }) => (
            <Button key={label} value={label} onClick={handleClick} variant={variant} />
          ))}
        </div>

        {/* History */}
        <div className="mt-4 text-sm">
          <h3 className="font-semibold mb-1">History</h3>
          {loading ? (
            <p>Loading...</p>
          ) : history.length === 0 ? (
            <p className="text-gray-400">No history yet.</p>
          ) : (
            <ul className="max-h-28 overflow-y-auto space-y-1">
              {history.map((item, i) => (
                <li key={i} className="border-b border-gray-600 pb-1">
                  {item.expr} = {item.result}
                </li>
              ))}
            </ul>
          )}
          <div className="flex justify-center mt-2">
            <Button value="Clear" onClick={clearHistory} variant="func" />
          </div>
        </div>
      </div>
    </div>
  );
}
