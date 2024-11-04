/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        raleway: ["Raleway", "sans-serif"],
        dancing: ['Dancing Script', 'sans-serif'],
        amaticBold: ["AmaticSC-Bold", "sans-serif"],
        amaticRegular: ["AmaticSC-Regular", "sans-serif"],
        merriweatherRegular: ["Merriweather-Regular", "serif"],
        merriweatherBoldItalic: ["Merriweather-BoldItalic", "serif"],
        quicksand: ["Quicksand", "sans-serif"],
        gothic: ["GothicA1", "sans-serif"],
        pacifico: ["Pacifico", "cursive"],
        lobster: ['LobsterTwo-Regular', 'cursive'],
        lobsterBold: ["LobsterTwo-Bold", "cursive"],
        lobsterBoldItalic: ["LobsterTwo-BoldItalic", "sans-serif"],
        lobsterItalic: ["LobsterTwo-Italic", "sans-serif"],
      },
      scrollBehavior: {
        smooth: 'smooth',
      },
    
    },
  },
  plugins: [
    require("flowbite/plugin"),
],
};
