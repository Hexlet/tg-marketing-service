import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@mantine/core/styles.css";
import App from "./app/App.tsx";
import "vite/modulepreload-polyfill";
import { createInertiaApp } from "@inertiajs/react";

createRoot(document.getElementById("root")!).render(
 <StrictMode>
  <App />
 </StrictMode>,
);
document.addEventListener("DOMContentLoaded", () => {
 createInertiaApp({
  resolve: (name: string) => {
   switch (name) {
    case "Home":
     return import("./components/pages/LandingPage.tsx").then((m) => m.default);
    case "Auth":
     return import("./components/pages/Auth.tsx").then((m) => m.default);
    case "ComparePages":
     return import("./components/pages/ComparePage.tsx").then((m) => m.default);
    case "MassParsing":
     return import("./components/pages/Channels.tsx").then((m) => m.default);
    case "PasswordRecovery":
     return import("./components/modals/PasswordRecovery.tsx").then(
      (m) => m.default,
     );
    case "Header":
     return import("./components/Layout/Header.tsx").then((m) => m.default);
    case "Layout":
     return import("./components/Layout/Layout.tsx").then((m) => m.default);
    case "FormRegistration":
     return import("./components/ui/FormRegistration.tsx").then(
      (m) => m.default,
     );
    default:
     throw new Error(`Page ${name} not found`);
   }
  },
  setup({ el, App, props }) {
   const root = createRoot(el);
   root.render(<App {...props} />);
  },
 });
});
