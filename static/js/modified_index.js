(async() => {
    let response = await fetch(`${window.origin}/get-graph`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify("Get data"),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });

    var svg = d3.select("svg"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    let responseString = await response.json();
    let responseJSON = JSON.parse(responseString);

    var g = svg.append("g")
        .attr("class", "everything");

    // -- replaced by @gl changes
    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(responseJSON.links)
        .enter().append("line");

    var node = g.append("g")
        .attr("class", "node")
        .selectAll(".nodes")
        .data(responseJSON.nodes)
        .enter().append("circle")
        .attr("r", 5.0)
        .attr("fill", "darkgray")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
       .text(function(d) { return d.name; });
    // -- replaced by @gl changes

    // ++ @gl changes start here
    // var link = svg.append("g")
    //     .attr("class", "links")
    //     .selectAll("line")
    //     .data(responseJSON.links)
    //     .enter().append("line");

    // var path = svg.append("svg:g")
    //     .attr("class", "paths")
    //     .selectAll("path")
    //     .data(responseJSON.links)
    //     .enter().append("svg:path")
    //     .attr("id",function(d,i) { return "linkId_" + i; })
    //     .attr("marker-end", function(d) { return "url(#" + d.type + ")"; });

    // var linktext = svg.append("svg:g")
    //     .attr("class", "linklabels")
    //     .selectAll("g.linklabelholder")
    //     .data(responseJSON.links)
    //     .enter().append("g")
    //     .attr("class", "linklabelholder")
    //     .append("text")
    //     .style("font-size", "9px")
    //     .attr("text-anchor", "middle")
    //     .attr("dx", 50)
    //     .attr("dy", 5)
    //     .style("fill","black")
    //     .append("textPath")
    //     .attr("xlink:href",function(d,i) { return "#linkId_" + i;})
    //     .text(function(d) {
    //         return "my text"; //Can be dynamic via d object
    //     });

    // var node = g.selectAll(".node")
    //     .data(responseJSON.nodes)
    //     .enter().append("g")
    //     .attr("class", "node")
    //     .call(d3.drag()
    //         .on("start", dragstarted)
    //         .on("drag", dragged)
    //         .on("end", dragended));
     
    // node.append("circle").attr("r", 5).attr("fill", "darkgray");
    // node.append("text").attr("dx", 6).text(function(d) { return d.name; });
    // ++ @gl changes end here


    simulation
        .nodes(responseJSON.nodes)
        .on("tick", ticked);

    simulation
        .force("link")
        .links(responseJSON.links);

    var zoom_handler = d3.zoom()
        .on("zoom", zoom_actions);

    zoom_handler(svg);

    function zoom_actions() {
        g.attr("transform", d3.event.transform)
    }

    function ticked() {
        // ++ @gl changes start here
        // path.attr("d", function(d) {
        //     var dx = d.target.x - d.source.x,
        //         dy = d.target.y - d.source.y;
        //     return "M" + d.source.x + "," + d.source.y + " L" + d.target.x + "," + d.target.y;
        // });
        // ++ @gl changes end here

        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

        // ++ @gl changes start here
        // node.attr("transform", function(d) {
        //     return "translate(" + d.x + "," + d.y + ")";
        // });
        // ++ @gl changes end here
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

})();