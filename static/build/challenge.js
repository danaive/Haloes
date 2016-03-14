// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var PAGE_ITEM_COUNT, total;
    $('a[href$="challenge/"]').addClass('current');
    $('[data-toggle="tooltip"]').tooltip();
    $('input[type="checkbox"]').bootstrapSwitch({
      size: 'mini',
      onColor: 'info',
      onSwitchChange: function(event, state) {
        var $this;
        console.log(state);
        $(this).bootstrapSwitch('toggleIndeterminate');
        $this = $(this);
        return $.ajax({
          url: 'switch/',
          type: 'post',
          dataType: 'json',
          success: function(data) {
            return $this.bootstrapSwitch('state', state, true);
          }
        });
      }
    });
    PAGE_ITEM_COUNT = 15;
    total = 0;
    $('tr.ALL').each(function() {
      if (($(this).data('state')) === '0') {
        $(this).addClass('Attempted');
      }
      total += 1;
      if (total <= PAGE_ITEM_COUNT) {
        return $(this).show();
      }
    });
    stickFooter();
    $('[id^="btn"]').on('click', function() {
      var cate, cnt;
      $('tr.ALL').hide();
      $('#cont').data('page', 0);
      cate = $(this).attr('id').substr(3);
      $('#cont').data('cate', $(this).attr('cate', cate));
      cnt = 0;
      $("tr.ALL." + cate).each(function() {
        cnt += 1;
        if (cnt <= PAGE_ITEM_COUNT) {
          return $(this).show();
        }
      });
      return stickFooter();
    });
    $('[id^="pager"]').on('click', function() {
      var cate, cnt, page;
      total = $('tr.ALL').length;
      page = $('#cont').data('page');
      cate = $('#cont').data('cate');
      if ('Next' === $(this).attr('id').substr(5)) {
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
      $('tr.ALL').hide();
      $('#cont').data('page', page);
      cnt = 0;
      $("tr.ALL." + cate).each(function() {
        cnt += 1;
        if ((page < cnt && cnt <= page + PAGE_ITEM_COUNT)) {
          return $(this).show();
        }
      });
      return stickFooter();
    });
    return $('i[titil^="Attempted"]').on('click', function() {
      var $this, pk;
      pk = $(this).data('pk');
      $this = $(this);
      return $.ajax({
        url: 'drop-attempt/',
        type: 'post',
        dataType: 'json',
        data: {
          pk: pk
        },
        success: function(data) {
          return $this.hide();
        }
      });
    });
  });

}).call(this);
