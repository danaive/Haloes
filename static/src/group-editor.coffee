$ ->

  $('a[href$="group/"]').addClass 'current'

  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: ['title', 'bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr', '|', 'markdown']
    toolbarFloatOffset: $('nav').height()

  $('.alert').on 'click', ->
    $(@).fadeOut()

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
          li = '''<li class="list-group-item"> \
                    <a class="btn btn-xs btn-link pull-right" data-toggle="tooltip" data-placement="right" title="click to insert" data-path data-name> \
                      <i class="fa fa-share-square-o"></i> \
                    </a> \
                    <p></p> \
                  </li>'''
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
    if $('#title').val() and editor.getValue()
      $(@).attr 'disabled', 'disabled'
      $('i.fa-spiner').show()
      $.ajax
        url: '/group/submit/'
        type: 'post'
        dataType: 'json'
        data:
          title: $('#title').val()
          content: editor.getValue()
        success: (data) =>
          $('i.fa-spiner').hide()
          $(@).removeAttr 'disabled'
          if data.msg == 'okay'
            $('#submitSuccess').fadeIn()
            window.setTimeout "location.href='#{data.pk}/'", 1000
          else
            $('#submitFail').fadeIn()
            window.setTimeout "$('#submitFail').fadeOut()", 1000

  stickFooter()
