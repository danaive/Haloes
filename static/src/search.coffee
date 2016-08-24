$ ->

  $('[data-toggle="tooltip"]').tooltip()
  stickFooter()

  $('.alert').on 'click', ->
    $(@).fadeOut()

  $('input[type="checkbox"]').bootstrapSwitch
    size: 'mini'
    onColor: 'info'
    onSwitchChange: (event, state) ->
      $(@).bootstrapSwitch 'toggleIndeterminate'
      $.ajax
        url: 'switch/'
        type: 'post'
        dataType: 'json'
        data:
          state: state,
          pk: $(@).data 'pk'
        success: (data) =>
          if data.msg == 'okay'
            $(@).bootstrapSwitch 'state', state, true
          else
            $(@).bootstrapSwitch 'state', !state, true

  $('#modal-container').on 'show.bs.modal', (event) ->
    pk = $(event.relatedTarget).data 'pk'
    $('#modalTitle').text $(event.relatedTarget).text()
    $('#submit').data 'pk', pk
    $('#flagHolder').show()
    $('.alert').hide()
    $('#flagHolder').text ''
    $.ajax
      url: '/challenge/detail/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) ->
        if data.msg == 'okay'
          $('.modal-body').html data.content
        else
          false

  $('#submit').on 'click', ->
    pk = $(@).data 'pk'
    $.ajax
      url: '/challenge/submit/'
      type: 'post'
      dataType: 'json'
      data:
        flag: $('#flagHolder').val()
        pk: pk
      success: (data) ->
        $('flagHolder').hide()
        $('.alert').hide()
        if data.msg == 'okay'
          $('.alert-success').fadeIn()
        else if data.msg == 'fail'
          $('.alert-danger').fadeIn()


  apply = $('#teamCont').data 'pk'
  if apply != -1
    $('button.btn-default').hide()
    $("button[id='apply-#{apply}']").siblings('p.text-danger').show()

  $('button[id^="apply-"]').on 'click', ->
    pk = ($(@).attr 'id').substr 6
    $.ajax
      url: '/group/apply/'
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
      url: '/group/withdraw/'
      type: 'post'
      dataType: 'json'
      success: (data) ->
        $('p.text-danger').hide()
        $('button.btn-default').fadeIn()
        $('#withdrawSuccess').fadeIn()
        window.setTimeout "$('#withdrawSuccess').fadeOut()", 1000
