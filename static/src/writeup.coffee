$ ->

  $('a[href$="writeup/"]').addClass 'current'

  stickFooter()




ditor = new Simditor
  textarea: null
  placeholder: ''
  defaultImage: 'images/image.png'
  params: {}
  upload: false
  tabIndent: true
  toolbar: true
  toolbarFloat: true
  toolbarFloatOffset: 0
  toolbarHidden: false
  pasteImage: false
  cleanPaste: false