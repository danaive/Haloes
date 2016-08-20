// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var score;
    $('a[href$="person/"]').addClass('current');
    $('[href="#logout"]').on('click', function() {
      return $.ajax({
        url: 'sign-out/',
        type: 'post',
        dataType: 'json',
        success: function() {
          return location.href = '/';
        }
      });
    });
    $('.alert').on('click', function() {
      return $(this).fadeOut();
    });
    $('#updateBtn').on('click', function() {
      $(this).find('i').toggleClass('fa-angle-double-down').toggleClass('fa-angle-double-up');
      $('.alert').hide();
      return $('#updateForm').fadeToggle();
    });
    $('#cancelBtn').on('click', function() {
      return $('#updateForm').fadeOut();
    });
    $('#confBtn').on('click', function() {
      return $.ajax({
        url: 'update-info/',
        type: 'post',
        dataType: 'json',
        data: {
          major: $('#updateMajor').val(),
          school: $('#updateSchool').val(),
          email: $('#updateEmail').val(),
          blog: $('#updateBlog').val(),
          motto: $('#updateMotto').val()
        },
        success: function(data) {
          if (data.msg === 'okay') {
            $('.alert-success').fadeIn();
            window.setTimeout("$('#updateForm').fadeOut()", 1000);
            $('#infoMajor').text(data.major);
            $('#infoSchool').text(data.school);
            $('#infoEmail').text(data.email);
            $('#infoBlog').text(data.blog);
            return $('#infoMotto').text(data.motto);
          }
        }
      });
    });
    if ($('#followBtn').data('follow')) {
      $('#unfollowBtn').show();
    } else {
      $('#followBtn').show();
    }
    $('[id$="followBtn"]').on('click', function() {
      $(this).hide();
      return $.ajax({
        url: '/person/follow/',
        type: 'post',
        dataType: 'json',
        data: {
          username: $('#nickname').text()
        },
        success: (function(_this) {
          return function(data) {
            if (data.msg === 'okay') {
              if ($(_this).attr('id').length === 9) {
                return $('#unfollowBtn').fadeIn();
              } else {
                return $('#followBtn').fadeIn();
              }
            }
          };
        })(this)
      });
    });
    score = [];
    $.ajax({
      url: '/person/get-score/',
      type: 'post',
      dataType: 'json',
      data: {
        username: $('#nickname').text()
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
    $('[data-toggle="tooltip"]').tooltip();
    $('#avatar').on('click', function() {
      return $('#avatarHolder').click();
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
