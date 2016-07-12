$ ->

  $('a[href$="writeup/"]').addClass 'current'

  Simditor.locale = 'en-US'
  editor = new Simditor
    textarea: $('#editor')
    toolbar: [
                'title'
                'bold'
                'italic'
                'strikethrough'
                '|'
                'ol'
                'ul'
                'blockquote'
                'code'
                'table'
                '|'
                'link'
                'hr'
                '|'
                'markdown'
            ]
    toolbarFloatOffset: $('nav').height()
    imageButton: [
                    'upload'
                    'external'
                 ]
    upload:
      url: ''
      params: null
      fileKey: 'upload_file'
      connectionCount: 3
      leaveConfirm: 'Uploading is in progress, are you sure to leave this page?'

  $('#getv').on 'click', ->
    console.log editor.getValue()

  $('#sync').on 'click', ->
    console.log editor.sync()

  stickFooter()
