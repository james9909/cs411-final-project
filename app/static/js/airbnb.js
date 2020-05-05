const starring = {};

function flip(attraction_id) {
    let span = $(`#${attraction_id}-star`);
    if (span.text().trim() === "star") {
        span.text("star_border");
    } else {
        span.text("star");
    }
}

function star(attraction_id) {
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
