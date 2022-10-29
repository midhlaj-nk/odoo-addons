odoo.define('elearning_snippet.snippet', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   console.log("hey")
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.elearning_snippet',
       start: function () {
           var self = this;
           rpc.query({
               route: '/fetchcourse',
               params: {},
           }).then(function (result) {
               self.$('#course_name1').text(result[0].course);
               self.$('#description_1').html(result[0].description);
               self.$('#image_1').html("<img src='data:image/png;base64," + (result[0].image) + "'/>");
               var link1 = result[0].course
               key1=link1.replace(/ /g, "-");
//               console.log(key)
               self.$('#href1').append('<a href=slides/' + key1 + '-' +result[0].id+ '>' + '<button class="btn btn-primary btn_cta"" >Go to Course</button> ' + '</a>');

               self.$('#course_name2').text(result[1].course);
               self.$('#description_2').html(result[1].description);
               self.$('#image_2').html("<img src='data:image/png;base64," + (result[1].image) + "'/>");
               var link2 = result[1].course
               key2=link2.replace(/ /g, "-");
               self.$('#href2').append('<a href=slides/' + key2 + '-' +result[1].id+ '>' + '<button class="btn btn-primary btn_cta"" >Go to Course</button> ' + '</a>');

               self.$('#course_name3').text(result[2].course);
               self.$('#description_3').html(result[2].description);
               self.$('#image_3').html("<img src='data:image/png;base64," + (result[2].image) + "'/>");
               var link3 = result[2].course
               key3=link3.replace(/ /g, "-");
               self.$('#href3').append('<a href=slides/' + key3 + '-' +result[2].id+ '>' + '<button class="btn btn-primary btn_cta"" >Go to Course</button> ' + '</a>');


           });
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});


