$ ->
  $('a[href$="group/"]').addClass 'current'
  # charts
  score = []
  $.ajax
    url: '/person/get-score/'
    type: 'post'
    dataType: 'json'
    data:
      username: 'danlei'
    success: (data) ->
      # pie chart
      score = data.score
      label = ['PWN', 'REVERSE', 'WEB', 'CRYPTO', 'MISC']
      color = ['#3BAFDA', '#8CC152', '#ED5565', '#37BC9B', '#FFCE54']
      # color = ['#68BC31', '#2091CF', '#AF4E96', '#DA5430', '#FFA400']
      highlight = ['#4FC3EE', '#A0D566', '#FF6979', '#4BD0AF', '#FFE268']
      pdata = ({
        label: label[i],
        value: score[i],
        color: color[i],
        highlight: highlight[i]
      } for _, i in label)
      pctx = $("#pieChart").get(0).getContext '2d'
      new Chart(pctx).Pie pdata, {animateScale: true}

      # radar chart
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
      rctx = $('#radarChart').get(0).getContext '2d'
      new Chart(rctx).Radar(
        rdata
        scaleOverride: true
        scaleSteps: 5
        scaleStepWidth: 25
        scaleStartValue: -25
      )
  $('#deadline').datetimepicker(
    format: 'yyyy-mm-dd'
    autoclose: true
    minView: 2
    maxView: 2
  ).on 'changeDate', (ev) ->
    console.log ev.date
  stickFooter()
