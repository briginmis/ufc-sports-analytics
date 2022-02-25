// Create selector for fighter 1
fighter_list_url = "/api/fighter_list"

d3.json(fighter_list_url).then((fighter) => {
    fighter_list = fighter.name;
    for (let [key, name] of Object.entries(fighter_list)) {
        var option = d3.select("#selFighter1").append("option");
        option.text(name);
        option.attr("value",name);
      };
});

// Create selector for fighter 2
fighter_list_url = "/api/fighter_list"

d3.json(fighter_list_url).then((fighter) => {
    fighter_list = fighter.name;
    for (let [key, name] of Object.entries(fighter_list)) {
        var option = d3.select("#selFighter2").append("option");
        option.text(name);
        option.attr("value",name);
      };
});

// Create function for showing fighter data
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

// Create function for showing fighter data
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

// Call functions when a change takes place to the DOM
d3.selectAll("#selFighter1").on("change", updateFighter1);
d3.selectAll("#selFighter2").on("change", updateFighter2);

