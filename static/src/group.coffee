$ ->
  $('a[href$="group/"]').addClass 'current'
  $('[data-toggle="tooltip"]').tooltip()
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


  $('#deadline').datetimepicker
    format: 'yyyy-mm-dd'
    autoclose: true
    minView: 2
    maxView: 2


  $('a.memberName').on 'click', ->
    $('#assign').text $(@).text()

  $('#newTaskBtn').on 'click', ->
    $('#taskContent').val ''
    $('#deadline').val ''
    $('#assign').text 'Unassigned'
    $('#assign').attr 'data-content', 0
    $('#newTask').fadeToggle()

  $('#taskAssign').on 'click', ->
    if $('#taskContent').val()
      data =
        content: $('#taskContent').val()
        assign: $('#assign').text()
      if $('#deadline').val()
        data.deadline = $('#deadline').val()
      $.ajax
        url: 'newTask/'
        type: 'post'
        dataType: 'json'
        data: data
        success: (data) ->
          if data.msg == 'okay'
            location.href = ''

  $('#taskCancel').on 'click', ->
    $('#newTask').fadeOut()

  $('ul.task').hover(
    -> $(@).children().last().fadeIn 'fast'
    -> $(@).children().last().fadeOut 'fast'
  )

  $('li.doneTask').hover(
    -> $(@).find('i.fa-check').fadeIn 'fast'
    -> $(@).find('i.fa-check').fadeOut 'fast'
  ).on 'click', ->
    $.ajax
      url: 'doTask/'
      type: 'post'
      dataType: 'json'
      data:
        pk: $(@).data 'pk'
      success: (data) =>
        if data.msg == 'okay'
          $(@).parent().fadeOut()
          $('#doneList').prepend "
            <ul class='list-inline' style='margin-left: 15px;'>
              <li class='text-success'><i class='fa fa-lg fa-check-square-o'></i></li>
              <li>#{$(@).next().text()}</li>
            </ul>
            <p class='text-muted' style='margin: 15px 50px;'>
              checked by <span class='text-warning'>you</span> just now
            </p>
            "

  $('#comTask').on 'click', ->
    $(@).find('i')
      .toggleClass 'fa-angle-double-down'
      .toggleClass 'fa-angle-double-up'
    $('#doneList').fadeToggle()

  $('.doneItem').hover(
    -> $(@).find('span').last().fadeIn 'fast'
    -> $(@).find('span').last().fadeOut 'fast'
  )

  $('a[href^="#clear-"]').on 'click', ->
    pk = $(@).attr('href').substr 7
    $.ajax
      url: 'clearTask/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) =>
        if data.msg == 'okay'
          $(@).parents('.doneItem').fadeOut().remove()

  stickFooter()


