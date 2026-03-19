/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#08111f",
        panel: "#0f1b2d",
        steel: "#91a4bd",
        mint: "#43d69d",
        ember: "#ffb454",
        rose: "#ff7f8e",
        sky: "#6ec7ff",
      },
      boxShadow: {
        panel: "0 24px 80px rgba(2, 12, 27, 0.35)",
      },
      fontFamily: {
        display: ["Georgia", "Cambria", "Times New Roman", "serif"],
        body: ["Segoe UI", "Tahoma", "Geneva", "Verdana", "sans-serif"],
      },
      backgroundImage: {
        grid: "linear-gradient(rgba(145,164,189,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(145,164,189,0.08) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};
