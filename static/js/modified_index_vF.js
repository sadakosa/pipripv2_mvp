import { D3TopicNode, D3PaperNode, D3Link } from './d3_models.js';

(async() => {
    // === Fetch data about graph (nodes and links)
    let response = await fetch(`${window.origin}/get-graph`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify("Get data"),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    });

    let responseString = await response.json();
    let responseJSON = JSON.parse(responseString);
    // console.log(responseJSON);

    let d3nodes = [];
    for (node of responseJSON.nodes) {
        if (node.type === "topic") {
            d3nodes.push(new D3TopicNode(node.id, node.description));
        } else {
            d3nodes.push(new D3PaperNode(
                node.id,
//                node.arxiv_id,
//                node.url,
//                node.citation_count,
                node.title,
                node.authors,
                node.abstract
//                node.publication_date,
//                node.references
            ));
        }
    }
    let d3links = [];
    for (link of responseJSON.links) {
        d3links.push(new D3Link(link.source, link.target, link.label));
    }
    // console.log(d3nodes);
    // console.log(d3links);

    // === Create d3 graph
    const width = document.documentElement.clientWidth; 
    const height = document.documentElement.clientHeight * 0.9;

    console.log("Width and height:");
    console.log(width, height);

    var svg = d3.select("svg")
        .attr("preserveAspectRatio", "xMidYMid meet")
        .attr("viewBox", `0 0 ${width} ${height}`);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(300)) // Increase the distance value to spread out the nodes
        .force("charge", d3.forceManyBody().strength(-500)) // Increase the magnitude of negative strength
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collide", d3.forceCollide().radius(10)); // Add a collision force to prevent overlap of nodes

    var g = svg.append("g")
        .attr("class", "everything");

    // -- replaced by @gl changes
    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(d3links)
        .enter()
        .append("line")
            .attr("id", d => `link-${d.source}-${d.target}`) // Add ID to each link for hover over features
            .attr("class", "normal-lines") 

    // Append text labels to each link
    var linkLabel = g.append("g")
        .attr("class", "link-labels")
        .selectAll("text")
        .data(d3links)
        .enter().append("text")
        .attr("text-anchor", "middle") // Ensure labels are centered along the link
        .attr("font-size", "10px")
        .text(d => d.getLabel()); 
    
    var node = g.append("g")
        .attr("class", "node")
        .selectAll(".nodes")
        .data(d3nodes)
        .enter().append("g")  // Append a 'g' element for each node
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
    
    // Append circle to each node group
    node.append("circle")
        .attr("id", d => `node-${d.id}`) // Added ID to each node for hover over features
        .attr("r", 50)
        .attr("fill", d => {
            if (d.type === "topic") {
                return `#FFF0F5`;
            } else if (d.type === "paper") {
                return `gray`;
            }
        })
        .on("mouseover", function(d) {
            highlightNode.call(this, d);

            if (d.type === "topic") {
                updateSidebar(`<b>Hovered on node:</b> ${d.id}` + "<br> <b>Description:</b> " + d.description);
            } else if (d.type === "paper") {
                updateSidebar(`<b>Hovered on node:</b> ${d.title}<br> <b>Authors:</b> ${d.authors}<br> <b>Abstract:</b> ${d.abstract}`);
            }
        })
        .on("mouseout", resetHighlights)
        .on("click", function(d) {
            if (d.type === "topic") {
                updateSidebar(`<b>Clicked on node:</b> ${d.id}` + "<br> <b>Description:</b> " + d.description);
            } else if (d.type === "paper") {
                updateSidebar(`<b>Clicked on node:</b> ${d.title}<br> <b>Authors:</b> ${d.authors}<br> <b>Abstract:</b> ${d.abstract}`);
            }
        });


    // Append text to each node group
    node.append("text")
        .attr("x", 0) // Center text horizontally on the circle's center
        .attr("y", ".35em") // Center text vertically relative to circle
        .attr("text-anchor", "middle") // Align text around its middle point
        .each(function(d) {
            const lines = splitText(d.getLabel(), 30); 
            const line_count = lines.length;
            const line_height = 1.2;  // Line height in ems
            const initial_offset = -(line_height / 2) * (line_count - 1) + "em";  // Vertical shift to center the block
            
            const tspans = d3.select(this).selectAll('tspan')
                .data(lines)
                .enter()
                .append('tspan')
                .attr("x", 0) 
                .attr("dy", (d, i) => i === 0 ? initial_offset : `${line_height}em`)  // Adjust vertical position
                .text(d => d);
        })
        .style("font-size", "12px")
        .style("font-family", "Arial, sans-serif");


    function splitText(text, maxLength) {
        let words = text.split(/\s+/);
        let lines = [];
        let currentLine = words[0];
    
        for (let i = 1; i < words.length; i++) {
            let word = words[i];
            if (currentLine.length + word.length + 1 <= maxLength) {
                currentLine += " " + word;
            } else {
                lines.push(currentLine);
                currentLine = word;
            }
        }
        lines.push(currentLine);

        return lines; // Returns an array of lines
    }

    // To add hover over display of node details
    // node.append("title")
    //     .text(d => d.getDetails());
    
    
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
        .nodes(d3nodes)
        .on("tick", ticked);

    simulation
        .force("link")
        .links(d3links);


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
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
            // ++ @cc changes start here
            // .attr("cx", function(d) { return d.x; })
            // .attr("cy", function(d) { return d.y; });
            // ++ @cc changes end here

        // ++ @gl changes start here
        // node.attr("transform", function(d) {
        //     return "translate(" + d.x + "," + d.y + ")";
        // });
        // ++ @gl changes end here
        
        // Position the link labels at the midpoint of each link
        linkLabel
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);
        
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
        
        if (!d.fixed) { 
            d.fixed = true; 
        }
    }

    window.addEventListener("resize", function() {
    // Code to handle resizing or rerendering of SVG
        var width = document.documentElement.clientWidth;  
        var height = document.documentElement.clientHeight * 0.9; 
        svg.attr('viewBox', `0 0 ${width} ${height}`);
    });

    function updateSidebar(content) {
        document.getElementById('sidebar-content').innerHTML = content;
    }

    
    // =============================================================
    // Function to highlight nodes and links when hovered over
    // =============================================================

    // Function to highlight nodes and links
    function highlightNode(d) {
        // Set all nodes and links to faded state
        svg.selectAll(".node circle").classed("faded", true);
        svg.selectAll(".links line").classed("faded", true);

        // Highlight the current node
        d3.select(this).classed("highlight-node", true).classed("faded", false);
        
        // Highlight all connected links and the nodes at their ends
        d3links.forEach(link => {
            console.log(link.source, link.target, d)
            console.log(returnMatch(link, d))
            if (link.source === d || link.target === d) {
                // Highlight this link
                d3.select(`#link-${link.source.id}-${link.target.id}`).classed("highlight-link", true).classed("faded", false);
                // Highlight the connected nodes
                d3.select(`#node-${link.source.id}`).classed("highlight-node", true).classed("faded", false);
                d3.select(`#node-${link.target.id}`).classed("highlight-node", true).classed("faded", false);
            }
        });
    }

    function returnMatch(link, d) {
        if (link.source === d || link.target === d) {
            return [link.source.id, d.id];
        } else {
            return "no match";
        }
    }

    // Function to reset highlights
    function resetHighlights() {
        svg.selectAll(".node circle").classed("highlight-node", false).classed("faded", false);
        svg.selectAll(".links line").classed("highlight-link", false).classed("faded", false);
    }

})();