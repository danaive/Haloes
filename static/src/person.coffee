$ ->
  # sign out
  $('[href="#logout"]').on 'click', ->
    $.ajax
      url: 'sign-out/'
      type: 'post'
      dataType: 'json'
      success: ->
        location.href = '/'

  #update
  $('#updateBtn').on 'click', ->
    $(this).hide()
    $('#cancelBtn').show()
    $('.alert').hide()
    $('#updateForm').fadeToggle()
  $('#cancelBtn').on 'click', ->
    $(this).hide()
    $('#updateBtn').show()
    $('#updateForm').fadeToggle()
  $('#confBtn').on 'click', ->
    $.ajax
      url: 'update-info/'
      type: 'post'
      dataType: 'json'
      data:
        major: $('#updateMajor').val()
        school: $('#updateSchool').val()
        email: $('#updateEmail').val()
        blog: $('#updateBlog').val()
      success: (data) ->
        if data.msg == 'okay'
          $('.alert-success').fadeIn()
          window.setTimeout("$('#updateForm').fadeOut()", 1000)
          $('#cancelBtn').hide()
          $('#updateBtn').show()
          $('#infoMajor').text(data.major)
          $('#infoSchool').text(data.school)
          $('#infoEmail').text(data.email)
          $('#infoBlog').text(data.blog)

  # follow
  if $('#followBtn').data('follow') == true
    $(this).hide()
  else
    $('#unfollowBtn').hide()
  $('#followBtn').on 'click', ->
    $.ajax
      url: 'follow/'
      type: 'post'
      dataType: 'json'
      data:
        username: $('#nickname').text()
      success: (data) ->
        if data.msg == 'okay'
          $('#followAlert').fadeIn()
          window.setTimeout("$('#followAlert').fadeOut()", 2000)

  # charts
  score = []
  $.ajax
    url: 'getscore/'
    dataType: 'json'
    success: (data) ->
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
      new Chart(rctx).Radar rdata, {}

