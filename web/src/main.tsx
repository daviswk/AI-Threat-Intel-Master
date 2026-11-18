import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

// Fonts are bundled with the app. Nothing is fetched from the network at runtime.
import "@fontsource/ibm-plex-sans/400.css";
import "@fontsource/ibm-plex-sans/500.css";
import "@fontsource/ibm-plex-sans/600.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "./styles/app.css";

import App from "./App";

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
