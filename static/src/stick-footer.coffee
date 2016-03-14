$ ->
  window.stickFooter = ->
    docHeight = $(window).height()
    footerTop = $('.footer').position().top + $('.footer').height() + 30
    if footerTop < docHeight
      $('.footer').css 'margin-top': (docHeight - footerTop) + 'px'

  stickFooter()

  csrftoken = $.cookie('csrftoken')
  csrfSafeMethod = (method) ->
    /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  $.ajaxSetup
    beforeSend: (xhr, settings) ->
      unless csrfSafeMethod(settings.type) or this.crossDomain
        xhr.setRequestHeader('X-CSRFToken', csrftoken)