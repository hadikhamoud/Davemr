import React, { useEffect, useRef } from "react";
import { layoutdagre } from "../cytostyle";
import { cytoscapeStylesheet } from "../cytostyle";
import CytoscapeComponent from "react-cytoscapejs";

export default function DaveCytoscape({ cytoElements, clearGraph, setClearGraph, setGraph }) {
  const cytoScapeElements = [...cytoElements];
  const cytoReference = useRef(null);


  useEffect(() => {
    if (cytoReference.current){
      if (clearGraph) {
        cytoReference.current.destroy();
        setGraph(null);
        setClearGraph(null);
      }

    }


  }, [clearGraph]);


  useEffect(() => {
    if (cytoReference.current) {
      // Initialize the graph layout
      const layout = cytoReference.current.layout(layoutdagre);
      layout.run();

      // Center the second node when the graph is first mounted
      layout.promiseOn("layoutstop").then(() => {
        const secondNode = cytoReference.current.nodes()[1];
        if (secondNode) {
          cytoReference.current.animate({
            fit: {
              eles: secondNode,
              padding: 20,
            },
            duration: 1000,
          });
        }
      });

      // Center the clicked node
      const centerNode = (evt) => {
        cytoReference.current.animate({
          fit: {
            eles: evt.target,
            padding: 20,
          },
          duration: 350,
        });
      };

      // Collapse or expand nodes
      const toggleNodes = (evt) => {
        const ele = evt.target;
        const collapsed = ele.data("rank");
        ele.successors().toggleClass(`collapsedchild${collapsed / 3}`);
      };

      // Process nodes and hide/show them
      const processNodes = () => {
        const allNodes = cytoReference.current.nodes();

        for (let nId = 3; nId < allNodes.length; nId += 3) {
          const rankedNodes = cytoReference.current.nodes(`[rank='${nId}']`);
          const order = nId / 3;
          rankedNodes.successors().addClass(`collapsedchild${order}`);
          rankedNodes.addClass("expandable");
        }

        cytoReference.current.nodes(".expandable").on("tap", toggleNodes);
      };

      processNodes();

      // Assign event listeners
      cytoReference.current.on("tap", "node", centerNode);

      // Clean up event listeners on unmount
      return () => {
        cytoReference.current.removeListener("tap", "node", centerNode);
        cytoReference.current
          .nodes(".expandable")
          .removeListener("tap", toggleNodes);
      };
    }
  }, [cytoReference]);

  return (
    <CytoscapeComponent
      minZoom={0.5}
      maxZoom={1.5}
      autoungrabify={true}
      userPanningEnabled={true}
      className="cyto"
      cy={(ref) => (cytoReference.current = ref)}
      elements={cytoScapeElements}
      layout={layoutdagre}
      stylesheet={cytoscapeStylesheet}
    />
  );
}
