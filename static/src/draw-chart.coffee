$ ->
  score = []
  $.ajax
    url: 'getscore/'
    dataType: 'json'
    success: (data) ->
      score = data.score
      label = ['PWN', 'REVERSE', 'WEB', 'CRYPTO', 'MISC']
      # color = ['#D1DBE5', '#9BA9B3', '#B9D8FF', '#A7CFFF', '#95B7CD']
      color = ['#68BC31', '#2091CF', '#AF4E96', '#DA5430', '#FFA400']
      highlight = ['#7CD045', '#34A5E3', '#C362AA', '#EE6844', '#FFB814']
      pdata = ({
        label: label[i],
        value: score[i],
        color: color[i],
        highlight: highlight[i]
      } for _, i in label)
      pctx = $("#pieChart").get(0).getContext('2d')
      new Chart(pctx).Pie(pdata, {
        animateScale: true
      });

      capacity = data.capacity
      rgba = ['rgba(137,114,158,1)', 'rgba(151,187,205,1)']
      rdata = {
        labels: label
        datasets: ({
          label: capacity[i].name
          fillColor: rgba[i][..-3] + '0.2)'
          pointColor: rgba[i]
          pointStrokeColor: '#fff'
          pointHighlightFill: '#fff'
          pointHighlightStroke: rgba[i]
          data: capacity[i].score
        } for _, i in capacity)
      }
      rctx = $('#radarChart').get(0).getContext('2d')
      new Chart(rctx).Radar(rdata, {})
