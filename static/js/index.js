// Set url for to query the fighter data

map_data_url = "/api/map_data"

d3.json(map_data_url).then(data => {
 
console.log(data)

});
