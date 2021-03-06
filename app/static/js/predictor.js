
// Create selector for fighter 1
fighter_list_url = "/api/fighter_list"

d3.json(fighter_list_url).then((fighter) => {
    fighter_list = fighter.Name;
    for (let [key, Name] of Object.entries(fighter_list)) {
        var option = d3.select("#selFighter1").append("option");
        option.text(Name);
        option.attr("value",Name);
      };
});

// Create selector for fighter 2
fighter_list_url = "/api/fighter_list"

d3.json(fighter_list_url).then((fighter) => {
    fighter_list = fighter.Name;
    for (let [key, Name] of Object.entries(fighter_list)) {
        var option = d3.select("#selFighter2").append("option");
        option.text(Name);
        option.attr("value",Name);
      };
});

// Create function for showing fighter data 1
function updateFighter1(){

    var table1 = d3.select("#table1");

    table1.html("");

    var dropdownMenu = d3.select("#selFighter1");

    var fighter = dropdownMenu.property("value");

    url = "/api/predictor/" + fighter;

    d3.json(url).then((data) => {
        for (let [key, value] of Object.entries(data)) {
            var newList = table1.append("tr");
            var key_col = newList.append("td");
            key_col.text(`${key}`);

            for (let [key1, value1] of Object.entries(value)) {
                var value_col = newList.append("td");
                value_col.text(`${value1}`);
            };
          };
    });
};

// Create function for showing fighter data 2
function updateFighter2(){

    var table1 = d3.select("#table2");

    table1.html("");

    var dropdownMenu = d3.select("#selFighter2");

    var fighter = dropdownMenu.property("value");

    url = "/api/predictor/" + fighter;

    d3.json(url).then((data) => {
        for (let [key, value] of Object.entries(data)) {
            var newList = table1.append("tr");
            var key_col = newList.append("td");
            key_col.text(`${key}`);

            for (let [key1, value1] of Object.entries(value)) {
                var value_col = newList.append("td");
                value_col.text(`${value1}`);
            };
          };
    });
};

// Create function for showing fighter data
function predictwinner(){

    var outcome = d3.select("#winner");

    outcome.html("");

    var dropdownMenu1 = d3.select("#selFighter1");
    var dropdownMenu2 = d3.select("#selFighter2");

    var fighter1 = dropdownMenu1.property("value");
    var fighter2 = dropdownMenu2.property("value");

    fight_predict_url = "/api/predictor/" + fighter1 + "/" + fighter2;

    d3.json(fight_predict_url).then(data => {
        for (let [key, value] of Object.entries(data)) {
            outcome.text(`${value}`);
        }
    });
};

// Call functions when a change takes place to the DOM
d3.selectAll("#selFighter1").on("change", updateFighter1);
d3.selectAll("#selFighter2").on("change", updateFighter2);
d3.selectAll("#predictbutton").on("click", predictwinner);