$(document).ready(function () {
  $('.loader-wrapper').fadeOut("slow");

  $('.spinner-border').hide();

  //search 
  $('#search').keyup(function () {
    var search = $(this).val();
    $.get('/aniHistory/search/', {
      query: search
    }, function (data) {
      $('.search_results').html(data);
    });
  });
  // search per press load 
  $('#search').keydown(function () {
    $('.spinner-border').show();
  });

  $('#anime_Search').keyup(function () {
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
        $('.row').html(response);
      }
    });
  });
  //season filter 
  $('.filter-by-season').click(function () {
    var season_value = $(this).attr('value_id');
    var season_year = $('#year').val();

    if (!season_year) {
      season_year = 2021
    };

    $.get('/aniHistory/archive/', {
      season: season_value,
      year: season_year
    }, function (data) {
      $('.search_results').html(data);
    });
  });

  // recommended
  $('.request-type').click(function () {
    var request_type = $(this).attr('value_id');
    $.get('/aniHistory/recommended/', {
      session_request: request_type
    }, function (data) {
      $('.search_results').html(data);
    });
  });

  // latest
  $('[data-request="stream"]').click(function () {
    $.get('/aniHistory/stream/anime/latest/', {},
      function (data) {
        $('loader-wrapper').fadeOut("slow");
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

    $.get('/aniHistory/stream/anime/bookmark/', {
        anime_name: anime_title,
        user_id: id,
        anime_video_id: anime_vid_id,
        anime_cover: anime_cover
      },

      function (data) {
        if (data == 'True') {
          btn_image.attr('src', '/static/images/heart_selected.png');
        } else if (data == 'False') {
          btn_image.attr('src', '/static/images/heart_default.png');
        };
      });
  });

  $('#input-search').keyup(function (e) {
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
        $('.row-results').html(response);
      }
    });
  });

  $('.filter-option').click(function(){
    by_value = $(this).attr('value_id');
    $.get('/aniHistory/account/anime/bookmarks/filter/',{
      filter_by: by_value
    },
    function(response){
      $('.row-results').html(response);
    });
  });
});