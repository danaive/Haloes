$ ->
  $('a[href$="ranking/"]').addClass 'current'

  stickFooter()

  $('input[type="checkbox"]').bootstrapSwitch
    size: 'mini'
    onColor: 'info'
    offColor: 'warning'
    handleWidth: 50
    labelWidth: 30
    onText: 'User'
    offText: 'Team'
    onInit: (event, state) ->
      $(@).parent().parent().addClass 'pull-right'
    onSwitchChange: (event, state) ->
      if state
        $('#teamList').hide()
        $('#userList').fadeIn()
        $('#userCont').data 'focus', 'user'
      else
        $('#userList').hide()
        $('#teamList').fadeIn()
        $('#userCont').data 'focus', 'team'
      stickFooter()

  PAGE_ITEM_COUNT = 10

  inituser = () ->
    total = 0
    $('tr.user').each ->
      total += 1
      if total <= PAGE_ITEM_COUNT
        $(@).show()
    stickFooter()
  initteam = () ->
    total = 0
    $('tr.team').each ->
      if total <= PAGE_ITEM_COUNT
        $(@).show()

  inituser()
  initteam()

  $('[id^="pager"]').on 'click', ->
    focus = $('#userCont').data 'focus'
    total = $("tr.#{focus}").length
    page = $("##{focus}Cont").data 'page'
    if 'Next' == ($(@).attr 'id').substr 5
      if page + PAGE_ITEM_COUNT >= total
        return
      page += PAGE_ITEM_COUNT
    else
      if page < PAGE_ITEM_COUNT
        return
      page -= PAGE_ITEM_COUNT
    $("tr.#{focus}").hide()
    $("##{focus}Cont").data 'page', page
    cnt = 0
    $("tr.#{focus}").each ->
      cnt += 1
      if page < cnt <= page + PAGE_ITEM_COUNT
        $(@).show()
    stickFooter()
