import Calculator from "./components/Calculator";
import { ThemeProvider } from "./context/ThemeContext";

export default function App() {
  return (
    <ThemeProvider>
      <Calculator />
    </ThemeProvider>
  );
}
