$ ->

  $('a[href$="writeup/"]').addClass 'current'

  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: [
                'title'
                'bold'
                'italic'
                'strikethrough'
                '|'
                'ol'
                'ul'
                'blockquote'
                'code'
                'table'
                '|'
                'link'
                'hr'
                '|'
                'markdown'
            ]
    toolbarFloatOffset: $('nav').height()

  $('#uploadBtn').on 'click', ->
    if $('#imageName').val().length == 0
      return
    $.ajaxFileUpload
      url: '/writeup/uploadImage/'
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
            content = '![' + ($(this).data 'name') + '](' + ($(this).data 'path') + ')'
            insertAtCursor $('textarea')[0], content
          window.setTimeout "$('#uploadSuccess').fadeOut()", 1000

  $('#submitBtn').on 'click', ->
    if $('#CList').val() and $('#title').val()
      $this = $(this).attr 'disabled', 'disabled'
      $('i.fa-spiner').show()
      $.ajax
        url: '/writeup/submit/'
        type: 'post'
        dataType: 'json'
        data:
          title: $('#title').val()
          challenge: $('#CList').val()
          content: editor.getValue()
        success: (data) ->
          $('i.fa-spiner').hide()
          $this.removeAttr 'disabled'
          if data.msg == 'okay'
            $('#submitSuccess').fadeIn()
            window.setTimeout "location.href='/writeup/#{data.pk}/'", 1000
          else
            $('#submitFail').fadeIn()
            window.setTimeout "$('#submitFail').fadeOut()", 1000

  $('#SList').on 'change', ->
    $('#CList').empty()
    val = $(this).val()
    $.ajax
      url: '/writeup/getChallenges/'
      type: 'post'
      dataType: 'json'
      data:
        title: val
      success: (data) ->
        if data.msg == 'okay'
          for item in data.challenges
            $('#CList').append "<option value=#{item.pk}>#{item.name}</option>"


  stickFooter()
