$(document).ready(function(){
  $('.spinner-border').hide();

  $('#search').keyup(function(){
    var search = $(this).val();
      $.get('/aniHistory/search/',{query:search}, function(data){
        $('.search_results').html(data);
    });
  });
  
  $('#search').keydown(function(){
    $('.spinner-border').show();
  }); 
  
  $('.dropdown-item').click(function(){
    var season_value = $(this).attr('value_id');
    var season_year = $('#year').val();
   
    if(season_year == null){
      season_year = 2021
    };

    $.get('/aniHistory/archive/',{season:season_value, year:season_year}, function(data){
      $('.search_results').html(data);
    });
  });
  
  $('.request-type').click(function(){
    var request_type = $(this).attr('value_id'); 
    $.get('/aniHistory/recommended/',{session_request:request_type},function(data){
      $('.search_results').html(data);
    });
  });

});
