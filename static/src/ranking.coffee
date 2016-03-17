$ ->
  $('a[href$="ranking/"]').addClass 'current'

  stickFooter()

  $('input[type="checkbox"]').bootstrapSwitch
    size: 'mini'
    offColor: 'info'
    handleWidth: 80
    onText: 'User'
    offText: 'Team'
    onSwitchChange: (event, state) ->
      if state
        $('#teamList').hide()
        $('#userList').fadeIn()
      else
        $('#userList').hide()
        $('#teamList').fadeIn()