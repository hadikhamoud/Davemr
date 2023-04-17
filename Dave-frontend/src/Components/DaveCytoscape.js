import React, { useEffect } from 'react';
import { layoutdagre } from '../cytostyle';
import { cytoscapeStylesheet } from '../cytostyle';
import CytoscapeComponent from 'react-cytoscapejs';

export default function DaveCytoscape({
    cytoElements,
    cytoReference

}) {
    function CytoEvent(cytoRef) {
        console.log("SCREEAMMING");
        var AllNodes = cytoRef.current.nodes();
        if (AllNodes.length >= 3) {
          for (var nId = 3; nId < AllNodes.length; nId = nId + 3) {
            var RankedNodes = cytoRef.current.nodes("[rank='" + nId + "']");
            var order = nId / 3
            RankedNodes.successors().addClass("collapsedchild" + order)
            RankedNodes.addClass('expandable');
          }
        }
    
        var Expandable = function (ele) {
          if (ele.hasClass('expandable')) {
            ele.on('tap', function (evt) {
              var collapsed = ele.data('rank');
              ele.successors().toggleClass("collapsedchild" + collapsed / 3);
            })
          }
        }
        cytoRef.current.nodes().forEach(Expandable)
  
      }
    function CytoStartEvent(cytoRef) {
        console.log("CALLLEEDDDDDD")
        cytoRef.current.animate({
          fit: {
            eles: cytoRef.current.nodes("[rank='2']"),
            padding: 20
          }
        },
          {
            duration: 350
          });
      }
    console.log(cytoElements);
    const cytoScapeElements = [...cytoElements];
    
    useEffect(() => {
        if (cytoReference.current) {

            const layout = cytoReference.current.layout(layoutdagre);
            layout.run();
            // CytoEvent(cytoReference);

            // CytoStartEvent(cytoReference);
            console.log("crying");
            var AllNodes = cytoReference.current.nodes();
            if (AllNodes.length >= 3) {
              for (var nId = 3; nId < AllNodes.length; nId = nId + 3) {
                var RankedNodes = cytoReference.current.nodes("[rank='" + nId + "']");
                var order = nId / 3
                RankedNodes.successors().addClass("collapsedchild" + order)
                RankedNodes.addClass('expandable');
              }
            }
        
            const expandable = (ele) => {
              if (ele.hasClass('expandable')) {
                const onTapExpandable = (evt) => {
                  const collapsed = ele.data('rank');
                  ele.successors().toggleClass(`collapsedchild${collapsed / 3}`);
                };
        
                ele.on('tap', onTapExpandable);
        
                // Store the onTapExpandable function to remove it later
                ele._onTapExpandable = onTapExpandable;
              }
            };
        
            cytoReference.current.nodes().forEach(expandable);
        return () => {
    
          // Remove 'tap' event listeners for expandable nodes
          cytoReference.current.nodes('.expandable').forEach((ele) => {
            ele.removeListener('tap', ele._onTapExpandable);
          });
        };
      }
    }, [cytoElements]);

    // useEffect(() => {
    //     if (cytoReference.current){
    //         CytoStartEvent(cytoReference);
    //     }

    // }, []);

    useEffect(() => {
        if (cytoReference.current) {
            cytoReference.current.on('tap', 'node', function (evt) {
                const node = evt.target;

                cytoReference.current.animation({
                    center: {
                        eles: node,
                    },
                    zoom: 1.5,
                    duration: 350,
                }).play();
            });
        }

        return () => {
            if (cytoReference.current) {
                // Remove the 'tap' event listener when the component is unmounted
                cytoReference.current.off('tap', 'node');
            }
        }
    }, [cytoReference]);
    
    return (
        <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
        autoungrabify={true} userPanningEnabled={true} className="cyto"
        cy={ref => cytoReference.current = ref}
        elements={cytoScapeElements} layout={layoutdagre}
        stylesheet={cytoscapeStylesheet} />
    );
  }
