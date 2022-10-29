odoo.define("vehicle_rental.main", function (require) {
    "use strict";
        var ajax = require('web.ajax');
//            console.log("function1")
    $("#vehicleid").change(function(){
//    var vehicle = $('#vehicleid').val();
//    console.log(vehicle)
    _change(ajax)
    return ;
    });

});


function _change(ajax){
    console.log("ajaxfunct")
    var vehicle = $('#vehicleid').val();
    var period = $("#periodid").val();
    ajax.rpc('/onchange', {vehicle,period}).then(function (res) {
                var test = res
                $('#periodid').empty()
                $(test).each(function(i){
                $('#periodid').append("<option value=" + test[i].id + ">" + test[i].ptype  + "</option>");
//                $('#periodid').append("<option>" + test[i].id + "</option>");
//                $('#invoice_id').append("<option value=" + test[i] + ">" + test[i].ptype  + "</option>");
                });

            });
    };

