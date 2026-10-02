import 'vite/modulepreload-polyfill'; // vite's doc suggestion
import "../css/style.css";
import htmx from "htmx.org";
import "htmx.org/dist/ext/hx-alpine-compat";
import Alpine from "alpinejs";

// datatables
import moment from 'moment';
import jszip from 'jszip';
import pdfmake from 'pdfmake';
import 'datatables.net-key-validator-shim';
import DataTable from 'datatables.net-dt';
import 'datatables.net-autofill-dt';
import 'datatables.net-buttons-dt';
import 'datatables.net-colreorder-dt';
import 'datatables.net-columncontrol-dt';
import DateTime from 'datatables.net-datetime';
import 'datatables.net-fixedcolumns-dt';
import 'datatables.net-fixedheader-dt';
import 'datatables.net-keytable-dt';
import 'datatables.net-responsive-dt';
import 'datatables.net-rowgroup-dt';
import 'datatables.net-rowreorder-dt';
import 'datatables.net-scroller-dt';
import 'datatables.net-searchbuilder-dt';
import 'datatables.net-select-dt';
DataTable.Buttons.jszip(jszip);
DataTable.Buttons.pdfMake(pdfmake);

// extensions must go here, between Alpine global import and initializing it

window.Alpine = Alpine;
Alpine.start();

window.htmx = htmx;
let table = new DataTable('#myTable', {
    processing: true,
    serverSide: true,
    ajax: {
        url: "/provide-data",
        type: "GET",
        error: function(error) {
            console.log(error);
        },
    },
    columns: [
        { data: 'id' },
        { data: 'name' },
        { data: 'category_id' },
        { data: 'in_stock' },
        { data: 'available' },
        { data: 'price' },
    ],
});
console.log('main.js file loaded.');