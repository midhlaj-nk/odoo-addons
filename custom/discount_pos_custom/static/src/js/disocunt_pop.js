/** @odoo-module **/
   import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
   import Registries from 'point_of_sale.Registries';
   import PosComponent from 'point_of_sale.PosComponent';
//   import { onChangeOrder } from 'point_of_sale.custom_hooks';

   class Discount_custom_popup extends AbstractAwaitablePopup {

    constructor() {
    super(...arguments);
    }

     confirm(){

        var product_discount = $("#discount").val();
        var order    = this.env.pos.get_order();
        var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
        var base_to_discount = order.get_total_without_tax();
        var discount_type = this.env.pos.config.discount_pos_cust

     console.log("this",discount_type)

        if(this.env.pos.config.discount_pos_cust=='percentage')
        {
           var discount_price = -product_discount/ 100.0 * base_to_discount;
           if( discount_price < 0 ){
                order.add_product(product, {
                    price: discount_price,
                });
           }
            this.cancel()
        }

        else
        {
            var discount_price = -product_discount

            if( discount_price < 0 ){
                order.add_product(product, {
                            price: discount_price,
                        });
                    }
            this.cancel()
        }


     }
     };
         Discount_custom_popup.template = 'Discount_custom_popup';
             Discount_custom_popup.defaultProps = {
            confirmText: 'Ok',
            cancelText: 'Close',
//            body: this.env._t('Your purchase limit is '+customer.purchase_limit_amount)
            title: 'Discount'
    };
   Registries.Component.add(Discount_custom_popup);
//   export default  Discount_custom_popup;
