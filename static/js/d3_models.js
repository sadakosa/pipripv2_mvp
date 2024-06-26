// This contains the models for the d3 objects
// Not to be confused with the models for the Memgraph objects

export class D3Node {
    type;
    id;
    constructor(type, id) {
        this.type = type;
        this.id = id;
    }
    getLabel() { return "Unknown"; }
    getDetails() { return "Details not found"; }
}

export class D3TopicNode extends D3Node {
    constructor(id, description) {
        super("topic", id);
        this.description = description;
    }

    getLabel() {
        return this.id;
    }

    getDetails() {
        return `Topic: ${this.id}\Description: ${this.description}`;
    }
}

export class D3PaperNode extends D3Node {
    constructor(id, url, title, authors, abstract) {
        super("paper", id);
        this.title = title;
        this.url = url;
        this.authors = authors;
        this.abstract = abstract;
    }

    getLabel() {
        return this.title;
    }

    getDetails() {
        return `Authors: ${this.authors}\SS ID: ${this.ss_id}\nTitle: ${this.title}\nLink: ${this.url}\nAbstract: ${this.abstract}`;
    }
}

export class D3Link {
    constructor(source, target, relationship_type) {
        this.source = source;
        this.target = target;
        this.relationship_type = relationship_type;
    }

    getLabel() {
        return this.relationship_type;
    }
}

export class D3Graph {
    nodes;
    edges;
    constructor(nodes, edges) {
        this.nodes = nodes;
        this.edges = edges;
    }
}