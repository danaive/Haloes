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
      $(this).parent().parent().addClass 'pull-right'
    onSwitchChange: (event, state) ->
      if state
        $('#teamList').hide()
        $('#userList').fadeIn()
      else
        $('#userList').hide()
        $('#teamList').fadeIn()
      stickFooter()

  $('a[href^="#user"]').on 'click', ->
    pk = ($(this).attr 'href').substr 5

  $('a[href^="#team"]').on 'click', ->