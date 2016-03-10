$ ->
  $('[href="#logout"]').on 'click', ->
    $.ajax
      url: 'sign-out/'
      type: 'post'
      dataType: 'json'
      success: ->
        location.href = '/'

  $('#updateBtn').on 'click', ->
    $(this).hide()
    $('#cancelBtn').show()
    $('.alert').hide()
    $('#updateForm').fadeToggle()
  $('#cancelBtn').on 'click', ->
    $(this).hide()
    $('#updateBtn').show()
    $('#updateForm').fadeToggle()
  $('#confBtn').on 'click', ->
    $.ajax
      url: 'update-info/'
      type: 'post'
      dataType: 'json'
      data:
        major: $('#updateMajor').val()
        school: $('#updateSchool').val()
        email: $('#updateEmail').val()
        blog: $('#updateBlog').val()
      success: (data) ->
        if data.msg == 'okay'
          $('.alert-success').fadeIn()
          window.setTimeout("$('#updateForm').fadeOut()", 1000)
          $('#cancelBtn').hide()
          $('#updateBtn').show()
          $('#infoMajor').text(data.major)
          $('#infoSchool').text(data.school)
          $('#infoEmail').text(data.email)
          $('#infoBlog').text(data.blog)

