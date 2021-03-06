// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var editor, toolbar;
    $('a[href$="group/"]').addClass('current');
    $('[data-toggle="tooltip"]').tooltip();
    toolbar = ['bold', 'italic', 'strikethrough', '|', 'ol', 'ul', 'blockquote', 'code', 'table', '|', 'link', 'hr'];
    Simditor.locale = 'en-US';
    editor = new Simditor({
      textarea: $('#editor'),
      toolbar: toolbar,
      toolbarFloat: false
    });
    $('#writeupHolder').html($('#writeupHolder').text());
    $('p.marked').each(function() {
      return $(this).html($(this).text());
    });
    $('#submitBtn').on('click', function() {
      if (editor.getValue()) {
        return $.ajax({
          url: '/group/comment/',
          type: 'post',
          dataType: 'json',
          data: {
            content: editor.getValue(),
            issue: $(this).data('pk'),
            reply: 0
          },
          success: function(data) {
            if (data.msg === 'okay') {
              return location.href = '';
            }
          }
        });
      }
    });
    $('button.reply').on('click', function() {
      try {
        editor2.destroy();
      } catch (undefined) {}
      $('button.submit').hide();
      $('button.cancel').hide();
      $('button.reply').show();
      $(this).hide().siblings('button').show();
      $(this).parent().append('<textarea style="display: none;"></textarea>');
      return window.editor2 = new Simditor({
        textarea: $(this).siblings('textarea'),
        toolbar: toolbar,
        toolbarFloat: false
      });
    });
    $('button.cancel').on('click', function() {
      editor2.destroy();
      $(this).hide().siblings('button').hide();
      return $(this).siblings('button.reply').show();
    });
    $('button.submit').on('click', function() {
      var pk;
      pk = $(this).data('focus');
      if (editor2.getValue()) {
        return $.ajax({
          url: '/group/comment/',
          type: 'post',
          dataType: 'json',
          data: {
            content: editor2.getValue(),
            issue: $('#submitBtn').data('pk'),
            reply: pk
          },
          success: function(data) {
            if (data.msg === 'okay') {
              return location.href = '';
            }
          }
        });
      }
    });
    return stickFooter();
  });

}).call(this);
