import 'vite/modulepreload-polyfill'; // vite's doc suggestion
import "../css/style.css";
import htmx from "htmx.org";

window.htmx = htmx;
console.log('main.js file loaded.');