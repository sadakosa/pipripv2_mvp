// This contains the models for the d3 objects
// Not to be confused with the models for the Memgraph objects

export class D3Node {
    type;
    id;
    constructor(type, id) {
        this.type = type;
        this.id = id;
    }
    getLabel() { return ""; }
    getDetails() { return ""; }
}

export class D3TopicNode extends D3Node {
    name;
    summary;
    constructor(id, name, summary) {
        super("topic", id);
        this.name = name;
        this.summary = summary;
    }

    getLabel() {
        return this.name;
    }

    getDetails() {
        return `Name: ${this.name}\nSummary: ${this.summary}`;
    }
}

export class D3PaperNode extends D3Node {
    name;
    author;
    title;
    summary;
    constructor(id, name, author, title, summary) {
        super("paper", id);
        this.name = name;
        this.author = author;
        this.title = title;
        this.summary = summary;
    }

    getLabel() {
        return this.name;
    }

    getDetails() {
        return `Author: ${this.author}\nName: ${this.name}\nTitle: ${this.title}\nSummary: ${this.summary}`;
    }
}

export class D3Link {
    source;
    target;
    constructor(source, target, relationship_type) {
        this.source = source;
        this.target = target;
        this.relationship_type = relationship_type;
    }
}