$ ->

  $('a[href$="contest/"]').addClass 'current'
  stickFooter()

  $('a[href^="#mod-"]').on 'click', ->
    pk = ($(@).attr 'href').substr 5
    $('#modalTitle').text $(@).text()
    $('#submit').data 'pk', pk
    $('#flagHolder').show()
    $('.alert').hide()
    $.ajax
      url: '/challenge/detail/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) ->
        if data.msg == 'okay'
          $('.modal-body').html data.content
          $('#toggleModal').click()
        else
          return false

  $('#submit').on 'click', ->
    pk = $(@).data 'pk'
    $.ajax
      url: '/contest/submit/'
      type: 'post'
      dataType: 'json'
      data:
        flag: $('#flagHolder').val()
        pk: pk
      success: (data) ->
        $('flagHolder').hide()
        if data.msg == 'okay'
          $('.alert-success').fadeIn()
        else if data.msg == 'fail'
          $('.alert-danger').fadeIn()