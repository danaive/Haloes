$ ->

  $('a[href$="writeup/"]').addClass 'current'

  $('#writeupHolder').html $('#writeupHolder').text()

  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: ['title', 'bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr', '|', 'markdown']
    toolbarFloatOffset: $('nav').height()

  stickFooter()