$ ->
  $('a[href$="group/"]').addClass 'current'
  $('[data-toggle="tooltip"]').tooltip()
  # charts
  score = []
  $.ajax
    url: '/group/get-score/'
    type: 'post'
    dataType: 'json'
    data:
      name: $('#nameHolder').data 'name'
    success: (data) ->
      # pie chart
      score = data.score
      label = ['PWN', 'REVERSE', 'WEB', 'CRYPTO', 'MISC']
      color = ['#3BAFDA', '#8CC152', '#ED5565', '#37BC9B', '#FFCE54']
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
        scaleSteps: 4
        scaleStepWidth: 25
        # scaleStartValue: -25
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
        url: 'new-task/'
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
      url: 'do-task/'
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
              <li class='checked-task'></li>
            </ul>
            <p class='text-muted' style='margin: 15px 50px;'>
              checked by <span class='text-warning'>you</span> just now
            </p>
            "
          $('li.checked-task').text $(@).next().text()

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
      url: 'clear-task/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) =>
        if data.msg == 'okay'
          $(@).parents('.doneItem').fadeOut().remove()
          $(@).parents('ul.task').fadeOut().remove()


  $('#avatar').on 'click', ->
    $('#avatarHolder').click()

  if($('h2').data('state') != 1)
    $('.leader').remove()

  $('h2').hover(
    -> $(@).find('a').fadeIn 'slow'
    -> $(@).find('a').fadeOut 'fast'
  )

  $('#dismissBtn').on 'click', ->
    if $('#nameHolder').val() == $('#nameHolder').data 'name'
      $.post 'dismiss/'
      location.href = '/group/'
    else
      console.log $('#nameHolder').val()
      console.log $('#nameHolder').data 'name'

  $('li.member').hover(
    -> $(@).find('a.kickout').fadeIn 'slow'
    -> $(@).find('a.kickout').fadeOut 'fast'
  )

  $('#kickout-modal').on 'show.bs.modal', (event) ->
    $(@).find('span').text $(event.relatedTarget).data 'name'
    $(@).find('button').attr 'data-pk', $(event.relatedTarget).data 'pk'

  $('#kickoutBtn').on 'click', ->
    $.ajax
      url: 'kickout/'
      type: 'post'
      dataType: 'json'
      data:
        pk: $(@).data 'pk'
      success: (data) =>
        if data.msg == 'okay'
          $('#kickout-modal').modal 'hide'
          $("a.kickout[data-pk='#{$(@).data 'pk'}']").parents('li.media').fadeOut 'slow'

  $('a.approve').on 'click', ->
    $.ajax
      url: 'approve/'
      type: 'post'
      dataType: 'json'
      data:
        pk: $(@).data 'pk'
      success: (data) =>
        if data.msg == 'okay'
          $(@).hide()
          $(@).siblings('i.text-success').fadeIn 'slow'

  stickFooter()

window.uploadAvatar = ->
  $('#avatar').hide()
  $('#iconHolder').show()
  $.ajaxFileUpload
    url: 'update-avatar/'
    secureurl: false
    fileElementId: 'avatarHolder'
    dataType: 'json'
    success: (data) ->
      if data.msg == 'okay'
        $('#avatar').attr 'src', data.path
      else
        alert 'Image No Larger Than 5M is Accepted.'
      $('#iconHolder').hide()
      window.setTimeout "$('#avatar').show()", 50
