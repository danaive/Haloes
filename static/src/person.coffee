$ ->

  $('a[href$="person/"]').addClass 'current'

  # sign out
  $('[href="#logout"]').on 'click', ->
    $.ajax
      url: 'sign-out/'
      type: 'post'
      dataType: 'json'
      success: ->
        location.href = '/'

  $('.alert').on 'click', ->
    $(@).fadeOut()

  #update info
  $('#updateBtn').on 'click', ->
    $(@).find('i')
      .toggleClass 'fa-angle-double-down'
      .toggleClass 'fa-angle-double-up'
    $('.alert').hide()
    $('#updateForm').fadeToggle()
  $('#cancelBtn').on 'click', ->
    $('#updateForm').fadeOut()
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
        motto: $('#updateMotto').val()
      success: (data) ->
        if data.msg == 'okay'
          $('.alert-success').fadeIn()
          window.setTimeout "$('#updateForm').fadeOut()", 1000
          $('#infoMajor').text(data.major)
          $('#infoSchool').text(data.school)
          $('#infoEmail').text(data.email)
          $('#infoBlog').text(data.blog)
          $('#infoMotto').text(data.motto)

  # follow
  if $('#followBtn').data('follow')
    $('#unfollowBtn').show()
  else
    $('#followBtn').show()
  $('[id$="followBtn"]').on 'click', ->
    $(@).hide()
    $.ajax
      url: '/person/follow/'
      type: 'post'
      dataType: 'json'
      data:
        username: $('#nickname').text()
      success: (data) =>
        if data.msg == 'okay'
          if $(@).attr('id').length == 9
            $('#unfollowBtn').fadeIn()
          else
            $('#followBtn').fadeIn()


  # charts
  score = []
  $.ajax
    url: '/person/get-score/'
    type: 'post'
    dataType: 'json'
    data:
      username: $('#nickname').text()
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
      new Chart(pctx).Pie(
        pdata
        animateScale: true
      )

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
        # scaleStartValue: -5
      )

  # avatar
  $('[data-toggle="tooltip"]').tooltip()
  $('#avatar').on 'click', ->
    $('#avatarHolder').click()

  getNews = () ->
    step = 6
    page = $('#newsHolder').data 'page'
    $('#moreNews').hide()
    $('#moreNews').siblings('i').fadeIn()
    $.ajax
      url: 'get-news/'
      type: 'post'
      dataType: 'json'
      data:
        page: page
      success: (data) ->
        if data.msg == 'okay'
          putNews = (news) ->
            li = """<li class='media'> \
                      <a class='pull-left' href='#{news.link}'> \
                        <img class='media-object img-rounded' height='64' src='#{news.avatar}'> \
                      </a> \
                      <div class='media-body'> \
                        <h4 class='media-heading'>#{news.title}</h4> \
                        <p>#{news.time}</p> \
                        <p>#{news.content}</p> \
                      </div> \
                    </li>"""
            $('#newsHolder').append li
          putNews news for news in data.news
          $('#newsHolder').data 'page', ($('#newsHolder').data 'page') + step
        $('#moreNews').siblings('i').hide()
        $('#moreNews').show()


  $('#moreNews').on 'click', ->
    getNews()

  getNews()

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
