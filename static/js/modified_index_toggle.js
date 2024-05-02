import { D3TopicNode, D3PaperNode, D3Link, D3Graph } from './d3_models.js';

const toggle = document.querySelector('#levelToggle');
const filterPapers = document.querySelector('#filterPapers');
const filterTopics = document.querySelector('#filterTopics');


// SVG set up
const width = document.documentElement.clientWidth; 
const height = document.documentElement.clientHeight;
var w = window;
var d = document;
var e = d.documentElement;

console.log("Width and height:");
console.log(width, height);

// var svg = d3.select("svg")
//     .attr("preserveAspectRatio", "xMidYMid meet")
//     .attr("viewBox", `0 0 ${width} ${height}`);
var svg = d3.select("svg")
    .attr("width", width)
    .attr("height", height);

// resize canvas when window change
function updateWindow(){
    x = w.innerWidth || e.clientWidth || g.clientWidth;
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;

    svg.attr("width", x).attr("height", y);
}
d3.select(window).on('resize.updatesvg', updateWindow);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(300)) // Increase the distance value to spread out the nodes
    .force("charge", d3.forceManyBody().strength(-500)) // Increase the magnitude of negative strength
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collide", d3.forceCollide().radius(10)); // Add a collision force to prevent overlap of nodes


var l2Graph;
var l1Graph;
var isLevel2 = true;
var showPapers = true;
var showTopics = true;

getL2Graph()
.then(
    (graph) => {
        l2Graph = graph;
        generateSvgGraph(graph);
    },
    error => console.log(error)
)



// Level toggle
// function toggleLevel() {
toggle.addEventListener('click', () => {
    isLevel2 = !isLevel2;
    console.log("Toggle level");

    // d3.select("svg").select("g").selectAll("g").exit().remove();
    // d3.select("svg").selectAll("g").exit().remove();
    svg.selectAll("*").remove();


    if (isLevel2) {
        if (!l2Graph) {
            console.log("fetch l2 graph");
            getL2Graph()
            .then(
                (graph) => {
                    l2Graph = graph;
                    console.log(graph);
                    generateSvgGraph(graph);
                },
                error => console.log(error)
            )
        } else {
            console.log("no need fetch l2graph");
            console.log(l2Graph);
            generateSvgGraph(l2Graph);
        }
    } else {
        if (!l1Graph) {
            getL1Graph()
            .then(
                (graph) => {
                    console.log(graph);
                    l1Graph = graph;
                    generateSvgGraph(graph);
                },
                error => console.log(error)
            )
        } else {
            generateSvgGraph(l1Graph);
        }
        // let graph = dummygraph();
        // l1Graph = graph;
        // generateSvgGraph(graph);
    }

});

async function getL2Graph() {
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
    
    let d3nodes = [];
    for (let resnode of responseJSON.nodes) {
        if (resnode.type === "topic") {
            d3nodes.push(new D3TopicNode(resnode.id, resnode.description));
        } else {
            d3nodes.push(new D3PaperNode(
                resnode.id,
//                resnode.arxiv_id,
               resnode.url,
//                resnode.citation_count,
                resnode.title,
                resnode.authors,
                resnode.abstract
//                resnode.publication_date,
//                resnode.references
            ));
        }
    }
    let d3links = [];
    for (let reslink of responseJSON.links) {
        // console.log(reslink.source);
        d3links.push(new D3Link(reslink.source, reslink.target, reslink.label));
    }
    // console.log(d3nodes);
    // console.log(d3links);

    let graph = new D3Graph(d3nodes, d3links);
    return graph;
}

