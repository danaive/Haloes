$ ->

  $('a[href$="contest/"]').addClass 'current'
  stickFooter()

  $('a[href^="#mod-"]').on 'click', ->
    pk = ($(this).attr 'href').substr 5
    $('#modalTitle').text $(this).text()
    $('#submit').data 'pk', pk
    $('#flagHolder').show()
    $('.alert').hide()
    $.ajax
      url: '/challenge/get-challenge/'
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
    pk = $(this).data 'pk'
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