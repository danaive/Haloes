// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var PAGE_ITEM_COUNT, total;
    $('a[href$="writeup/"]').addClass('current');
    PAGE_ITEM_COUNT = 10;
    total = 0;
    $('tr.wp').each(function() {
      total += 1;
      if (total <= PAGE_ITEM_COUNT) {
        return $(this).show();
      }
    });
    stickFooter();
    return $('[id^="pager"]').on('click', function() {
      var cnt, page;
      total = $('tr.wp').length;
      page = $('#cont').data('page');
      if ('Next' === ($(this).attr('id')).substr(5)) {
        if (page + PAGE_ITEM_COUNT >= total) {
          return;
        }
        page += PAGE_ITEM_COUNT;
      } else {
        if (page < PAGE_ITEM_COUNT) {
          return;
        }
        page -= PAGE_ITEM_COUNT;
      }
      $('tr.wp').hide();
      $('#cont').data('page', page);
      cnt = 0;
      $("tr.wp").each(function() {
        cnt += 1;
        if ((page < cnt && cnt <= page + PAGE_ITEM_COUNT)) {
          return $(this).show();
        }
      });
      return stickFooter();
    });
  });

}).call(this);
