//$(function() {
//			  $('a#like').on('click', function() {
//				$.getJSON('/background_process', {
//				  like: $('like').val(),
//				}, function(data) {
//				  $("#like").text(data.result);
//				});
//				return false;
//			  });
//			});


 $(document).ready(function() {

    $(document).on('click', '.page-link', function(event) {

      var link = $(this).attr('href');
      searchResults(link);

  });
});

var searchResults = function(link) {
      req=$.ajax({
        data : {
          parameter1: $('input[name="parameter1"]').val()
        },
        type: 'POST',
        url: link

      });
      req.done(function(data) {
        $('#results').html(data);
      })
  };
