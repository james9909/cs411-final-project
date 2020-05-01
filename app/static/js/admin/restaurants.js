$("form[action='update']").submit(function(e) {
    e.preventDefault();

    let form = $(this);
    let restaurant_id = form.attr("id");
    let name = $(`#${restaurant_id}-name`).val();
    let address = $(`#${restaurant_id}-addr`).val();
    let rating = parseFloat($(`#${restaurant_id}-rating`).val());
    let latitude = parseFloat($(`#${restaurant_id}-lat`).val());
    let longitude = parseFloat($(`#${restaurant_id}-long`).val());
    let yelp_url = $(`#${restaurant_id}-url`).val();
    let categories = $(`#${restaurant_id}-categories`).val();
    $(`#${restaurant_id}-submit`).attr("disabled", "disabled");
    apiCall("POST", `/api/restaurants/${restaurant_id}`, {
        name: name,
        address: address,
        rating: rating,
        latitude: latitude,
        longitude: longitude,
        yelp_url: yelp_url,
        categories: categories
    },
        function(response) {
            $(`#${restaurant_id}-submit`).removeAttr("disabled", "disabled");
            window.location = "/admin/restaurants";
        },
        function(response) {
            $(`#${restaurant_id}-submit`).removeAttr("disabled", "disabled");
        }
    );
});

$("#add-form").submit(function(e) {
    e.preventDefault();

    let name = $(`#add-name`).val();
    let address = $(`#add-addr`).val();
    let rating = parseFloat($(`#add-rating`).val());
    let latitude = parseFloat($(`#add-lat`).val());
    let longitude = parseFloat($(`#add-long`).val());
    let yelp_url = $(`#add-url`).val();
    let categories = $(`#add-categories`).val();
    $(`#add-submit`).attr("disabled", "disabled");
    apiCall("POST", `/api/restaurants`, {
        name: name,
        address: address,
        rating: rating,
        latitude: latitude,
        longitude: longitude,
        yelp_url: yelp_url,
        categories: categories
    },
        function(response) {
            $(`#add-submit`).removeAttr("disabled", "disabled");
            window.location = "/admin/restaurants";
        },
        function(response) {
            $(`#add-submit`).removeAttr("disabled", "disabled");
        }
    );
});

function deleteRestaurant(id) {
    console.log(id)
    $(`#${id}-delete`).attr("disabled", "disabled");
    apiCall("DELETE", `/api/restaurants/${id}`, {}, function(response) {
        $(`#${id}-delete`).removeAttr("disabled", "disabled");
        window.location = "/admin/restaurants";
    }, function(response) {
        $(`#${id}-delete`).removeAttr("disabled", "disabled");
    });
}
