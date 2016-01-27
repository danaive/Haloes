$ ->
  docHeight = $(window).height()
  footerTop = $('.footer').position().top + $('.footer').height() + 30
  if footerTop < docHeight
    $('.footer').css 'margin-top': (docHeight - footerTop) + 'px'
