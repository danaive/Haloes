$ ->

  $('a[href$="challenge/"]').addClass 'current'
  $('[data-toggle="tooltip"]').tooltip()

  $.fn.bootstrapSwitch.defaults.size = 'mini'
  $.fn.bootstrapSwitch.defaults.onColor = 'info'

  $('input[type="checkbox"]').bootstrapSwitch
    onSwithChange: ->
        $(this).bootstrapSwitch('toggleIndeterminate')
        $(this).bootstrapSwitch('toggleDisable')


