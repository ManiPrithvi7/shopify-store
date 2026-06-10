module.exports = {
  content: ['./**/*.liquid', './frontend/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
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
