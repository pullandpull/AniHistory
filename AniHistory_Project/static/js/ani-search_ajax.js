$(document).ready(function () {
  $('.loader-wrapper').fadeOut("slow");
  $('.spinner-border').hide();

  //search 
  $('#search').keyup(function () {
    $('.loader-wrapper').fadeIn('slow');
    var search = $(this).val();
    $.get('/aniHistory/search/', {
      query: search
    }, function (data) {

      $('.loader-wrapper').fadeOut('fast');
      $('.row').html(data);
    });
  });

  $('#anime_Search').keyup(function () {
    $('.loader-wrapper').fadeIn('slow');
    const query = $(this).val();
    const token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
      url: '/aniHistory/stream/anime/search/',
      type: 'POST',
      data: {
        search_anime: query,
        csrfmiddlewaretoken: token
      },
      dataType: 'html',
      success: function (response) {

        $('.loader-wrapper').fadeOut('fast');
        $('.row').html(response);
      }
    });
  });
  //season filter 
  $('.filter-by-season').click(function () {
    $('.loader-wrapper').fadeIn('slow');
    var season_value = $(this).attr('value_id');
    var season_year = $('#year').val();

    if (!season_year) {
      season_year = 2021
    };

    $.get('/aniHistory/archive/', {
      season: season_value,
      year: season_year
    }, function (data) {

      $('.loader-wrapper').fadeOut('fast');
      $('.row').html(data);
    });
  });

  // recommended
  $('.request-type').click(function () {
    $('.loader-wrapper').fadeIn('slow');
    var request_type = $(this).attr('value_id');
    $.get('/aniHistory/recommended/', {
      session_request: request_type
    }, function (data) {
      $('.loader-wrapper').fadeOut("fast");
      $('.row').html(data);
    });
  });

  // latest
  $('[data-request="stream"]').click(function () {
    $('.loader-wrapper').fadeIn('slow');
    $.get('/aniHistory/stream/anime/latest/', {},
      function (data) {
        $('loader-wrapper').fadeOut("fast");
        $('.row').html(data);
      });
  });

  //add bookmark  
  $('.btn-trigger').click(function (e) {
    e.stopImmediatePropagation();
    const btn_image = $(this);
    const anime_title = $(this).attr('data-name');
    const id = $(this).attr('data-id');
    const anime_vid_id = $(this).attr('data-vid-id');
    const anime_cover = $(this).attr('data-cover');
    const token = $('input[name = "csrfmiddlewaretoken"]').val();

    $.ajax({
      url: '/aniHistory/stream/anime/bookmark/',
      type: "POST",
      data: {
        csrfmiddlewaretoken: token,
        anime_name: anime_title,
        user_id: id,
        anime_video_id: anime_vid_id,
        anime_cover: anime_cover
      },
      dataType: 'text',
      success: function (response) {
        if (response == 'True') {
          btn_image.attr('src', '/static/images/heart_selected.png');
        } else if (response == 'False') {
          btn_image.attr('src', '/static/images/heart_default.png');
        };
      }
    });
  });
  /*
          $.get('/aniHistory/stream/anime/bookmark/', {
              anime_name: anime_title,
              user_id: id,
              anime_video_id: anime_vid_id,
              anime_cover: anime_cover
            },*/


  $('#input-search').keyup(function (e) {
    $('.loader-wrapper').fadeIn('slow');
    e.stopImmediatePropagation();
    const search = $(this).val();
    const token = $('input[name = "csrfmiddlewaretoken"]').val();
    $.ajax({
      url: '/aniHistory/account/anime/bookmarks/search/',
      type: "POST",
      data: {
        anime_name: search,
        csrfmiddlewaretoken: token
      },
      dataType: "html",
      success: function (response) {
        // handle returned data

        $('.loader-wrapper').fadeOut('fast');
        $('.row-results').html(response);
      }
    });
  });

  $('.filter-option').click(function () {
    $('.loader-wrapper').fadeIn('slow');
    by_value = $(this).attr('value_id');
    $.get('/aniHistory/account/anime/bookmarks/filter/', {
        filter_by: by_value
      },
      function (response) {
        $('.loader-wrapper').fadeOut('fast');
        $('.row-results').html(response);
      });
  });
});