/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        'proof-bg': '#0a0a0a',
        'proof-surface': '#1a1a2e',
        'proof-text': '#f0f0f0',
        'proof-muted': '#888888',
        'proof-accent': '#c9a84c',
      },
    },
  },
  plugins: [],
};
