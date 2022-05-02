import React from "react";
import './App.css';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';
import dagre from 'cytoscape-dagre';

cytoscape.use(dagre);


const cytoscapeStylesheet = [
  {
    selector: "node",
    style: {
      "background-color": "#F5F5DC",
      width: "label",
      height: "label",
      padding: "20px",
      shape: "rectangle",
      'text-wrap': 'wrap',
      label: 'My multiline\nlabel',
    }
  },
  {
    selector: "node[label]",
    style: {
      label: "data(label)",
      "font-size": "12",
      color: "black",
      "text-halign": "center",
      "text-valign": "center"
    }
  },
  {
    selector: "edge",
    style: {
      "curve-style": "bezier",
      "target-arrow-shape": "triangle",
      "line-style": 'straight',
      'width': 1.5
    }
  },
  {
    selector: "edge[label]",
    style: {
      label: "data(label)",
      "font-size": "12",

      "text-background-color": "white",
      "text-background-opacity": 1,
      "text-background-padding": "2px",

      "text-border-color": "black",
      "text-border-style": "solid",
      "text-border-width": 0.5,
      "text-border-opacity": 1

      // "text-rotation": "autorotate"
    }
  }
]

class Graphbox extends React.Component {
    constructor(props) {
      
        super(props);
        this.state = { graph: "graph" };
    }
    render() {
        return (
            <div className="graphBoxRight">
            {this.graph != "null" &&
              <CytoscapeComponent className="cyto" cy={(cy) => {
                cy.on("select", (_x) => {
                  console.log("something was selected here");
                });
              }} elements={CytoscapeComponent.normalizeElements(this.graph)} layout={{
                name: "dagre",
                // other options
                padding: 10,
                idealEdgeLength: 10,
                edgeElasticity: 0.1
  
              }}
              stylesheet={cytoscapeStylesheet} />
            }
          </div>
        );
    }
}

export default Graphbox;


