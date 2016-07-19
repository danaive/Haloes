$ ->

  $('a[href$="writeup/"]').addClass 'current'

  $('#writeupHolder').html $('#writeupHolder').text()
  toolbar = ['title', 'bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr', '|', 'markdown']
  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: toolbar
    toolbarFloat: false

  $('p.marked').each ->
    $(this).html $(this).text()

  $('#submitBtn').on 'click', ->
    if editor.getValue()
      $.ajax
        url: '/writeup/comment/'
        type: 'post'
        dataType: 'json'
        data:
          content: editor.getValue()
          writeup: 2
          reply: 0
        success: (data) ->
          if data.msg == 'okay'
            location.href = ''

  $('button.reply').on 'click', ->
    try editor2.destroy()
    $this = $(this).hide().siblings('button').show()
    $this.parent().append '<textarea style="display: none;"></textarea>'
    window.editor2 = new Simditor
      textarea: $this.siblings('textarea')
      toolbar: toolbar

  $('button.cancel').on 'click', ->
    editor2.destroy()
    $(this).hide().siblings('button').hide()
    $(this).siblings('button.reply').show()

  $('button.submit').on 'click', ->
    pk = $(this).data 'focus'
    if editor2.getValue()
      $.ajax
        url: '/writeup/comment/'
        type: 'post'
        dataType: 'json'
        data:
          content: editor2.getValue()
          writeup: 2
          reply: pk
        success: (data) ->
          if data.msg == 'okay'
            location.href = ''

  stickFooter()