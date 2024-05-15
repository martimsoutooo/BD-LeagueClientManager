/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/src/**/*.{html,js,htmx}"],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
}

