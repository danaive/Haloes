$ ->

  $('a[href$="group/"]').addClass 'current'

  stickFooter()

  apply = $('#teamCont').data 'pk'
  if apply != -1
    $('button.btn-default').hide()
    $("button[id='apply-#{apply}']").siblings('p.text-danger').show()

  $('.alert').on 'click', ->
    $(@).fadeOut()

  $('#joinBtn').on 'click', ->
    if $('#invCode').val()
      $.ajax
        url: 'join/'
        type: 'post'
        dataType: 'json'
        data:
          code: $('#invCode').val()
        success: (data) ->
          if data.msg == 'okay'
            $('#groupName').text data.name
            $('#joinSuccess').fadeIn()
            window.setTimeout 'location.href="/group/"', 1000
          else
            window.setTimeout "$('#joinFail').fadeIn()", 1000

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
            window.setTimeout "$('#createFail').fadeIn()", 1000

  $('button[id^="apply-"]').on 'click', ->
    pk = ($(@).attr 'id').substr 6
    $.ajax
      url: 'apply/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) =>
        if data.msg == 'okay'
          $('button.btn-default').hide()
          $('#applySuccess').fadeIn()
          $(@).siblings('p.text-danger').fadeIn()
          window.setTimeout "$('#applySuccess').fadeOut()", 1000
        else
          $('#applyFail').fadeIn()
          window.setTimeout "$('#applyFail').fadeOut()", 1000

  $('#withdrawBtn').on 'click', ->
    $.ajax
      url: 'withdraw/'
      type: 'post'
      dataType: 'json'
      success: (data) ->
        $('p.text-danger').hide()
        $('button.btn-default').fadeIn()
        $('#withdrawSuccess').fadeIn()
        window.setTimeout "$('#withdrawSuccess').fadeOut()", 1000
