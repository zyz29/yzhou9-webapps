/* Wait until the DOM loads by wrapping our code in a callback to $. */
$(function() {

  /* Add click event listeners to the restaurant list items. This adds a
   * handler for each element matching the CSS selector
   * .restaurant-list-item. */
  $('.restaurant-list-item a').click(function(event) {

    /* Prevent the default link navigation behavior. */
    event.preventDefault();

    var $restaurant = $(this);
    var $categories = $restaurant.parents('.restaurant-list-item').find('.category-sublist');

    /* If the category list is shown, hide it. */
    if($categories.is(':visible')) {
      $categories.slideUp();
      return;
    }

    /* Fade out all other category lists. */
    $('.category-sublist').not($categories).slideUp();

    /* Get the category JSON data via Ajax. */
    $.ajax({
      type: 'GET',
      url: $restaurant.attr('href'),
      dataType: 'json'
    }).done(function(data) {

      /* This gets called if the Ajax call is successful. */

      /* We expect the JSON data to be in this form:
       *   [
       *     {
       *       "href": <url-of-category>,
       *       "name": <name-of-category>
       *     },
       *     ...
       *   ]
       */

      /* Empty out existing contents in the category list. */
      $categories.empty();

      /* Add a list item/link for each category received. */
      var categories = data;
      for(var i = 0, n = categories.length; i < n; ++i) {
        var category = categories[i];
        $categories.append(
          $('<a>')
            .addClass('list-group-item no-gutter')
            .attr('href', category.href)
            .append(
              $('<div>')
                .text(category.name)
                .addClass('list-group-item-heading no-gutter')
            )
        );
      }
      /* Slide the newly populated category list into view. */
      $categories.slideDown();
    }).fail(function() {

      /* This gets called if the Ajax call fails. */

      $categories.empty().slideUp();

      /* Create an alert box. */
      var $alert = (
        $('<div>')
          .text('Whoops! Something went wrong.')
          .addClass('alert')
          .addClass('alert-danger')
          .addClass('alert-dismissible')
          .attr('role', 'alert')
          .prepend(
            $('<button>')
              .attr('type', 'button')
              .addClass('close')
              .attr('data-dismiss', 'alert')
              .html('&times;')
          )
          .hide()
      );
      /* Add the alert to the alert container. */
      $('#alerts').append($alert);
      /* Slide the alert into view with an animation. */
      $alert.slideDown();
    });
  });
});
