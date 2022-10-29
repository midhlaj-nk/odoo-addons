//odoo.define('stock_availability.test', function (require) {
//'use strict';
//
//const {Markup} = require('web.utils');
//var VariantMixin = require('sale.VariantMixin');
//var publicWidget = require('web.public.widget');
//var ajax = require('web.ajax');
//var core = require('web.core');
//var QWeb = core.qweb;
//
//const loadXml = async () => {
//    return ajax.loadXML('/stock_availability/view/stock_availability.xml', QWeb);
//};
//
//require('website_sale.website_sale');
//
//
//    loadXml().then(function (result) {
//        $('.oe_website_sale')
//            .find('.availability_message_' + combination.product_template)
//            .remove();
//        combination.has_out_of_stock_message = $(combination.out_of_stock_message).text() !== '';
//        console.log("here")
//        combination.out_of_stock_message = Markup(combination.out_of_stock_message);
//        const $message = $(QWeb.render(
//            'website_sale_stock.product_availability',
//            combination
//        ));
//        $('#testms').html($message);
//    });
// });