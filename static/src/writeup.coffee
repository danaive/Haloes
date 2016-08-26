$ ->

  $('a[href$="writeup/"]').addClass 'current'

  PAGE_ITEM_COUNT = 10

  total = 0
  $('tr.wp').each ->
    total += 1
    if total <= PAGE_ITEM_COUNT
      $(@).show()

  stickFooter()

  $('[id^="pager"]').on 'click', ->
    total = $('tr.wp').length
    page = $('#cont').data 'page'
    if 'Next' == ($(@).attr 'id').substr 5
      if page + PAGE_ITEM_COUNT >= total
        return
      page += PAGE_ITEM_COUNT
    else
      if page < PAGE_ITEM_COUNT
        return
      page -= PAGE_ITEM_COUNT
    $('tr.wp').hide()
    $('#cont').data 'page', page
    cnt = 0
    $("tr.wp").each ->
      cnt += 1
      if page < cnt <= page + PAGE_ITEM_COUNT
        $(@).show()
    stickFooter()
