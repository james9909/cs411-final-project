const starring = {};

function flip(attraction_id) {
    let span = $(`#${attraction_id}-star`);
    if (span.text().trim() === "star") {
        span.text("star_border");
    } else {
        span.text("star");
    }
}

function starAttraction(attraction_id) {
    if (starring[attraction_id]) {
        return;
    }
    starring[attraction_id] = true;
    apiCall("POST", `/api/attractions/${attraction_id}/favorite`, {}, function(response) {
        flip(attraction_id);
        starring[attraction_id] = false;
    }, function(response) {
        starring[attraction_id] = false;
    });
};

function starRestaurant(restaurant_id) {
    if (starring[restaurant_id]) {
        return;
    }
    starring[restaurant_id] = true;
    apiCall("POST", `/api/restaurants/${restaurant_id}/favorite`, {}, function(response) {
        flip(restaurant_id);
        starring[restaurant_id] = false;
    }, function(response) {
        starring[restaurant_id] = false;
    });
};
