$ ->

  $('a[href$="challenge/"]').addClass 'current'
  $('[data-toggle="tooltip"]').tooltip()

  # $.fn.bootstrapSwitch.defaults.size = 'mini'
  # $.fn.bootstrapSwitch.defaults.onColor = 'info'

  $('input[type="checkbox"]').bootstrapSwitch
    size: 'mini'
    onColor: 'info'
    onSwitchChange: (event, state) ->
      $(this).bootstrapSwitch 'toggleIndeterminate'
      $this = $(this)
      $.ajax
        url: 'switch/'
        type: 'post'
        dataType: 'json'
        data: {
          state: state,
          pk: $this.data 'pk'
        }
        success: (data) ->
          if data.msg == 'okay'
            $this.bootstrapSwitch 'state', state, true
          else
            $this.bootstrapSwitch 'state', !state, true

  PAGE_ITEM_COUNT = 15

  total = 0
  $('tr.ALL').each ->
    if ($(this).data 'state') == 0
      $(this).addClass 'Attempted'
    total += 1
    if total <= PAGE_ITEM_COUNT
      $(this).show()

  stickFooter()

  $('[id^="btn"]').on 'click', ->
    $('tr.ALL').hide()
    $('#cont').attr 'data-page', 0
    cate = ($(this).attr 'id').substr 3
    $('#cont').attr 'data-cate', cate
    cnt = 0
    $("tr.ALL.#{cate}").each ->
      cnt += 1
      if cnt <= PAGE_ITEM_COUNT
        $(this).show()
    stickFooter()

  $('[id^="pager"]').on 'click', ->
    total = $('tr.ALL').length
    page = $('#cont').data 'page'
    cate = $('#cont').data 'cate'
    if 'Next' == ($(this).attr 'id').substr 5
      if page + PAGE_ITEM_COUNT >= total
        return
      page += PAGE_ITEM_COUNT
    else
      if page < PAGE_ITEM_COUNT
        return
      page -= PAGE_ITEM_COUNT
    $('tr.ALL').hide()
    $('#cont').attr 'data-page', page
    cnt = 0
    $("tr.ALL.#{cate}").each ->
      cnt += 1
      if page < cnt <= page + PAGE_ITEM_COUNT
        $(this).show()
    stickFooter()

  $('i.fa-lightbulb-o').on 'click', ->
    pk = $(this).data 'pk'
    $this = $(this)
    $.ajax
      url: 'drop-attempt/'
      type: 'post'
      dataType: 'json'
      data:
        pk: pk
      success: (data) ->
        if data.msg == 'okay'
          $this.hide()

  $('a[href^="#mod-"]').on 'click', ->
    pk = ($(this).attr 'href').substr 5
    $('#modalTitle').text $(this).text()
    $('#submit').data 'pk', pk
    $('#flagHolder').show()
    $('.alert').hide()
    $.ajax
      url: 'get-challenge/'
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
      url: 'submit/'
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

  $('#uploadBtn').on 'click', ->
    $.ajaxFileUpload
      url: '/challenge/upload/'
      secureurl: false
      fileElementId: 'zipHolder'
      dataType: 'json'
      success: (data) ->
        console.log data.msg

