// Add this at the beginning of your app entry.
import 'vite/modulepreload-polyfill';
import "../css/style.css";
import htmx from "htmx.org";

window.htmx = htmx;

console.log('main.js file loaded.');