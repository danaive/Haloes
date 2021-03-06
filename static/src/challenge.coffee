$ ->

  $('a[href$="challenge/"]').addClass 'current'
  $('[data-toggle="tooltip"]').tooltip()

  # $.fn.bootstrapSwitch.defaults.size = 'mini'
  # $.fn.bootstrapSwitch.defaults.onColor = 'info'

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

  PAGE_ITEM_COUNT = 10

  total = 0
  $('tr.ALL').each ->
    if $(@).data('state') == 0
      $(@).addClass 'Attempted'
    total += 1
    if total <= PAGE_ITEM_COUNT
      $(@).show()

  stickFooter()

  $('[id^="btn"]').on 'click', ->
    $('tr.ALL').hide()
    $('#cont').data 'page', 0
    cate = ($(@).attr 'id').substr 3
    $('#cont').data 'cate', cate
    cnt = 0
    $("tr.ALL.#{cate}").each ->
      cnt += 1
      if cnt <= PAGE_ITEM_COUNT
        $(@).show()
    stickFooter()

  $('[id^="pager"]').on 'click', ->
    total = $('tr.ALL').length
    page = $('#cont').data 'page'
    cate = $('#cont').data 'cate'
    if 'Next' == ($(@).attr 'id').substr 5
      if page + PAGE_ITEM_COUNT >= total
        return
      page += PAGE_ITEM_COUNT
    else
      if page < PAGE_ITEM_COUNT
        return
      page -= PAGE_ITEM_COUNT
    $('tr.ALL').hide()
    $('#cont').data 'page', page
    cnt = 0
    $("tr.ALL.#{cate}").each ->
      cnt += 1
      if page < cnt <= page + PAGE_ITEM_COUNT
        $(@).show()
    stickFooter()

  $('i.fa-lightbulb-o').on 'click', ->
    pk = $(@).data 'pk'
    $.ajax
      url: 'drop-attempt/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) =>
        if data.msg == 'okay'
          $(@).hide()

  $('#modal-container').on 'show.bs.modal', (event) ->
    pk = $(event.relatedTarget).data 'pk'
    $('#modalTitle').text $(event.relatedTarget).text()
    $('#submit').data 'pk', pk
    $('#flagHolder').show()
    $('.alert').hide()
    $('#flagHolder').text ''
    $.ajax
      url: 'detail/'
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
      url: 'submit/'
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
