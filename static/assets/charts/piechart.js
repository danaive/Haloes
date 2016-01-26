function test(idx, data, height) {

  var placeholder = $('#' + idx).css({ 'width': '90%', 'min-height': height + 'px' });

  function drawPieChart(placeholder, data, position) {

    $.plot(placeholder, data, {
      series: {
        pie: {
          radius: 1,
          show: true,
          tilt: 0.8,
          highlight: {
            opacity: 0.25
          },
          stroke: {
            color: '#fff',
            width: 2
          },
          startAngle: 2,
          label: {
            show: true,
            radius: 3 / 5,
            formatter: function (label, series) {
              console.log(series.data[0][1]);
              return '<div style="font-size: 8pt; text-align: center; padding: 2px; color: #fff;">' + label + '<br />' + Math.round(series.data[0][1]) + '</div>';
            },
            // background: {
            //   opacity: 0.5,
            //   color: "#000"
            // }
          }
        }
      },
      legend: {
        show: true,
        position: position || "ne",
        labelBoxBorderColor: null,
        margin: [-30, 15]
      },
      grid: {
        hoverable: true,
        clickable: true
      }
    })
  }
  drawPieChart(placeholder, data);
  var $tooltip = $("<div class='tooltip top in'><div class='tooltip-inner'></div></div>").hide().appendTo('body');
  var previousPoint = null;

  placeholder.on('plothover', function (event, pos, item) {
		if (item) {
      if (previousPoint != item.seriesIndex) {
        previousPoint = item.seriesIndex;
        var tip = item.series['label'] + " :<br /> " + item.series['data'][0][1];
        $tooltip.show().children(0).html(tip);
      }
      $tooltip.css({ top: pos.pageY + 10, left: pos.pageX + 10 });
		} else {
      $tooltip.hide();
      previousPoint = null;
		}
  });
}