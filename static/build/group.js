// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var score;
    $('a[href$="group/"]').addClass('current');
    $('[data-toggle="tooltip"]').tooltip();
    score = [];
    $.ajax({
      url: '/group/get-score/',
      type: 'post',
      dataType: 'json',
      data: {
        name: $('#nameHolder').data('name')
      },
      success: function(data) {
        var _, capacity, color, highlight, i, label, pctx, pdata, rctx, rdata, rgba;
        score = data.score;
        label = ['PWN', 'REVERSE', 'WEB', 'CRYPTO', 'MISC'];
        color = ['#3BAFDA', '#8CC152', '#ED5565', '#37BC9B', '#FFCE54'];
        highlight = ['#4FC3EE', '#A0D566', '#FF6979', '#4BD0AF', '#FFE268'];
        pdata = (function() {
          var j, len, results;
          results = [];
          for (i = j = 0, len = label.length; j < len; i = ++j) {
            _ = label[i];
            results.push({
              label: label[i],
              value: score[i],
              color: color[i],
              highlight: highlight[i]
            });
          }
          return results;
        })();
        pctx = $("#pieChart").get(0).getContext('2d');
        new Chart(pctx).Pie(pdata, {
          animateScale: true
        });
        capacity = data.capacity;
        rgba = ['rgba(137,114,158,1)', 'rgba(151,187,205,1)'];
        rdata = {
          labels: label,
          datasets: (function() {
            var j, len, results;
            results = [];
            for (i = j = 0, len = capacity.length; j < len; i = ++j) {
              _ = capacity[i];
              results.push({
                label: capacity[i].name,
                fillColor: rgba[i].slice(0, -2) + '0.2)',
                pointColor: rgba[i],
                pointStrokeColor: '#fff',
                pointHighlightFill: '#fff',
                pointHighlightStroke: rgba[i],
                data: capacity[i].score
              });
            }
            return results;
          })()
        };
        rctx = $('#radarChart').get(0).getContext('2d');
        return new Chart(rctx).Radar(rdata, {
          scaleOverride: true,
          scaleSteps: 4,
          scaleStepWidth: 25
        });
      }
    });
    $('#deadline').datetimepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
      minView: 2,
      maxView: 2
    });
    $('a.memberName').on('click', function() {
      return $('#assign').text($(this).text());
    });
    $('#newTaskBtn').on('click', function() {
      $('#taskContent').val('');
      $('#deadline').val('');
      $('#assign').text('Unassigned');
      $('#assign').attr('data-content', 0);
      return $('#newTask').fadeToggle();
    });
    $('#taskAssign').on('click', function() {
      var data;
      if ($('#taskContent').val()) {
        data = {
          content: $('#taskContent').val(),
          assign: $('#assign').text()
        };
        if ($('#deadline').val()) {
          data.deadline = $('#deadline').val();
        }
        return $.ajax({
          url: 'new-task/',
          type: 'post',
          dataType: 'json',
          data: data,
          success: function(data) {
            if (data.msg === 'okay') {
              return location.href = '';
            }
          }
        });
      }
    });
    $('#taskCancel').on('click', function() {
      return $('#newTask').fadeOut();
    });
    $('ul.task').hover(function() {
      return $(this).children().last().fadeIn('fast');
    }, function() {
      return $(this).children().last().fadeOut('fast');
    });
    $('li.doneTask').hover(function() {
      return $(this).find('i.fa-check').fadeIn('fast');
    }, function() {
      return $(this).find('i.fa-check').fadeOut('fast');
    }).on('click', function() {
      return $.ajax({
        url: 'do-task/',
        type: 'post',
        dataType: 'json',
        data: {
          pk: $(this).data('pk')
        },
        success: (function(_this) {
          return function(data) {
            if (data.msg === 'okay') {
              $(_this).parent().fadeOut();
              $('#doneList').prepend("<ul class='list-inline' style='margin-left: 15px;'> <li class='text-success'><i class='fa fa-lg fa-check-square-o'></i></li> <li class='checked-task'></li> </ul> <p class='text-muted' style='margin: 15px 50px;'> checked by <span class='text-warning'>you</span> just now </p>");
              return $('li.checked-task').text($(_this).next().text());
            }
          };
        })(this)
      });
    });
    $('#comTask').on('click', function() {
      $(this).find('i').toggleClass('fa-angle-double-down').toggleClass('fa-angle-double-up');
      return $('#doneList').fadeToggle();
    });
    $('.doneItem').hover(function() {
      return $(this).find('span').last().fadeIn('fast');
    }, function() {
      return $(this).find('span').last().fadeOut('fast');
    });
    $('a[href^="#clear-"]').on('click', function() {
      var pk;
      pk = $(this).attr('href').substr(7);
      return $.ajax({
        url: 'clear-task/',
        type: 'post',
        dataType: 'json',
        data: {
          pk: pk
        },
        success: (function(_this) {
          return function(data) {
            if (data.msg === 'okay') {
              $(_this).parents('.doneItem').fadeOut().remove();
              return $(_this).parents('ul.task').fadeOut().remove();
            }
          };
        })(this)
      });
    });
    $('#avatar').on('click', function() {
      return $('#avatarHolder').click();
    });
    if ($('h2').data('state') !== 1) {
      $('.leader').remove();
    }
    $('h2').hover(function() {
      return $(this).find('a').fadeIn('slow');
    }, function() {
      return $(this).find('a').fadeOut('fast');
    });
    $('#dismissBtn').on('click', function() {
      if ($('#nameHolder').val() === $('#nameHolder').data('name')) {
        $.post('dismiss/');
        return location.href = '/group/';
      } else {
        console.log($('#nameHolder').val());
        return console.log($('#nameHolder').data('name'));
      }
    });
    $('li.member').hover(function() {
      return $(this).find('a.kickout').fadeIn('slow');
    }, function() {
      return $(this).find('a.kickout').fadeOut('fast');
    });
    $('#kickout-modal').on('show.bs.modal', function(event) {
      $(this).find('span').text($(event.relatedTarget).data('name'));
      return $(this).find('button').attr('data-pk', $(event.relatedTarget).data('pk'));
    });
    $('#kickoutBtn').on('click', function() {
      return $.ajax({
        url: 'kickout/',
        type: 'post',
        dataType: 'json',
        data: {
          pk: $(this).data('pk')
        },
        success: (function(_this) {
          return function(data) {
            if (data.msg === 'okay') {
              $('#kickout-modal').modal('hide');
              return $("a.kickout[data-pk='" + ($(_this).data('pk')) + "']").parents('li.media').fadeOut('slow');
            }
          };
        })(this)
      });
    });
    $('a.approve').on('click', function() {
      return $.ajax({
        url: 'approve/',
        type: 'post',
        dataType: 'json',
        data: {
          pk: $(this).data('pk')
        },
        success: (function(_this) {
          return function(data) {
            if (data.msg === 'okay') {
              $(_this).hide();
              return $(_this).siblings('i.text-success').fadeIn('slow');
            }
          };
        })(this)
      });
    });
    return stickFooter();
  });

  window.uploadAvatar = function() {
    $('#avatar').hide();
    $('#iconHolder').show();
    return $.ajaxFileUpload({
      url: 'update-avatar/',
      secureurl: false,
      fileElementId: 'avatarHolder',
      dataType: 'json',
      success: function(data) {
        if (data.msg === 'okay') {
          $('#avatar').attr('src', data.path);
        } else {
          alert('Image No Larger Than 5M is Accepted.');
        }
        $('#iconHolder').hide();
        return window.setTimeout("$('#avatar').show()", 50);
      }
    });
  };

}).call(this);
