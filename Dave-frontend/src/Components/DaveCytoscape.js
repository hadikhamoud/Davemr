import React, { useEffect } from 'react';
import { layoutdagre } from '../cytostyle';
import { cytoscapeStylesheet } from '../cytostyle';
import CytoscapeComponent from 'react-cytoscapejs';

export default function DaveCytoscape({
    cytoElements,
    cytoReference

}) {
    console.log(cytoElements);
    const cytoScapeElements = [...cytoElements];
    
    useEffect(() => {
        // This function will be called when the component is mounted or when cytoElements changes
        const cytoInstance = cytoReference.current;
        
        // Cleanup function: destroy the previous instance if it exists
        return () => {
            if (cytoInstance) {
                cytoInstance.destroy();
            }
        };
    }, [cytoElements, cytoReference]);
    return (
        <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
        autoungrabify={true} userPanningEnabled={true} className="cyto"
        cy={ref => cytoReference.current = ref}
        elements={cytoScapeElements} layout={layoutdagre}
        stylesheet={cytoscapeStylesheet} />
    );
  }
