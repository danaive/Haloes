$ ->
  csrftoken = $.cookie('csrftoken')
  csrfSafeMethod = (method) ->
    /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  $.ajaxSetup
    beforeSend: (xhr, settings) ->
      unless csrfSafeMethod(settings.type) or this.crossDomain
        xhr.setRequestHeader 'X-CSRFToken', csrftoken

  $('#username').focus()

  $('.alert').on 'click', ->
    $(this).fadeOut()

  $('#signIn').on 'click', ->
    if $('#username').val() and $('#password').val()
      salt = $('#signIn').data 'salt'
      $.ajax
        url: 'person/sign-in/'
        type: 'post'
        dataType: 'json'
        data:
          username: $('#username').val()
          password: $.sha256($.sha256($('#password').val()) + salt)
          salt: salt
        success: (data) ->
          if data.msg == 'okay'
            $('#signInDone').fadeIn()
            window.setTimeout 'location.href="/person"', 500
          else if data.msg == 'fail'
            $('#signInFail').fadeIn()
          else
            $('#alertError').fadeIn()

  $('#signUp').on 'click', ->
    if $('#remail').val() and $('#rusername').val() and $('#rpassword').val()
      $.ajax
        url: 'person/sign-up/'
        type: 'post'
        dataType: 'json'
        data:
          username: $('#rusername').val()
          password: $.sha256($('#rpassword').val())
          email: $('#remail').val()
        success: (data) ->
          if data.msg == 'okay'
            $('#signUpDone').fadeIn()
            window.setTimeout 'location.href="/person"', 500
          else if data.msg == 'fail'
            $('#signUpFail').fadeIn()
          else
            $('#alertError').fadeIn()