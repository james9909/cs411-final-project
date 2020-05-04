$("form[action='update']").submit(function(e) {
    e.preventDefault();

    let form = $(this);
    let attraction_id = form.attr("id");
    let name = $(`#${attraction_id}-name`).val();
    let address = $(`#${attraction_id}-addr`).val();
    let rating = parseFloat($(`#${attraction_id}-rating`).val());
    let latitude = parseFloat($(`#${attraction_id}-lat`).val());
    let longitude = parseFloat($(`#${attraction_id}-long`).val());
    $(`#${attraction_id}-submit`).attr("disabled", "disabled");
    apiCall("POST", `/api/attractions/${attraction_id}`, {
        name,
        address,
        rating,
        latitude,
        longitude
    },
        function(response) {
            $(`#${attraction_id}-submit`).removeAttr("disabled", "disabled");
            location.reload();
        },
        function(response) {
            $(`#${attraction_id}-submit`).removeAttr("disabled", "disabled");
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
    $(`#add-submit`).attr("disabled", "disabled");
    apiCall("POST", `/api/attractions`, {
        name,
        address,
        rating,
        latitude,
        longitude
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

function deleteAttraction(id) {
    $(`#${id}-delete`).attr("disabled", "disabled");
    apiCall("DELETE", `/api/attractions/${id}`, {}, function(response) {
        $(`#${id}-delete`).removeAttr("disabled", "disabled");
        location.reload();
    }, function(response) {
        $(`#${id}-delete`).removeAttr("disabled", "disabled");
    });
}
