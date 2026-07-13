module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        hig: {
          ink: "#080A0F",
          gold: "#1279D7",
          mist: "#F4F8FD",
          blue: "#1279D7"
        }
      },
      fontFamily: {
        sans: ["Inter", "Tajawal", "Arial", "sans-serif"]
      }
    }
  },
  safelist: [
    "h-8",
    "h-14",
    "h-24",
    "h-[420px]",
    "min-h-[72vh]",
    "min-h-[76vh]"
  ],
  plugins: []
}
