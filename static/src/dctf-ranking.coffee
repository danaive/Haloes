$ ->
  $('a[href$="contest/"]').addClass 'current'

  stickFooter()

  $('input[type="checkbox"]').bootstrapSwitch
    size: 'mini'
    onColor: 'info'
    offColor: 'warning'
    handleWidth: 50
    labelWidth: 30
    onText: 'Team'
    offText: 'User'
    onInit: (event, state) ->
      $(this).parent().parent().addClass 'pull-right'
    onSwitchChange: (event, state) ->
      if state
        $('#userList').hide()
        $('#teamList').fadeIn()
      else
        $('#teamList').hide()
        $('#userList').fadeIn()
      stickFooter()

  $('a[href^="#user-"]').on 'click', ->
    pk = ($(this).attr 'href').substr 6
    location.href = '/person/' + pk

  $('a[href^="#team-"]').on 'click', ->
    pk = ($(this).attr 'href').substr 6
    location.href = '/team/' + pk