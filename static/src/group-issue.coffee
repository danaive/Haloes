$ ->

  $('a[href$="group/"]').addClass 'current'
  $('[data-toggle="tooltip"]').tooltip()

  toolbar = ['bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr']
  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: toolbar
    toolbarFloat: false

  $('#writeupHolder').html $('#writeupHolder').text()
  $('p.marked').each ->
    $(@).html $(@).text()

  $('#submitBtn').on 'click', ->
    if editor.getValue()
      $.ajax
        url: '/group/comment/'
        type: 'post'
        dataType: 'json'
        data:
          content: editor.getValue()
          issue: $(@).data 'pk'
          reply: 0
        success: (data) ->
          if data.msg == 'okay'
            location.href = ''

  $('button.reply').on 'click', ->
    try editor2.destroy()
    $('button.submit').hide()
    $('button.cancel').hide()
    $('button.reply').show()
    $(@).hide().siblings('button').show()
    $(@).parent().append '<textarea style="display: none;"></textarea>'
    window.editor2 = new Simditor
      textarea: $(@).siblings('textarea')
      toolbar: toolbar
      toolbarFloat: false

  $('button.cancel').on 'click', ->
    editor2.destroy()
    $(@).hide().siblings('button').hide()
    $(@).siblings('button.reply').show()

  $('button.submit').on 'click', ->
    pk = $(@).data 'focus'
    if editor2.getValue()
      $.ajax
        url: '/group/comment/'
        type: 'post'
        dataType: 'json'
        data:
          content: editor2.getValue()
          issue: $('#submitBtn').data 'pk'
          reply: pk
        success: (data) ->
          if data.msg == 'okay'
            location.href = ''


  stickFooter()