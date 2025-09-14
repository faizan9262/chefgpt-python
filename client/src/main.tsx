import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import axios from "axios";
import { Toaster } from "sonner";
import { DishContextProvider } from "./Context/DishContext.tsx";
import { AuthProvider } from "./Context/AuthContext.tsx";

// axios.defaults.baseURL = "http://localhost:8000";
axios.defaults.baseURL = "https://3d0c7802bfd2.ngrok-free.app";
// axios.defaults.baseURL = "https://chef-gpt-ai-server.vercel.app/api";
axios.defaults.withCredentials = true;

createRoot(document.getElementById("root")!).render(
  // <StrictMode>
  <>
    <AuthProvider>
      <DishContextProvider>
        <App />
      </DishContextProvider>
    </AuthProvider>
    <Toaster position="top-right" />
  </>
  // </StrictMode>
);
