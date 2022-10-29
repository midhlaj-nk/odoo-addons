odoo.define('spanish_product.pos', function(require){
    'use strict';
    var models = require('point_of_sale.models');
    var _super_product = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes){
            var self = this;
            models.load_fields('product.product', ['spanish_product']);
            _super_product.initialize.apply(this, arguments);
        }
    });
});
odoo.define('spanish_product.receipt', function(require){
    "use strict";
    var models = require('point_of_sale.models');
    models.load_fields('product.product', 'spanish_product');
    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function(){
            var line = _super_orderline.export_for_printing.apply(this, arguments);
            line.spanish_product = this.get_product().spanish_product;
            return line;
        }
    });
});







//odoo.define('spanish_product.pos', function (require) {
//    'use strict';
//    console.log("works")
//    var models = require('point_of_sale.models');
//    var _super_orderline = models.Orderline.prototype;
//    console.log("models",models);
//    models.load_fields('product.product', 'spanish_product');
//    models.Orderline = models.Orderline.extend({
//        initialize:function(attr,options){
//            var line=_super_orderline.initialize.apply(this,arguments);
//            this.spanish_product=this.product.spanish_product;
//            console.log("sp",this.spanish_product)
//            }
//        })
//});

