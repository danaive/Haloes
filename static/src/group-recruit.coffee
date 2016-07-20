$ ->

  $('a[href$="group/"]').addClass 'current'

  stickFooter()

  $('#joinBtn').on 'click', ->
    if $('#invCode').val()
      $.ajax
        url: 'join/'
        type: 'post'
        dataType: 'json'
        data:
          code: $('#invCode').val()
        success: (data) ->
          if data.name != '%%'
            $('#groupName').text data.name
            $('#joinSuccess').fadeIn()
            window.setTimeout 'location.href="/gruop/"', 1000
          else
            $('#joinFail').fadeIn()

  $('#createBtn').on 'click', ->
    if $('#grpName').val()
      $.ajax
        url: 'create/'
        type: 'post'
        dataType: 'json'
        data:
          name: $('#grpName').val()
        success: (data) ->
          if data.msg == 'okay'
            $('#createSuccess').fadeIn()
            window.setTimeout 'location.href="/group/"', 1000
          else
            $('#createFail').fadeIn()

  $('btn[id^="apply-"]').on 'click', ->
    pk = ($(@).attr 'id').substr 6
    $.ajax
      url: 'apply/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) =>
        if data.msg == 'okay'
          $('#applySuccess').fadeIn()
          $('btn[id^="apply-"]').hide()
          $(@).next().show()
          window.setTimeout "$('#applySuccess').fadeOut()", 1000
        else
          $('#applyFail').fadeIn()
          window.setTimeout "$('#applyFail').fadeOut()", 1000

  $('btn.withdraw').on 'click', ->
    $.ajax
      url: 'withdraw/'
      type: 'post'
      dataType: 'json'
      success: (data) ->
        $('#withdrawSuccess').fadeIn()
        $('btn.withdraw').hide()
        $('btn[id^="apply-"]').show()
        window.setTimeout "$('#withdrawSuccess').fadeOut()", 1000
