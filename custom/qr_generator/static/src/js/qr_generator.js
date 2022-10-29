/** @odoo-module **/
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var QrWidget = Widget.extend({
   template: 'QrSystray',
   events: {
       'click #qr_gen': '_onClick',
   },
   _onClick: function(){
       this.do_action({
            type: 'ir.actions.act_window',
            name: 'qr code',
            res_model: 'qr.generator',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new'
       });
   },
});
SystrayMenu.Items.push(QrWidget);
export default QrWidget;