async function getL1Graph() {
    let response = await fetch(`${window.origin}/get-l1-graph`, {
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
    
    let d3nodes = [];
    for (let node of responseJSON.nodes) {
        d3nodes.push(new D3TopicNode(node.id, node.description));
    }
    let d3links = [];
    for (let link of responseJSON.links) {
        d3links.push(new D3Link(link.source, link.target, link.label));
    }
    console.log(d3nodes);
    console.log(d3links);

    let graph = new D3Graph(d3nodes, d3links);
    return graph;
}

function dummygraph() {
    let nodes = [
        new D3TopicNode("one", "one"),
        new D3TopicNode("two", "two"),
        new D3TopicNode("three", "three"),
        new D3TopicNode("four", "four"),
        new D3TopicNode("five", "five")
    ]
    let edges = [
        new D3Link("one", "two", "label"),
        new D3Link("one", "three", "label"),
        new D3Link("two", "four", "label"),
        new D3Link("two", "five", "label")
    ]
    return new D3Graph(nodes, edges)
}

// ===============
// Filters
// ===============
filterPapers.addEventListener('click', () => {
    showPapers = !showPapers
    let nodes = svg.select("g").select(".node");
    let links = svg.select("g").select(".links");
    let linklabels = svg.select("g").select(".link-labels");
    if (showPapers) {
        nodes.selectAll("#node-paper").attr("visibility", "visible");
        nodes.selectAll("#node-paper").selectAll("circle").classed("node-circle", true);
        nodes.selectAll("#node-paper").selectAll("circle").classed("node-circle-hidden", false);
        links.selectAll(".paperpaper").attr("visibility", "visible");
        links.selectAll(".papertopic").attr("visibility", "visible");
        links.selectAll(".topicpaper").attr("visibility", "visible");
        linklabels.selectAll(".paperpaper").attr("visibility", "visible");
        linklabels.selectAll(".papertopic").attr("visibility", "visible");
        linklabels.selectAll(".topicpaper").attr("visibility", "visible");
    } else {
        nodes.selectAll("#node-paper").attr("visibility", "hidden");
        nodes.selectAll("#node-paper").selectAll("circle").classed("node-circle", false);
        nodes.selectAll("#node-paper").selectAll("circle").classed("node-circle-hidden", true);
        links.selectAll(".paperpaper").attr("visibility", "hidden");
        links.selectAll(".papertopic").attr("visibility", "hidden");
        links.selectAll(".topicpaper").attr("visibility", "hidden");
        linklabels.selectAll(".paperpaper").attr("visibility", "hidden");
        linklabels.selectAll(".papertopic").attr("visibility", "hidden");
        linklabels.selectAll(".topicpaper").attr("visibility", "hidden");
    }
});

filterTopics.addEventListener('click', () => {
    showTopics = !showTopics
    let nodes = svg.select("g").select(".node");
    let links = svg.select("g").select(".links");
    let linklabels = svg.select("g").select(".link-labels");
    if (showTopics) {
        nodes.selectAll("#node-topic").attr("visibility", "visible");
        nodes.selectAll("#node-topic").selectAll("circle").classed("node-circle", true);
        nodes.selectAll("#node-topic").selectAll("circle").classed("node-circle-hidden", false);
        links.selectAll(".topictopic").attr("visibility", "visible");
        links.selectAll(".papertopic").attr("visibility", "visible");
        links.selectAll(".topicpaper").attr("visibility", "visible");
        linklabels.selectAll(".topictopic").attr("visibility", "visible");
        linklabels.selectAll(".papertopic").attr("visibility", "visible");
        linklabels.selectAll(".topicpaper").attr("visibility", "visible");
    } else {
        nodes.selectAll("#node-topic").attr("visibility", "hidden");
        nodes.selectAll("#node-topic").selectAll("circle").classed("node-circle", false);
        nodes.selectAll("#node-topic").selectAll("circle").classed("node-circle-hidden", true);
        links.selectAll(".topictopic").attr("visibility", "hidden");
        links.selectAll(".papertopic").attr("visibility", "hidden");
        links.selectAll(".topicpaper").attr("visibility", "hidden");
        linklabels.selectAll(".topictopic").attr("visibility", "hidden");
        linklabels.selectAll(".papertopic").attr("visibility", "hidden");
        linklabels.selectAll(".topicpaper").attr("visibility", "hidden");
    }
});



function isPaper(id) {
    // hacky way to check if the node is a paper or topic node from the id
    // to check if the edge is a paper-paper / paper-topic / topic-topic edge
    return id.startsWith('arxiv') || (id.length == 40 && /\d/.test(id) && id.indexOf(' ') == -1)
}

function generateSvgGraph(graph) {
    let d3links = graph.edges;
    let d3nodes = graph.nodes;
    console.log(d3links);
    console.log(d3nodes);

    var g = svg.append("g")
        .attr("class", "everything");

    // Define the marker for the arrow heads
    svg.append("defs").selectAll("marker")
        .data(["end"])      // Different marker types can be defined here
        .enter().append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 70)   // Controls the distance of the marker from the node
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto") 
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("class", "arrowHead")
        .style("fill", "#999"); // Set the color of the arrow

    var link = g.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(d3links)
        .enter()
        .append("line")
            .attr("id", d => {
                if (typeof d.source === 'string') {
                    return `link-${d.source.replace(/\s+/g, '-')}-${d.target.replace(/\s+/g, '-')}`
                }
                return `link-${d.source.id.replace(/\s+/g, '-')}-${d.target.id.replace(/\s+/g, '-')}`
            }) // Add ID to each link for hover over features
            .attr("class", d => {
                if (typeof d.source === 'string') {
                    var sourceType = isPaper(d.source) ? "paper" : "topic";
                    var targetType = isPaper(d.target) ? "paper" : "topic";
                    return "normal-lines " + sourceType + targetType;
                } else {
                    return "normal-lines " + d.source.type + d.target.type;
                }
            }) 
            .attr("marker-end", "url(#arrow)");  // Use the arrow marker

    // Append text labels to each link
    var linkLabel = g.append("g")
        .attr("class", "link-labels")
        .selectAll("text")
        .data(d3links)
        .enter().append("text")
            .attr("text-anchor", "middle") // Ensure labels are centered along the link
            .attr("font-size", "10px")
            // .attr("class", "link-labels")
            // .attr("id", d => `link-label-${d.getLabel().replace(/\s+/g, '-')}`) // Set ID replacing spaces with hyphens
            // .attr("id", d => `link-label-${d.source.replace(/\s+/g, '-')}-${d.target.replace(/\s+/g, '-')}`) // Set ID replacing spaces with hyphens
            .attr("id", d => {
                if (typeof d.source === 'string') {
                    return `link-label-${d.source.replace(/\s+/g, '-')}-${d.target.replace(/\s+/g, '-')}`
                }
                return `link-label-${d.source.id.replace(/\s+/g, '-')}-${d.target.id.replace(/\s+/g, '-')}`
            }) // Add ID to each link for hover over features
            .text(d => d.getLabel())
            .attr("class", d => {
                if (typeof d.source === 'string') {
                    var sourceType = isPaper(d.source) ? "paper" : "topic";
                    var targetType = isPaper(d.target) ? "paper" : "topic";
                    return "link-labels " + sourceType + targetType;
                } else {
                    return "link-labels " + d.source.type + d.target.type;
                }
            }); 
        
    var node = g.append("g")
        .attr("class", "node")
        .selectAll(".nodes")
        .data(d3nodes)
        .enter().append("g")  // Append a 'g' element for each node
        .attr("id", d => d.type == "topic" ? "node-topic" : "node-paper")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));
    
    // Append circle to each node group
    node.append("circle")
        .attr("class", "node-circle")
        .attr("id", d => `node-${d.id.replace(/\s+/g, '-')}`) // Add ID to each node for hover over features
        .attr("r", 50)
        .attr("fill", d => {
            if (d.type === "topic") {
                return `#80f2db`;
            } else if (d.type === "paper") {
                return `gray`;
            }
        })
        .on("mouseover", function(D3NodeObject) {
            console.log("d: ", D3NodeObject);
            highlightNode.call(this, D3NodeObject);
            if (D3NodeObject.type === "topic") {
                updateSidebar(`<b>Hovered on node:</b> ${D3NodeObject.id}` + "<br> <b>Description:</b> " + D3NodeObject.description);
            } else if (D3NodeObject.type === "paper") {
                updateSidebar(`<b>Hovered on node:</b> ${D3NodeObject.title}<br> <b>Authors:</b> ${D3NodeObject.authors}<br> <b><a href=${D3NodeObject.url} target="_blank">Link</a></b><br> <b>Abstract:</b> ${D3NodeObject.abstract}`);
            }
        })
        .on("mouseout", resetHighlights)
        .on("click", function(D3NodeObject) {
            if (D3NodeObject.url) {
                window.open(D3NodeObject.url, '_blank');
            }
        });
    
    // Append text to each node group
    node.append("text")
        .attr("class", "node-labels")
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
    
    
    simulation
        .nodes(d3nodes)
        .on("tick", ticked);

    simulation
        .force("link")
        .links(d3links);

    // need this to force the force simulation to spread the nodes around again
    simulation.restart();


    var zoom_handler = d3.zoom()
        .on("zoom", zoom_actions);

    zoom_handler(svg);

    function zoom_actions() {
        g.attr("transform", d3.event.transform)
    }

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
        
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
        d.subject.fixed = true;
        
        d.fx = null;
        d.fy = null;
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
    function highlightNode(D3NodeObject) { 
        // Set all nodes and links to faded state
        svg.selectAll(".node circle").classed("faded", true);
        svg.selectAll(".links line").classed("faded", true);
        svg.selectAll(".link-labels").classed("faded", true);
        svg.selectAll(".node-labels").classed("faded", true);

        // Highlight the current node and node labels
        d3.select(this).classed("highlight-node", true).classed("faded", false);
        d3.select(this.parentNode).select("text.node-labels").classed("faded", false);
        
        // Highlight all connected links and the nodes at their ends
        var count = 0;
        d3links.forEach(link => { // link refers to the D3Link object
            // console.log(link.source, link.target, D3NodeObject)
            // console.log(returnMatch(link, d))
            if (link.source === D3NodeObject || link.target === D3NodeObject) {
                count += 1;
                // Highlight this link
                d3.select(`#link-${link.source.id.replace(/\s+/g, '-')}-${link.target.id.replace(/\s+/g, '-')}`)
                .classed("highlight-link", true)
                .classed("faded", false);

                // Highlight the link label
                d3.select(`#link-label-${link.source.id.replace(/\s+/g, '-')}-${link.target.id.replace(/\s+/g, '-')}`).classed("faded", false);

                // Highlight the connected nodes
                var sourceNode = d3.select(`#node-${link.source.id.replace(/\s+/g, '-')}`);
                var targetNode = d3.select(`#node-${link.target.id.replace(/\s+/g, '-')}`);
                sourceNode.classed("highlight-node", true).classed("faded", false);
                d3.select(sourceNode.node().parentNode).select("text.node-labels").classed("faded", false);
                targetNode.classed("highlight-node", true).classed("faded", false);
                d3.select(targetNode.node().parentNode).select("text.node-labels").classed("faded", false);
            }
        })
        
        console.log("count: ", count);
    }

    // Function to reset highlights
    function resetHighlights() {
        svg.selectAll(".node circle").classed("highlight-node", false).classed("faded", false);
        svg.selectAll(".links line").classed("highlight-link", false).classed("faded", false);
        svg.selectAll(".link-labels").classed("faded", false);
        svg.selectAll(".node-labels").classed("faded", false);
    }

}
