$ ->

  $('a[href$="writeup/"]').addClass 'current'

  $('#writeupHolder').html $('#writeupHolder').text()

  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: ['title', 'bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr', '|', 'markdown']
    toolbarFloatOffset: $('nav').height()

  $('p.marked').each ->
    $(this).html $(this).text()

  $('#submitBtn').on 'click', ->
    $.ajax
      url: '/writeup/comment/'
      type: 'post'
      dataType: 'json'
      data:
        content: editor.getValue()
        writeup: 2
        reply: 2
      success: (data) ->
        if data.msg == 'okay'
          alert 'okay'

  stickFooter()