/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#071018",
        panel: "#0d1824",
        shell: "#101f30",
        steel: "#97a9bc",
        mist: "#d8e4ef",
        mint: "#4ad4a0",
        ember: "#f3a941",
        rose: "#ff6e7d",
        sky: "#73c7ff",
        cobalt: "#3b82f6",
        gold: "#dfbf78",
      },
      boxShadow: {
        panel: "0 28px 80px rgba(1, 8, 20, 0.42)",
        float: "0 18px 40px rgba(2, 12, 27, 0.28)",
      },
      fontFamily: {
        display: ["Garamond", "Times New Roman", "serif"],
        body: ["Trebuchet MS", "Segoe UI", "Tahoma", "sans-serif"],
      },
      backgroundImage: {
        grid: "linear-gradient(rgba(145,164,189,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(145,164,189,0.08) 1px, transparent 1px)",
      },
      animation: {
        "float-slow": "floatSlow 9s ease-in-out infinite",
        "pulse-glow": "pulseGlow 4s ease-in-out infinite",
        "fade-rise": "fadeRise 0.7s ease-out",
      },
      keyframes: {
        floatSlow: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-10px)" },
        },
        pulseGlow: {
          "0%, 100%": { boxShadow: "0 0 0 rgba(115, 199, 255, 0.0)" },
          "50%": { boxShadow: "0 0 28px rgba(115, 199, 255, 0.28)" },
        },
        fadeRise: {
          "0%": { opacity: "0", transform: "translateY(18px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
