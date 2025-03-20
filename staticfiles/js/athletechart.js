const plugin = {
    id: 'customCanvasBackgroundColor',
    beforeDraw: (chart, args, options) => {
      const {ctx} = chart;
      ctx.save();
      ctx.globalCompositeOperation = 'destination-over';
      ctx.fillStyle = options.color || '#99ffff';
      ctx.fillRect(0, 0, chart.width, chart.height);
      ctx.restore();
    }
  };
  
var q_config = {
    type: 'line',
    data: {
        labels: {{ q_labels }},
        datasets: [{
            data: {{ q_data1 }},
            label: "{{q_data1_label}}",
            borderColor: "#282761",
            backgroundColor: "#282761",
            fill: false,
            tension: 0
        }, {
            data: {{ q_data2 }},
            label: "{{q_data2_label}}",
            borderColor: "#DC0D17",
            backgroundColor: "#DC0D17",
            fill: false,
            tension: 0
        }]},
    options: {
        plugins: {
            title: {
                display: function(ctx) {
                    return ctx.chart.width > 500
                },
                text: '{{q_chart_title}}',
                font: {
                    size: 16
                }
            },
            subtitle: {
                display: function(ctx) {
                    return ctx.chart.width > 500
                },
                text: '{{q_chart_subtitle}}',
                padding: {
                    bottom:10
                }
            },
            customCanvasBackgroundColor: {
              color: 'white',
            }
          },
          scales: {
          x: {
              title: {
                display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{q_chart_x_title}}'
              }
          }
      }
        },
        plugins: [plugin],
  };
  
var f_config = {
        type: 'line',
        data: {
          labels: {{ f_labels }},
          datasets: [{
              data: {{ f_data1 }},
              label: "{{f_data1_label}}",
              borderColor: "#282761",
              backgroundColor: "#282761",
              fill: false,
              tension: 0
            }, {
              data: {{ f_data2 }},
              label: "{{f_data2_label}}",
              borderColor: "#DC0D17",
              backgroundColor: "#DC0D17",
              fill: false,
              tension: 0
          }]},
        options: {
          plugins: {
            title: {
                  display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{f_chart_title}}',
                  font: {
                     size: 16
                    }
              },
              subtitle: {
                display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{f_chart_subtitle}}',
                  padding: {
                      bottom:10
                  }
              },
            customCanvasBackgroundColor: {
              color: 'white',
            }
          },
          scales: {
          x: {
              title: {
                display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{f_chart_x_title}}'
              }
          }
      }
        },
        plugins: [plugin],
  };
  
var e_config = {
        type: 'line',
        data: {
          labels: {{ e_labels }},
          datasets: [{
              data: {{ e_data1 }},
              label: "{{e_data1_label}}",
              borderColor: "#282761",
              backgroundColor: "#282761",
              fill: false,
              tension: 0
            }, {
              data: {{ e_data2 }},
              label: "{{e_data2_label}}",
              borderColor: "#DC0D17",
              backgroundColor: "#DC0D17",
              fill: false,
              tension: 0
          }]},
        options: {
          plugins: {
            title: {
                  display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{e_chart_title}}',
                  font: {
                     size: 16
                    }
              },
              subtitle: {
                display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{e_chart_subtitle}}',
                  padding: {
                      bottom:10
                  }
              },
            customCanvasBackgroundColor: {
              color: 'white',
            }
          },
          scales: {
          x: {
              title: {
                display: function(ctx) {
                      return ctx.chart.width > 500
                  },
                  text: '{{e_chart_x_title}}'
              }
          }
      }
        },
        plugins: [plugin],
    };
  
  
window.onload = function() {
      ish = true;
  
      var myVar = "{{ q_data2_label }}";
      if(myVar.length > 0) {
        var ctx4 = document.getElementById('q-line-chart').getContext('2d');
        window.myPie4 = new Chart(ctx4, q_config);
      }
  
      var myVar = "{{ f_data2_label }}";
      if(myVar.length > 0) {
        var ctx1 = document.getElementById('f-line-chart').getContext('2d');
        window.myPie1 = new Chart(ctx1, f_config);
      }
  
      var myVar = "{{ e_data2_label }}";
      if(myVar.length > 0) {
        var ctx2 = document.getElementById('e-line-chart').getContext('2d');
        window.myPie2 = new Chart(ctx2, e_config);
      }
  
};
