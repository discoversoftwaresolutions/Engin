const config = {
  server: {
    headless: true,
    port: 8501,
    enableCORS: true,
    enableXsrfProtection: true,
    enableWebsocketCompression: true,
    fileWatcherType: "auto",
  },
  theme: {
    base: "light",
    primaryColor: "#005bbb",
    backgroundColor: "#ffffff",
    secondaryBackgroundColor: "#f0f2f6",
    textColor: "#262730",
    font: "sans-serif",
  },
};

export default config;
