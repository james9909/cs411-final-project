$("form[action='update']").submit(function(e) {
    e.preventDefault();

    let form = $(this);
    let airbnb_id = form.attr("id");
    let name = $(`#${airbnb_id}-name`).val();
    let amenities = $(`#${airbnb_id}-amenities`).val();
    let neighborhood = $(`#${airbnb_id}-neighborhood`).val();
    let minimum_nights = parseInt($(`#${airbnb_id}-min_nights`).val());
    let reviews_per_month = parseFloat($(`#${airbnb_id}-reviews`).val());
    let rating = parseFloat($(`#${airbnb_id}-rating`).val());
    let latitude = parseFloat($(`#${airbnb_id}-lat`).val());
    let longitude = parseFloat($(`#${airbnb_id}-long`).val());
    let airbnb_url = $(`#${airbnb_id}-airbnb_url`).val();
    let image_url = $(`#${airbnb_id}-image_url`).val();
    let price = parseFloat($(`#${airbnb_id}-price`).val());
    $(`#${airbnb_id}-submit`).attr("disabled", "disabled");
    apiCall("POST", `/api/airbnbs/${airbnb_id}`, {
        name,
        amenities,
        neighborhood,
        minimum_nights,
        reviews_per_month,
        rating,
        latitude,
        longitude,
        airbnb_url,
        image_url,
        price
    },
        function(response) {
            $(`#${airbnb_id}-submit`).removeAttr("disabled", "disabled");
            location.reload();
        },
        function(response) {
            $(`#${airbnb_id}-submit`).removeAttr("disabled", "disabled");
        }
    );
});

$("#add-form").submit(function(e) {
    e.preventDefault();

    let name = $(`#add-name`).val();
    let amenities = $(`#add-amenities`).val();
    let neighborhood = $(`#add-neighborhood`).val();
    let minimum_nights = parseInt($(`#add-min_nights`).val());
    let reviews_per_month = parseFloat($(`#add-reviews`).val());
    let rating = parseFloat($(`#add-rating`).val());
    let latitude = parseFloat($(`#add-lat`).val());
    let longitude = parseFloat($(`#add-long`).val());
    let airbnb_url = $(`#add-airbnb_url`).val();
    let image_url = $(`#add-image_url`).val();
    let price = parseFloat($(`#add-price`).val());
    $(`#add-submit`).attr("disabled", "disabled");
    apiCall("POST", `/api/airbnbs`, {
        name,
        amenities,
        neighborhood,
        minimum_nights,
        reviews_per_month,
        rating,
        latitude,
        longitude,
        airbnb_url,
        image_url,
        price
    },
        function(response) {
            $(`#add-submit`).removeAttr("disabled", "disabled");
            location.reload();
        },
        function(response) {
            $(`#add-submit`).removeAttr("disabled", "disabled");
        }
    );
});

function deleteAirbnb(id) {
    $(`#${id}-delete`).attr("disabled", "disabled");
    apiCall("DELETE", `/api/airbnbs/${id}`, {}, function(response) {
        $(`#${id}-delete`).removeAttr("disabled", "disabled");
        location.reload();
    }, function(response) {
        $(`#${id}-delete`).removeAttr("disabled", "disabled");
    });
}
