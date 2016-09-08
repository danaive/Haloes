$ ->
  csrftoken = $.cookie('csrftoken')
  csrfSafeMethod = (method) ->
    /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  $.ajaxSetup
    beforeSend: (xhr, settings) ->
      unless csrfSafeMethod(settings.type) or @.crossDomain
        xhr.setRequestHeader 'X-CSRFToken', csrftoken

  $('#username').focus()

  $('.alert').on 'click', ->
    $(@).fadeOut()

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
            window.setTimeout 'location.href="person/"', 500
          else if data.msg == 'fail'
            $('#signInFail').fadeIn()
          else if data.msg == 'email'
            $('#emailFail').fadeIn()
          else
            $('#alertError').fadeIn()

  signup = ->
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
          else if data.msg == 'fail'
            $('#signUpFail').fadeIn()
          else
            $('#alertError').fadeIn()

  $('#guest').on 'click', ->
    $('#signInDone').fadeIn()
    window.setTimeout 'location.href="challenge/"', 500

  handler = (captchaObj) ->
    $('#signUp').on 'click', ->
      validate = captchaObj.getValidate()
      if !validate
        alert 'plz validate first'
        return
      $.ajax
        url: 'person/validate_captcha/'
        type: 'post'
        dataType: 'json'
        data:
          challenge: validate.geetest_challenge
          validate: validate.geetest_validate
          seccode: validate.geetest_seccode
        success: (data) ->
          false

    captchaObj.bindOn('#signUp')
    captchaObj.appendTo('#captcha')
    captchaObj.onSuccess(signup)

  $.ajax
    url: 'person/get_captcha/'
    type: 'get'
    dataType: 'json'
    success: (data) ->
      initGeetest
        gt: data.gt
        challenge: data.challenge
        product: 'popup'
        offline: !data.success
        lang: 'en'
        handler
