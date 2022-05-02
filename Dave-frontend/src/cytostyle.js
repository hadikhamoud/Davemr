

export const layoutdagre = {
    name: "dagre",
    // other options
    padding: 5,
    idealEdgeLength: 10,
    edgeElasticity: 0.1,
    nodeDimensionsIncludeLabels: true,
    spacingFactor: 1,
    fit: true,
    rankDir: "TB",
    // animate: true,
    // animationDuration: 1000,
    ranker: 'network-simplex',
    animateFilter: function (node, i) { return true; },
  
  };

export const layoutYesNo = {
    name: 'dagre',
    // other options
    edgeWeight: function( edge ){ return 500; },
  
  };
  
export const cytoscapeStylesheet = [
  
    {
  
  
      selector: "node",
      style: {
        "background-color": "#F5F5DC",
        width: "label",
        height: "label",
        padding: "20px",
        shape: "round-rectangle",
        'text-wrap': 'wrap',
        label: 'My multiline\nlabel',
        "shadow-blur":"30px",
  
      }
    },
  
    {
      selector: "node[label]",
      style: {
        label: "data(label)",
        "font-size": "12",
        color: "black",
        "text-halign": "center",
        "text-valign": "center",
        "box-shadow": "10px 5px 5px red",
        "font-family": 'Gill Sans'



      }
    },
    {
      selector: "edge",
      style: {
        "curve-style": "taxi",
        "taxi-direction": "auto",
  
        "target-arrow-shape": "triangle",
        "line-style": 'straight',
        'width': 2
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
  
    },
    {
      selector: "node[type='YES/NO']",
      style: {
        "font-size": "12",
        "text-background-color": "white",

  
        // "text-rotation": "autorotate"
      }
  
    },
    {
      selector: "node[prefcolor]",
      css: {
        'background-color':'data(prefcolor)'
  
      },
    },
    {
      selector: "node[prefshape]",
      css: {
        width: "label",
        height: "label",
        padding: "20px",
        shape: 'data(prefshape)',
  
      },
    },
    {
      selector: ".expandable",
      css: {
        "background-color":"#ffb6c1",
        shape:"octagon",
        "border-color": "red",
        
  
      },
    },
    {
      selector: ".TopNodeGiven",
      css: {
        "background-color":"#ADD8E6",
        shape:"octagon",
        "border-color": "red",
        
  
      },
    },
  
    {
      selector: ".collapsedchild1",
      css: {
        'display': "none",
  
      },
    },
    {
      selector: ".collapsedchild2",
      css: {
        'display': "none",
  
      },
    },
    {
      selector: ".collapsedchild3",
      css: {
        'display': "none",
  
      },
    },
    {
      selector: ".collapsedchild4",
      css: {
        'display': "none",
  
      },
    },
    {
      selector: ".hide",
      css: {
        'display': "none",
  
      },
    }
  
  
  ];


  