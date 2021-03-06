$ ->

  $('a[href$="writeup/"]').addClass 'current'

  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: ['title', 'bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr', '|', 'markdown']
    toolbarFloatOffset: $('nav').height()

  $('.alert').on 'click', ->
    $(@).fadeOut()

  if $('#submitBtn').data 'state'
    editor.setValue $('#contentHolder').text()
    $('#title').val $('#titleHolder').text()

  $('#uploadBtn').on 'click', ->
    if $('#imageName').val().length == 0
      return
    $.ajaxFileUpload
      url: '/writeup/upload-image/'
      secureurl: false
      fileElementId: 'imageFile'
      dataType: 'json'
      success: (data) ->
        if data.msg == 'okay'
          $('#uploadSuccess').fadeIn()
          li = '<li class="list-group-item"><a class="btn btn-xs btn-link pull-right" data-toggle="tooltip" data-placement="right" title="click to insert" data-path data-name><i class="fa fa-share-square-o"></i></a><p></p></li>'
          $('ul.list-group').append li
          $li = $('ul.list-group li').last()
          $li.find('p').text $('#imageName').val()
          $li.find('a').attr 'data-path', data.path
          $li.find('a').attr 'data-name', $('#imageName').val()
          $('[data-toggle="tooltip"]').tooltip()
          $('a.btn.btn-xs.btn-link').on 'click', ->
            content = '![' + ($(@).data 'name') + '](' + ($(@).data 'path') + ')'
            insertAtCursor $('textarea')[0], content
          window.setTimeout "$('#uploadSuccess').fadeOut()", 1000

  $('#submitBtn').on 'click', ->
    if $(@).data 'state'
      challenge = $('#challengeHolder').text()
    else
      challenge = $('#CList').val()
    if $('#title').val() and challenge
      $(@).attr 'disabled', 'disabled'
      $('i.fa-spiner').show()
      $.ajax
        url: '/writeup/submit/'
        type: 'post'
        dataType: 'json'
        data:
          title: $('#title').val()
          challenge: challenge
          content: editor.getValue()
        success: (data) =>
          $('i.fa-spiner').hide()
          $(@).removeAttr 'disabled'
          if data.msg == 'okay'
            $('#submitSuccess').fadeIn()
            window.setTimeout "location.href='/writeup/#{data.pk}/'", 1000
          else
            $('#submitFail').fadeIn()
            window.setTimeout "$('#submitFail').fadeOut()", 1000

  $('#SList').on 'change', ->
    $('#CList').empty()
    val = $(@).val()
    $.ajax
      url: '/writeup/get-challenges/'
      type: 'post'
      dataType: 'json'
      data:
        title: val
      success: (data) ->
        if data.msg == 'okay'
          for item in data.challenges
            $('#CList').append "<option value=#{item.pk}>#{item.name}</option>"

  stickFooter()
