import 'vite/modulepreload-polyfill'; // vite's doc suggestion
import "../css/style.css";
import htmx from "htmx.org";
import "htmx.org/dist/ext/hx-alpine-compat";
import Alpine from "alpinejs";

// extensions must go here, between Alpine global import and initializing it

window.Alpine = Alpine;
Alpine.start();

window.htmx = htmx;
console.log('main.js file loaded.');