odoo.define('dashboard_pos.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var web_client = require('web.web_client');
var _t = core._t;
var QWeb = core.qweb;
var i;
  var text = [];
  for (i = 0; i < 100; i++) {
    var a = Math.floor((Math.random() * 250));
    var b = Math.floor((Math.random() * 250));
    var c = Math.floor((Math.random() * 250));
    text.push("rgba("+a+", "+b+", "+c+", 1)");
}
var PosDashboard = AbstractAction.extend({
    template: 'PosDashboard',
    events: {
            'click #sales_orders'       : 'onclick_pos_order',
            'click #sales_product'      : 'onclick_product',
            'click #pos_orders_customer': 'onclick_pos_customer',
            'click #pos_categ_product'  : 'onclick_pos_categ_product',
            'click #pos_product'        : 'onclick_pos_product',
            'click #button_action'      : 'onclick_select_pos',
            'click #button_action'      : 'onclick_date_end',
            'click #pos_orders'         : 'onclick_chart_pos',  
            // 'change #date_start': 'onclick_date_start',
    },

    init: function(parent, context) {
        this._super(parent, context); 
        this.dashboards_templates = ['PosChart_Dashboard'];
        this.payment_details = [];
        this.top_salesperson = [];
        this.selling_product = [];
        this.total_sale = [];
    },



    start: function() {
        // setInterval(function () {document.getElementById("select_pos").click();}, 1000);
        var self = this;
        var pos = $('#select_pos').val();
        var date1 = "";
        var date2 = "";

        rpc.query({
          model: "pos.order",
          method: "get_date_now",
        }).then(function (arrays) {
          document.getElementById('date_end').setAttribute("value", arrays[1]);
          document.getElementById('date_start').setAttribute("value", arrays[0]);
        })

        rpc.query({
            model: "pos.order",
            method: "o_today_order",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_today_order').html(data);
        })

        rpc.query({
            model: "pos.order",
            method: "get_order",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_pos_order').html(data);
        })

        rpc.query({
            model: "pos.session",
            method: "get_session",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_pos_session').html(data);
        })

        rpc.query({
            model: "pos.order",
            method: "get_order_today",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_get_order_today').html(data);
        })

        rpc.query({
            model: "pos.order",
            method: "get_name_pos",
          }).then(function (data) {
          self.$('.o_select_pos').append(data);
        })
        // setInterval(function(){
        //    $('#pos_product.active_button').trigger("click");
        //    $('#pos_categ_product.active_button').trigger("click");
        //    $('#pos_orders_customer.active_button').trigger("click");
        //    $('#sales_orders.active_button').trigger("click");
        // },random(30000,60000));
        // function random(min,max){
        //   return min + (max - min) * Math.random()
        // }
        this.set("title", 'Dashboard');
        return this._super().then(function() {
            self.render_dashboards();
            self.render_graphs();
            self.$el.parent().addClass('oe_background_grey');
        });
    },


    render_dashboards: function() {
        var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_pos_dashboard').append(QWeb.render(template, {widget: self}));
            });
    },

    render_graphs: function(){
        var self = this;
        self.onclick_pos_order2();
        self.onclick_pos_customer2();
        self.onclick_pos_product2();
        self.onclick_pos_categ_product2();
        self.onclick_chart_pos2();
    },

    onclick_pos_product:function(events){
      // $("#date_start").val("");
      // $("#date_end").val("");
      var date1 = "";
      var date2 = "";
      var option = $('#pos_product.active_button').val()
      var pos = $('#select_pos').val();
      var self = this;
       rpc.query({
            model: "pos.order",
            method: "get_top_sales",
            args: [option,pos,date1,date2],
          }).then(function (data) {
          self.$('.o_data_top_product').html(data);
        })
    },

    onclick_pos_product2:function(){
      var date1 = "";
      var date2 = "";
      var pos = $('#select_pos').val();
      var option = "pos_monthly_product";
      var self = this;
       rpc.query({
            model: "pos.order",
            method: "get_top_sales",
            args: [option,pos,date1,date2],
          }).then(function (data) {
          self.$('.o_data_top_product').html(data);
        })
    },

    onclick_chart_pos:function(events){
      // $("#date_start").val("");
      // $("#date_end").val("");
      var date1 = "";
      var date2 = "";
      var self = this;
      var option = $('#pos_orders.active_button').val() 
      var pos = $('#select_pos').val();
      var ctx4 = self.$("#canvas_3");
          rpc.query({
                model: "pos.order",
                method: "get_pos_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
                  labels: arrays[1],
                  datasets: [{
                       label: 'Penjualan',
                       data: arrays[2], 
                       backgroundColor: "#03b6fc",
                       order: 2
                   }, {
                       label: 'Order',
                       data: arrays[0],
                       backgroundColor: "#f2f200",
                       type: 'line', 
                       order: 1
                   }],
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips: { 
                 mode: 'label', 
                 label: 'mylabel', 
                 callbacks: { 
                     label: function(tooltipItem, data) { 
                         return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
              },  
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

                //create Chart class object
                if (window.myCharts3 != undefined)
                window.myCharts3.destroy();
                window.myCharts3 = new Chart(ctx4, {
      //          var chart = new Chart(ctx, {
                  type: "line",
                  data: data,
                  options: options
                });
          })
    },

    onclick_chart_pos2:function(){
      // $("#date_start").val("");
      // $("#date_end").val("");
      var date1 = "";
      var date2 = "";
      var self = this;
      var option = "pos_monthly_sales" 
      var pos = $('#select_pos').val();
      var ctx4 = self.$("#canvas_3");
          rpc.query({
                model: "pos.order",
                method: "get_pos_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
                  labels: arrays[1],
                  datasets:[{
                       label: 'Penjualan',
                       data: arrays[2], 
                       backgroundColor: "#03b6fc",
                       order: 2
                   }, {
                       label: 'Order',
                       data: arrays[0],
                       backgroundColor: "#f2f200",
                       type: 'line', 
                       order: 1
                   }],
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips: { 
                 mode: 'label', 
                 label: 'mylabel', 
                 callbacks: { 
                     label: function(tooltipItem, data) { 
                         return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
              },  
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

                //create Chart class object
                if (window.myCharts3 != undefined)
                window.myCharts3.destroy();
                window.myCharts3 = new Chart(ctx4, {
      //          var chart = new Chart(ctx, {
                  type: "line",
                  data: data,
                  options: options
                });
          })
    },

    onclick_pos_categ_product:function(events){
      // $("#date_start").val("");
      // $("#date_end").val("");
      var date1 = "";
      var date2 = "";
      var self = this;
      var option = $('#pos_categ_product.active_button').val() 
      var pos = $('#select_pos').val();
      var ctx3 = self.$("#canvas_2");
          rpc.query({
                model: "pos.order",
                method: "get_product_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
                  labels: arrays[1],
                  datasets: [
                    {
                      label: arrays[0],
                      data: arrays[0],
                      backgroundColor: text,
                      borderWidth: 1
                    },

                  ]
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips:{ 
                   mode: 'label', 
                   label: 'mylabel',
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

                //create Chart class object
                if (window.myCharts2 != undefined)
                window.myCharts2.destroy();
                window.myCharts2 = new Chart(ctx3, {
      //          var chart = new Chart(ctx, {
                  type: "doughnut",
                  data: data,
                  options: options
                });
          })
    },
    
    onclick_pos_categ_product2:function(events){
      // $("#date_start").val("");
      // $("#date_end").val("");
      var date1 = "";
      var date2 = "";
      var self = this;
      var option = "pos_monthly_categ_product";   
      var pos = $('#select_pos').val();
      var ctx3 = self.$("#canvas_2");
          rpc.query({
                model: "pos.order",
                method: "get_product_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
                  labels: arrays[1],
                  datasets: [
                    {
                      label: arrays[0],
                      data: arrays[0],
                      backgroundColor: text,
                      borderWidth: 1
                    },

                  ]
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips: { 
                     mode: 'label', 
                     label: 'mylabel', 
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

                //create Chart class object
                if (window.myCharts2 != undefined)
                window.myCharts2.destroy();
                window.myCharts2 = new Chart(ctx3, {
      //          var chart = new Chart(ctx, {
                  type: "doughnut",
                  data: data,
                  options: options
                });
          })
    },

    onclick_pos_customer:function(events){
      // $("#date_start").val("");
      // $("#date_end").val("");
      var date1 = "";
      var date2 = "";
      var option = $('#pos_orders_customer.active_button').val()
      var pos = $('#select_pos').val();
      var self = this;
      rpc.query({
              model: "pos.order",
              method: "get_sale_by_salesman",
              args: [option,pos,date1,date2],
            }).then(function (data) {
            self.$('.o_sale_by_salesman').html(data);
          })
      },
  
    onclick_pos_customer2:function(){
      var date1 = "";
      var date2 = "";
      var pos = $('#select_pos').val();
      var option = "pos_monthly_customer";
      var self = this;
      rpc.query({
              model: "pos.order",
              method: "get_sale_by_salesman",
              args: [option,pos,date1,date2],
            }).then(function (data) {
            self.$('.o_sale_by_salesman').html(data);
          })
      },

     onclick_pos_order:function(events){
        // $("#date_start").val("");
        // $("#date_end").val("");
        var date1 = "";
        var date2 = "";
        var option = $('#sales_orders.active_button').val()
        var pos = $('#select_pos').val();
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "pos.order",
                method: "get_orders_chart",
                args: [option,pos,date1,date2],
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",

              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            }, tooltips: { 
           mode: 'label', 
           label: 'mylabel', 
           callbacks: { 
               label: function(tooltipItem, data) { 
                   return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
        }, 
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          if (window.myCharts1 != undefined)
          window.myCharts1.destroy();
          window.myCharts1 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "line",
            data: data,
            options: options
          });

        });
        },
    
    onclick_pos_order2:function(){
      var date1 = "";
      var date2 = "";
      console.log('came monthly')
      var self = this
      var pos = $('#select_pos').val();
      var option = "pos_monthly_sales";
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "pos.order",
                method: "get_orders_chart",
                args: [option,pos,date1,date2],
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor:text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",

              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            }, tooltips: { 
           mode: 'label', 
           label: 'mylabel', 
           callbacks: { 
               label: function(tooltipItem, data) { 
                   return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
        }, 
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          window.myCharts1 = new Chart(ctx, {
            type: "line",
            data: data,
            options: options
          });

        });
        },

        onclick_select_pos:function(){
          // var date1 = $('#date_start').val();
          // var date2 = $('#date_end').val();
          var pos = $('#select_pos').val();
          document.getElementById('pos_total_order').setAttribute("href", "point_of_sales/order/filter?session="+pos);
          document.getElementById('pos_today_order').setAttribute("href", "point_of_sale/today_order/filter?today="+pos);
          document.getElementById('pos_active_pos').setAttribute("href", "point_of_sale/active_session/filter?active=");
          document.getElementById('pos_today_product').setAttribute("href", "point_of_sale/product/filter?product=");

        rpc.query({
            model: "pos.order",
            method: "get_order",
              args: [pos,date1,date2],
          }).then(function (data) {
          self.$('.o_pos_order').html(data);
        })

           rpc.query({
            model: "pos.order",
            method: "o_today_order",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_today_order').html(data);
        })

        rpc.query({
            model: "pos.session",
            method: "get_session",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_pos_session').html(data);
        })

        rpc.query({
            model: "pos.order",
            method: "get_order_today",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_get_order_today').html(data);
        })

           var option1 = $('#pos_orders.active_button').removeClass('active_button'); 
          var ctx4 = self.$("#canvas_3");
          rpc.query({
                model: "pos.order",
                method: "get_pos_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
               datasets: [{
                       label: 'Penjualan',
                       data: arrays[2], 
                       backgroundColor: "#03b6fc",
                       order: 2
                   }, {
                       label: 'Order',
                       data: arrays[0],
                       backgroundColor: "#f2f200",
                       type: 'line', 
                       order: 1
                   }],
                   labels: arrays[1] 
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    // font: {
                    //     size: 18,
                    //   }
                  },tooltips: { 
                   mode: 'label', 
                   label: 'mylabel', 
                   callbacks: { 
                       label: function(tooltipItem, data) { 
                           return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };
 
                if (window.myCharts3 != undefined)
                window.myCharts3.destroy();
                window.myCharts3 = new Chart(ctx4, { 
                  type: "bar",
                  data: data,
                  options: options
                });
          })
          
          var option = $('#pos_product.active_button').val();
          var self = this;
           rpc.query({
                model: "pos.order",
                method: "get_top_sales",
                args: [option,pos,date1,date2],
              }).then(function (data) {
              self.$('.o_data_top_product').html(data);
            })


          var option = $('#pos_categ_product.active_button').val(); 
          var ctx3 = self.$("#canvas_2");
          rpc.query({
                model: "pos.order",
                method: "get_product_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
                  labels: arrays[1],
                  datasets: [
                    {
                      label: arrays[0],
                      data: arrays[0],
                      backgroundColor: text,
                      borderWidth: 1
                    },

                  ]
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips: { 
                     mode: 'label', 
                     label: 'mylabel',
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

                //create Chart class object
                if (window.myCharts2 != undefined)
                window.myCharts2.destroy();
                window.myCharts2 = new Chart(ctx3, {
      //          var chart = new Chart(ctx, {
                  type: "doughnut",
                  data: data,
                  options: options
                });
          })


          var option = $('#pos_orders_customer.active_button').val();
          var self = this;
          rpc.query({
                  model: "pos.order",
                  method: "get_sale_by_salesman",
                  args: [option,pos,date1,date2],
                }).then(function (data) {
                self.$('.o_sale_by_salesman').html(data);
              })


          var option = $('#sales_orders.active_button').val();
          console.log('came monthly')
          var self = this
          var ctx = self.$("#canvas_1");
              rpc.query({
                  model: "pos.order",
                  method: "get_orders_chart",
                  args: [option,pos,date1,date2],
              }).then(function (arrays) {
              console.log(arrays)
            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: arrays[2],
                  data: arrays[0],
                  backgroundColor: text,
                  borderWidth: 1
                },

              ]
            };

            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                
                fontSize: 18,
                fontColor: "#111"
              },
              legend: {
                display: true,
                position: "bottom",
                labels: {
                  fontColor: "#111",
                  fontSize: 16
                }
              },
              scales: {
                yAxes: [{
                  ticks: {
                    min: 0
                  }
                }]
              }
            };

            //create Chart class object
            if (window.myCharts1 != undefined)
            window.myCharts1.destroy();
            window.myCharts1 = new Chart(ctx, {
  //          var chart = new Chart(ctx, {
              type: "line",
              data: data,
              options: options
            });

          });

        },




      onclick_date_start:function(){
          var date1 = $('#date_start').val();
          document.getElementById('date_end').setAttribute("min", date1);
          var date2 = $('#date_end').val();
          document.getElementById('date_start').setAttribute("max", date2);
          var pos = $('#select_pos').val();
        },


        onclick_date_end:function(events){
          var date1 = $('#date_start').val();
          document.getElementById('date_end').setAttribute("min", date1);
          var date2 = $('#date_end').val();
          document.getElementById('date_start').setAttribute("max", date2);
          var pos = $('#select_pos').val();

           // TOday Produuct Sold
          rpc.query({
            model: "pos.order",
            method: "get_order_today",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_get_order_today').html(data);
        })
           // Today order
          rpc.query({
            model: "pos.order",
            method: "o_today_order",
            args: [pos, date1, date2],
          }).then(function (data) {
          self.$('.o_today_order').html(data);
        })
          //  TOtal order
          rpc.query({
            model: "pos.order",
            method: "get_order",
            args: [pos, date1, date2],
          }).then(function (data) {
            self.$('.o_pos_order').html(data);
          })

          var option = $('#pos_product.active_button').removeClass('active_button');
          var self = this;
           rpc.query({
                model: "pos.order",
                method: "get_top_sales",
                args: [option,pos,date1,date2],
              }).then(function (data) {
              self.$('.o_data_top_product').html(data);
            })


          var option = $('#pos_categ_product.active_button').removeClass('active_button'); 
          var ctx3 = self.$("#canvas_2");
          rpc.query({
                model: "pos.order",
                method: "get_product_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
                  labels: arrays[1],
                  datasets: [
                    {
                      label: arrays[0],
                      data: arrays[0],
                      backgroundColor: text,
                      borderWidth: 1
                    },

                  ]
                };  

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips: { 
                   mode: 'label', 
                   label: 'mylabel',
                  },  
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

                //create Chart class object
                if (window.myCharts2 != undefined)
                window.myCharts2.destroy();
                window.myCharts2 = new Chart(ctx3, {
      //          var chart = new Chart(ctx, {
                  type: "doughnut",
                  data: data,
                  options: options
                });
          })

          var option1 = $('#pos_orders.active_button').removeClass('active_button'); 
          var ctx4 = self.$("#canvas_3");
          rpc.query({
                model: "pos.order",
                method: "get_pos_chart",
                args: [option,pos,date1,date2],
              }).then(function (arrays) { 
            var data = {
               datasets: [{
                       label: 'Penjualan',
                       data: arrays[2], 
                       backgroundColor: "#03b6fc",
                       order: 2
                   }, {
                       label: 'Order',
                       data: arrays[0],
                       backgroundColor: "#f2f200",
                       type: 'line', 
                       order: 1
                   }],
                   labels: arrays[1] 
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    font: {
                        size: 18,
                      }
                  },tooltips: { 
                   mode: 'label', 
                   label: 'mylabel', 
                   callbacks: { 
                       label: function(tooltipItem, data) { 
                           return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };
 
                if (window.myCharts3 != undefined)
                window.myCharts3.destroy();
                window.myCharts3 = new Chart(ctx4, { 
                  type: "bar",
                  data: data,
                  options: options
                });
          })


          var option = $('#pos_orders_customer.active_button').removeClass('active_button');
          var self = this;
          rpc.query({
                  model: "pos.order",
                  method: "get_sale_by_salesman",
                  args: [option,pos,date1,date2],
                }).then(function (data) {
                self.$('.o_sale_by_salesman').html(data);
              })


          if($('#sales_orders.active_button').val() != 'pos_hourly_sales' && $('#sales_orders.active_button').val() != 'pos_monthly_sales'){
            $('#sales_orders.active_button').removeClass('active_button');
          }
          var option = $('#sales_orders.active_button').val()
          console.log('came monthly')
          var self = this
          var ctx = self.$("#canvas_1");
              rpc.query({
                  model: "pos.order",
                  method: "get_orders_chart",
                  args: [option,pos,date1,date2],
              }).then(function (arrays) {
              // console.log(arrays)
            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: arrays[2],
                  data: arrays[0],
                  backgroundColor: text,
                  borderWidth: 1
                },

              ]
            };


            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                fontSize: 18,
                fontColor: "#111"
              },
              legend: {
                display: true,
                position: "bottom",
                labels: {
                  fontColor: "#111",
                  fontSize: 16
                }
              },tooltips: { 
                 mode: 'label', 
                 label: 'mylabel', 
                 callbacks: { 
                     label: function(tooltipItem, data) { 
                         return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
              }, 
              scales: {
                yAxes: [{
                  ticks: {
                    min: 0
                  }
                }]
              }
            };

            //create Chart class object
            if (window.myCharts1 != undefined)
            window.myCharts1.destroy();
            window.myCharts1 = new Chart(ctx, {
  //          var chart = new Chart(ctx, {
              type: "line",
              data: data,
              options: options
            });

          });


        },


});

core.action_registry.add('pos_dashboard', PosDashboard);

return PosDashboard;

}); 