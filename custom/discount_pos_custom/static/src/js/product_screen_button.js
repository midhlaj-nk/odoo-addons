odoo.define('pos_custom_buttons.DemoButton', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   class Discountonpos extends PosComponent {

constructor() {

super(...arguments);
useListener('click', this.onClick);

}

is_available() {

const order = this.env.pos.get_order();
return order

}

onClick() {

    Gui.showPopup("Discount_custom_popup", {
//title: this.env._t('Payment Screen Custom Button Clicked'),
//body: this.env._t('Welcome to OWL'),

});
}
}

   Discountonpos.template = 'Discountonpos';
   ProductScreen.addControlButton({
component: Discountonpos,
condition: function() {
return this.env.pos;
},
   });
   Registries.Component.add(Discountonpos);
   return Discountonpos;

});