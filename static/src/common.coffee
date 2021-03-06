$ ->
  window.stickFooter = ->
    docHeight = $(window).height()
    footerTop = $('.footer').position().top + $('.footer').height() + 20
    if footerTop < docHeight
      $('.footer').css 'margin-top': (docHeight - footerTop) + 'px'
    else
      $('.footer').css 'margin-top': '0px'

  csrftoken = $.cookie('csrftoken')
  csrfSafeMethod = (method) ->
    /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  $.ajaxSetup
    beforeSend: (xhr, settings) ->
      unless csrfSafeMethod(settings.type) or @.crossDomain
        xhr.setRequestHeader 'X-CSRFToken', csrftoken

  $('a[href="#signIn"]').on 'click', ->
    location.href = '/'

  $('a[href="#signUp"]').on 'click', ->
    location.href = '/'

  $('a[href="#signOut"]').on 'click', ->
    $.post '/sign-out/'
    location.href = '/'

  $('ul.navbar-nav li').hover(
    -> $(@).children('a').addClass 'hovering'
    -> $(@).children('a').removeClass 'hovering'
  )
