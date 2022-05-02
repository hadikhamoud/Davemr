import { useState, useEffect } from "react";
import React from "react";
import './App.css';
import CytoscapeComponent from 'react-cytoscapejs';
import cytoscape from 'cytoscape';
import dagre from 'cytoscape-dagre';
import { useRef } from "react";
import CloseIcon from '@mui/icons-material/Close';
import {
  Button, Typography, AppBar, Toolbar, createTheme, ThemeProvider, FormGroup, Stack, Switch,
  Card, CardActionArea, CardMedia, CardContent, Slide, Dialog, IconButton
} from "@mui/material";
import img from "./symptomToDiagnosis.jpg";
import img1 from "./patientHistory.jpg";
import svgDave from "./DAVE-3.svg";
import svgText from "./DAVE-2.svg";
import svgFig from "./DAVE-1.svg";
import ColorButton from "./styledButtons";
import SideButton from "./sideButtonStyle";
import GraphButton from "./graphButtonStyle";
import UserCredentialsDialog from "./UserCredentialsDialog";
import StyledSwitch from "./StyledSwitch";
import StickyNote2OutlinedIcon from '@mui/icons-material/StickyNote2Outlined';
import LooksOneOutlinedIcon from '@mui/icons-material/LooksOneOutlined';
import LooksTwoOutlinedIcon from '@mui/icons-material/LooksTwoOutlined';
import Looks3OutlinedIcon from '@mui/icons-material/Looks3Outlined';
import Looks4OutlinedIcon from '@mui/icons-material/Looks4Outlined';
import Looks5OutlinedIcon from '@mui/icons-material/Looks5Outlined';
import Looks6OutlinedIcon from '@mui/icons-material/Looks6Outlined';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import ImageOutlinedIcon from '@mui/icons-material/ImageOutlined';
import MedicationIcon from '@mui/icons-material/Medication';
// import ChromeReaderModeTwoToneIcon from '@mui/icons-material/ChromeReaderModeTwoTone';
import MenuBookRoundedIcon from '@mui/icons-material/MenuBookRounded';
import { saveAs } from 'file-saver'
import ToPNG from './topng';

import {layoutdagre} from './cytostyle';
import {cytoscapeStylesheet} from './cytostyle';
import {layoutYesNo} from './cytostyle';
// import {defaults} from './cytostyle';
import coseBilkent from 'cytoscape-cose-bilkent';
import contextMenus from 'cytoscape-context-menus';
import 'cytoscape-context-menus/cytoscape-context-menus.css';
// import popper from 'cytoscape-popper';
// import tippy from 'tippy.js';
// import 'tippy.js/dist/tippy.css';
// import nodeHtmlLabel from "cytoscape-node-html-label";
// cytoscape.use( popper );
cytoscape.use(contextMenus);
cytoscape.use(dagre);
// nodeHtmlLabel(cytoscape);

var SERVER_URL = "https://davemr.herokuapp.com/"


function App() {
  let [start, setStart] = useState(true);
  let [icon, setIcon] = useState(false);
  let [Notes, setNotes] = useState("");
  let [showText, setShowText] = useState(true);
  let [more, setMore] = useState(false);
  let [openPNG, setOpenPNG] = useState(false)
  let [book, setBook] = useState("hideChooseBook");
  let [bookChoice,setBookChoice] = useState("Book3");
  let [showGraph1, setShowGraph1] = useState(false);
  let [showGraph2, setShowGraph2] = useState(false);
  let [showGraph3, setShowGraph3] = useState(false);
  let [showGraph4, setShowGraph4] = useState(false);
  let [showGraph5, setShowGraph5] = useState(false);
  let [showGraph6, setShowGraph6] = useState(false);
  let [graph1Name, setGraph1Name] = useState("");
  let [graph2Name, setGraph2Name] = useState("");
  let [graph3Name, setGraph3Name] = useState("");
  let [graph4Name, setGraph4Name] = useState("");
  let [graph5Name, setGraph5Name] = useState("");
  let [graph6Name, setGraph6Name] = useState("");
  let [graph1Score, setGraph1Score] = useState("");
  let [graph2Score, setGraph2Score] = useState("");
  let [graph3Score, setGraph3Score] = useState("");
  let [graph4Score, setGraph4Score] = useState("");
  let [graph5Score, setGraph5Score] = useState("");
  let [graph6Score, setGraph6Score] = useState("");
  let [graph1, setGraph1] = useState("null");
  let [graph2, setGraph2] = useState("null");
  let [graph3, setGraph3] = useState("null");
  let [graph4, setGraph4] = useState("null");
  let [graph5, setGraph5] = useState("null");
  let [graph6, setGraph6] = useState("null");
  let [pop, setPop] = useState(true);
  let [datar, setDatar] = useState("null");
  let [datarRest, setDatarRest] = useState("null");
  let [counter, setCounter] = useState(1);
  const [disableVisNow, setDisable] = React.useState(false);
  const [show, setShow] = useState(false);
  let [graph, setGraph] = useState("1");
  const cytoRef = useRef(null);
  const ContextMenuRef = useRef(null)
  let [TopNodeTemp, setTopNodeTemp] = useState(2);
  let TopNodesTemp;



  const interval = setInterval(function () {
    setStart(false);
  }, 2000);
  

  if (typeof cytoscape('core',contextMenus) === null) {
    console.log("it is null")
    contextMenus(cytoscape);
  }

  


  const defaults = {

    evtType: 'cxttap',
    menuItems: [
      {
        id: "Accept",
        content: "Accept",
        image: {src: "./Accept.png", width: 12, height: 12, x: 6, y: 10},
        selector: "node[TopNode='1']",
        onClickFunction: function (event) {
          console.log(event.target.data().id)
        },
        hasTrailingDivider: false
      },
      {
        id: "Reject",
        content: "Reject",
        image: {src: "./Reject.png", width: 12, height: 12, x: 6, y: 10},
        selector: "node[TopNode='1']",
        onClickFunction: function (event) {
          console.log("inside Reject " + TopNodeTemp);
          event.target.removeClass("TopNodeGiven");
          event.target.data("TopNode","0");
          rejectNode();

        },
        hasTrailingDivider: false
      }
    ],
    menuItemClasses: ["custom-menu-item", "custom-menu-item:hover"],
    contextMenuClasses: ["custom-context-menu"]
};

function HandleContextMenu(){
  if (cytoRef.current && counter!==3) {
    if(ContextMenuRef.current===null){
      ContextMenuRef.current = cytoRef.current.contextMenus(defaults)
    }
    else{
      ContextMenuRef.current = null
      ContextMenuRef.current = cytoRef.current.contextMenus(defaults)
    }
   }
}


async function rejectNode() {
    const response = await fetch(`${SERVER_URL}/RejectNode`, {

      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    // var TopNode = cytoRef.current.getElementById("A"+TopNodeTemp)
    // console.log("inside reject Node " + TopNode.data('id'))
    // TopNode.removeClass("TopNodeGiven")
    // TopNode.data("TopNode","0")
    const TopNodeReceived = await response.json();
    setTopNodeTemp(TopNodeReceived.topNode[1]);
    var countholder = counter + 1
    setCounter(countholder)

}
  

  function displayGraph1() {
    setShowGraph1(false);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("1");

    // CytoEvent();

  }
  function displayGraph2() {
    setShowGraph1(true);
    setShowGraph2(false);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("2");
    // CytoEvent();
  }
  function displayGraph3() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(false);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("3");

    // CytoEvent();
  }
  function displayGraph4() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(false);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("4");
    // CytoEvent();
  }
  function displayGraph5() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(false);
    setShowGraph6(true);
    setGraph("5");
    // CytoEvent();
  }
  function displayGraph6() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(false);
    setGraph("6");
    // CytoEvent();
  }

  function ResetNames() {
    setGraph1Name("");
    setGraph2Name("");
    setGraph3Name("");
    setGraph4Name("");
    setGraph5Name("");
    setGraph6Name("");

  }
  

  function GetGraphName() {
    if (showGraph1 == false)
      return graph1Name
    if (showGraph2 == false)
      return graph2Name
    if (showGraph3 == false)
      return graph3Name
    if (showGraph4 == false)
      return graph4Name
    if (showGraph5 == false)
      return graph5Name
    if (showGraph6 == false)
      return graph6Name
  }


  useEffect(() => {
    if (cytoRef.current) {
      let cytoContainer = document.getElementsByClassName("__________cytoscape_container")[0];
      cytoContainer.children[0].classList.add("cyto-graph-container-dimensions");
      cytoRef.current.resize();
      // cytoRef.current.container.classList.add("cyto-container-dimensions");
    }

  }, [showText])

  useEffect(() => {
    console.log('count' + counter)
    if (counter === 3) {
      if (ContextMenuRef.current){
        ContextMenuRef.current.destroy()
      }
    
    }

  }, [counter])

  useEffect(() => {
    if (cytoRef.current) {
      CytoEvent();
      CytoStartEvent()
      HandleContextMenu();
      
    }

  }, [graph])

  useEffect(() => {
    if (cytoRef.current) {
      CytoTopNodeEvent();
    }

  }, [TopNodeTemp])



  function checkKeyChanged(e) {
    if (!disableVisNow)
      if (e.code === 'Space' || e.code === 'Enter') {
        console.log(Notes);
        postData(`${SERVER_URL}/Addnote`, { text: Notes })
        if(more){
          postDataRest(`${SERVER_URL}/RestOfNotes`);

        }



      }
  }

  function getRestGraphs() {
    postDataRest(`${SERVER_URL}/RestOfNotes`);
  }
  function CytoStartEvent(){
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

  function visualizeNow() {
    console.log(Notes);
    postData(`${SERVER_URL}/AddnoteNow`, { text: Notes });
  }

  // function makeTippy(el){
  //   var ref = el.popperRef();
  //   var dummyDomEle = document.createElement('div');

  //   var tip = tippy( dummyDomEle, {
  //     getReferenceClientRect: ref.getBoundingClientRect,
  //     trigger: 'manual', 
  //     content: function(){
  //       var div = document.createElement('div');

  //       div.innerHTML = "right Click to Accept of Reject";

  //       return div;
  //     },
  //     arrow: true,
  //     placement: 'top',
  //     hideOnClick: false,
  //     sticky: "reference",
  //     interactive: true,
  //     followCursor: true,
  //     appendTo: document.body
  //   } );

  //   return tip;
  // };

  function CytoTopNodeEvent(){

    var TopNode = cytoRef.current.getElementById("A"+TopNodeTemp)
    TopNode.addClass('TopNodeGiven');
    cytoRef.current.getElementById("A"+TopNodeTemp).data("TopNode","1")
    console.log("Inside CytoEventTopNode "+"[id='A"+TopNodeTemp+"']")
    TopNode.predecessors().forEach(function(ele){
      if(ele.hasClass('expandable')){
        ele.successors().toggleClass('collapsedchild'+ele.data('rank')/3);
      }
    })
  

    if(!cytoRef.current.destroyed()){
      cytoRef.current.animate({
        fit: {
          eles: TopNode,
          padding: 20
        }
      },
        {
          duration: 350
        });
      }
  }
  

  function CytoEvent() {
      // cytoRef.current.removeListener('cxttap');
      // cytoRef.current.contextMenus(defaults);
    // cytoRef.current.removeListener("click",Animate);
    // cytoRef.current.removeListener("click",Expandable);

    // cytoRef.current.nodes(topNode).style('background-color', '#00ffff');
    // var myNode1 = cytoRef.current.nodes('[id="A3"]')[0];
    // var myNode2 = cytoRef.current.nodes('[id="A7"]')[0];
    // var level3Nodes = cytoRef.current.nodes('[type="3"]');
    // myNode1.style('background-color', '#ffb6c1');
    // myNode2.style('background-color', '#ffb6c1');
    // var TopNode = cytoRef.current.getElementById('A1');
    // var Tippy = makeTippy(TopNode)
    // Tippy.show()
    var AllNodes = cytoRef.current.nodes();
    // cytoRef.current.animate({
    //   fit: {
    //     eles: cytoRef.current.nodes("[rank='2']"),
    //     padding: 20
    //   }
    // },
    //   {



    //     duration: 350
    //   });
    if (AllNodes.length>=3){
    for(var nId=3; nId<AllNodes.length; nId=nId+3){
      var RankedNodes = cytoRef.current.nodes("[rank='"+nId+"']");
      var order = nId/3
      RankedNodes.successors().addClass("collapsedchild"+order)
      RankedNodes.addClass('expandable');
    }
  }
  // cytoRef.current.nodeHtmlLabel([
  //   {
  //     query: "node",
  //     // cssClass: "cyNode",
  //     valign: "center",
  //     // halign: "left",
  //     valignBox: "center",
  //     // halignBox: "left",
  //     tpl: (data) => {
  //       return `<div class="cyNode">
  //                <div class="goggleBtn">+</div>
  //               </div>
  //               `;
  //     },
  //   },
  // ]);
  var Expandable = function(ele){
    if(ele.hasClass('expandable')){
      ele.on('tap', function (evt) {
        var collapsed = ele.data('rank');
        ele.successors().toggleClass("collapsedchild"+collapsed/3);
        })
    }


}
  cytoRef.current.nodes().forEach(Expandable)
    
    // myNode1.successors().addClass('collapsedchild');
    // myNode2.successors().addClass('collapsedchild');
    // cytoRef.current.zoomingEnabled(true);

  var Animate = function (evt) {
      var targetNode = cytoRef.current.nodes("[id = '" + evt.target.data().id + "']");
      cytoRef.current.animate({
        fit: {
          eles: targetNode,
          padding: 20
        }
      },
        {


          duration: 350
        });
    }
    cytoRef.current.on('click', 'node', Animate);



    // });
    // myNode2.on('tap', function (evt) {
    //   myNode2.successors().toggleClass("collapsedchild");
    // });
    // cytoRef.current.on('click', 'node', function (evt) {
    //   var targetNode = cytoRef.current.nodes("[id = '" + evt.target.data().id + "']");
    // })
  }


  function FromEPIC() {
    fetch(`${SERVER_URL}/getnoteepic`)
      .then(response => response.json())
      .then(data => {
        console.log(data)

      });
  }

  function resetData() {
    if (cytoRef.current){
      cytoRef.current.destroy()
    }
    // setGraph("1");
    setGraph1("null");
    setGraph2("null");
    setGraph3("null");
    setGraph4("null");
    setGraph5("null");
    setGraph6("null");
    setShowGraph1(false);
    setShowGraph2(false);
    setShowGraph3(false);
    setShowGraph4(false);
    setShowGraph5(false);
    setShowGraph6(false);
    setGraph1Score("");
    setGraph2Score("");
    setGraph3Score("");
    setGraph4Score("");
    setGraph5Score("");
    setGraph6Score("");
    
    setShowText(true);
    setNotes("");
    ResetNames();
    setMore(false);
    reset(`${SERVER_URL}/reset`);
      

    console.log("reset")
  }

  function changeBook(bookselected) {
    console.log(bookselected);
    postBook(`${SERVER_URL}/ChangeBook`, { Book: bookselected });
    setBook("hideChooseBook");
    setBookChoice("Book" + bookselected);
    resetData();
  }

  async function postBook(url = '', data = {}) {
    const response = await fetch(url, {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    // const datar = await response.json();
    // setBook(datar.Book);
  }

  async function reset(url = '') {
    const response = await fetch(url, {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      // body: JSON.stringify("RESET")
    })
  }

  async function postData(url = '', data = {}) {
    const response = await fetch(url, {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

    const datarTemp = await response.json();
    setDatar(datarTemp);
    if (datarTemp.elementss !== "Stall") {
      if (datarTemp.Name !== graph1Name) {
        setGraph1Name(datarTemp.Name);
        setGraph2Name(datarTemp.Name1);
        setGraph3Name(datarTemp.Name2);
        setShowGraph2(true);
        setShowGraph3(true);
        setGraph1("null");
        setGraph2("null");
        setGraph3("null");
        console.log("inside first postData TopNodeTemp Before "+TopNodeTemp)
        
        
        console.log("inside first postData TopNodeTemp After "+TopNodeTemp)
        console.log("inside first postData Received"+datarTemp.topNode[1])
        setGraph1(datarTemp.elementss);
        setGraph2(datarTemp.elementss1);
        setGraph3(datarTemp.elementss2);

        setGraph1Score(datarTemp.Score);
        setGraph2Score(datarTemp.Score1);
        setGraph3Score(datarTemp.Score2);
        setGraph("1");

        
      if (graph!=='1' &&  graph!=='2' && graph!=='3')
          setGraph("1");
      else
          setGraph(graph)
      
        console.log("A"+TopNodeTemp)
        console.log(cytoRef.current.getElementById("A"+TopNodeTemp).data("TopNode"))
        cytoRef.current.getElementById("A"+TopNodeTemp).data("TopNode","1")
        console.log(cytoRef.current.getElementById("A"+TopNodeTemp).data("TopNode"))
        setTopNodeTemp(datarTemp.topNode[1])
        HandleContextMenu();
        CytoEvent();

      }
    }
  }

  async function postDataRest(url = '') {
    const response = await fetch(url, {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      // body: JSON.stringify(data)
    })

    const datarTemp = await response.json();
    setDatarRest(datarTemp);
    if (datarTemp.elementss !== "Stall") {
      setGraph4Name(datarTemp.Name);
      if (datarTemp.Name !== graph4Name) {
        setGraph5Name(datarTemp.Name1);
        setGraph6Name(datarTemp.Name2);
        setShowGraph4(true);
        setShowGraph5(true);
        setShowGraph6(true);
        setGraph4("null");
        setGraph5("null");
        setGraph6("null");
        setGraph4(datarTemp.elementss);
        setGraph5(datarTemp.elementss1);
        setGraph6(datarTemp.elementss2);
        setGraph4Score(datarTemp.Score);
        setGraph5Score(datarTemp.Score1);
        setGraph6Score(datarTemp.Score2);
      }
    }
  }
  const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
  });

  return (
    <div className="App">
    {start &&
      <div className="animation">
        <img className="img-animation" src={svgDave}></img>
      </div>
    }
    {!start &&
      <div className="App">
        <AppBar position="static">
          <Toolbar classes={{ root: "nav" }}>
            <div>
              <Button className="btn-class epic" variant="outlined" onClick={FromEPIC} ></Button>&nbsp;&nbsp;
              <Button className="btn-class book" variant="outlined" onClick={() => setBook("showChooseBook")} > <MenuBookRoundedIcon sx={{ fontSize: 30 }}></MenuBookRoundedIcon></Button>
            </div>
            <div>
            {/* <img className="img-title" src={svgDave}></img> */}
            <img className="img-title" src={svgFig}></img>
            <img className="img-text" src={svgText}></img>  
            </div>
            <div>
              <div>
                <Button className="btn-class" variant="outlined" onClick={() => cytoRef.current.reset()}>Reset Zoom</Button>
                &nbsp;&nbsp;<Button className="btn-class" variant="outlined" onClick={resetData} >Clear</Button>
              </div>
            </div>
          </Toolbar>
        </AppBar>
        <UserCredentialsDialog open={book === "showChooseBook"} onSubmit={(bookselected) => changeBook(bookselected)}
          onClose={() => setBook("hideChooseBook")}
          title={'Choose Book'} submitText={'submit'}></UserCredentialsDialog>
        {openPNG &&
          <Dialog
            fullScreen
            open={openPNG}
            onClose={() => setOpenPNG(false)}
            TransitionComponent={Transition}
          >
            <AppBar sx={{ position: 'relative' }}>
              <Toolbar classes={{ root: "nav-png" }}>
                <IconButton
                  edge="start"
                  color="inherit"
                  onClick={() => setOpenPNG(false)}
                  aria-label="close"
                >
                  <CloseIcon />
                </IconButton>
                <Button autoFocus variant="outlined" color="inherit" onClick={() => saveAs("./PNGs/" + bookChoice + "/" + GetGraphName() + '.png', GetGraphName() + '.png')}>
                  Save
                </Button>
              </Toolbar>
            </AppBar>
            <div className="to-png-pop-up">
              <img src={require("../public/PNGs/" + bookChoice + "/" + GetGraphName() + '.png')} />
            </div>
          </Dialog>
        }
        <div className="graphBox">
          {showText &&
            <div className="graphBoxLeft">
              <div className="wrapper">
                <div className="graphBox-wrapper__clinical-notes__header">
                  <Typography variant="h5">Write your notes here</Typography>
                </div>
                <textarea id="clincalNotesTextField" name="clincalNotesTextField" rows="15" cols="100"
                  value={Notes} onChange={e => setNotes(e.target.value)} onKeyPress={(e) => checkKeyChanged(e)}>
                </textarea>
                <div className="graphBox-wrapper__clinical-notes__action-fields">
                  <FormGroup>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <Switch style={{ color: '#c4a35a' }} defaultChecked onChange={() => setDisable(!disableVisNow)} inputProps={{ 'aria-label': 'ant design' }} />
                      <Typography>Visualize Continuously</Typography>
                    </Stack>
                  </FormGroup>
                  <ColorButton disabled={!disableVisNow} variant="contained" onClick={visualizeNow}>Visualize</ColorButton>
                </div>
              </div>
            </div>
          }
          <div className="graphBoxRight">
            <div className="graph-box-right__open-note-button-container">
              <SideButton className="graph-box-right__open-note-button" variant="contained" onClick={() => setShowText(!showText)}>
                <StickyNote2OutlinedIcon></StickyNote2OutlinedIcon>
              </SideButton>
              <div className="graph-box-right__button-container">
                <GraphButton className={`base-class ${showGraph1 ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`}
                  disabled={!showGraph1} variant="contained" onClick={() => displayGraph1()}>
                  <LooksOneOutlinedIcon></LooksOneOutlinedIcon>
                </GraphButton>
                <label className={`base-class ${!showGraph1 ? 'graph-box-right__button-container__label' : 'graph-box-right__button-container__label--disabled'}`}
                >{graph1Name} {graph1Score && ": "+graph1Score}</label>
              </div>
              <div className="graph-box-right__button-container">
                <GraphButton className={`base-class ${showGraph2 ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`}
                  disabled={!showGraph2} variant="contained" onClick={() => { displayGraph2() }}>
                  <LooksTwoOutlinedIcon></LooksTwoOutlinedIcon>
                </GraphButton>
                <label className={`base-class ${!showGraph2 ? 'graph-box-right__button-container__label' : 'graph-box-right__button-container__label--disabled'}`}
                >{graph2Name} {graph2Score && ": "+graph2Score}</label>
              </div>
              <div className="graph-box-right__button-container">
                <GraphButton className={`base-class ${showGraph3 ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`} disabled={!showGraph3} variant="contained" onClick={() => displayGraph3()}>
                  <Looks3OutlinedIcon></Looks3OutlinedIcon>
                </GraphButton>
                <label className={`base-class ${!showGraph3 ? 'graph-box-right__button-container__label' : 'graph-box-right__button-container__label--disabled'}`}
                >{graph3Name} {graph3Score && ": "+graph3Score}</label>
              </div>
              {more &&
                <div>
                  <div className="graph-box-right__button-container">
                    <GraphButton className={`base-class ${showGraph4 ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`} disabled={!showGraph4} variant="contained" onClick={() => displayGraph4()}>
                      <Looks4OutlinedIcon></Looks4OutlinedIcon>
                    </GraphButton>
                    <label className={`base-class ${!showGraph4 ? 'graph-box-right__button-container__label' : 'graph-box-right__button-container__label--disabled'}`}
                    >{graph4Name} {graph4Score && ": "+graph4Score}</label>
                  </div>
                  <div className="graph-box-right__button-container">
                    <GraphButton className={`base-class ${showGraph5 ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`} disabled={!showGraph5} variant="contained" onClick={() => displayGraph5()}>
                      <Looks5OutlinedIcon></Looks5OutlinedIcon>
                    </GraphButton>
                    <label className={`base-class ${!showGraph5 ? 'graph-box-right__button-container__label' : 'graph-box-right__button-container__label--disabled'}`}
                    >{graph5Name} {graph5Score && ": "+graph5Score}</label>
                  </div>
                  <div className="graph-box-right__button-container">
                    <GraphButton className={`base-class ${showGraph6 ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`} disabled={!showGraph6} variant="contained" onClick={() => displayGraph6()}>
                      <Looks6OutlinedIcon></Looks6OutlinedIcon>
                    </GraphButton>
                    <label className={`base-class ${!showGraph6 ? 'graph-box-right__button-container__label' : 'graph-box-right__button-container__label--disabled'}`}
                    >{graph6Name} {graph6Score && ": "+graph6Score}</label>
                  </div>

                </div>

              }
              <GraphButton className={`base-class ${graph1 != "null" ? 'graph-box-right__graph-buttons' : 'graph-box-right__graph-buttons--disabled'}`}
                disabled={graph1 === "null"} variant="contained" onClick={() => { setMore(!more); getRestGraphs() }}>
                {!more &&
                  <MoreHorizIcon></MoreHorizIcon>
                }
                {more &&
                  <KeyboardArrowUpIcon></KeyboardArrowUpIcon>
                }
              </GraphButton>
            </div>
            <div className="graph-box-right__to-png-container">
              <GraphButton className={`base-class ${graph1 != "null" ? 'graph-box-right__to-png-buttons' : 'graph-box-right__to-png-buttons--disabled'}`}
                disabled={graph1 === "null"} variant="contained" onClick={() => setOpenPNG(!openPNG)}>
                <ImageOutlinedIcon></ImageOutlinedIcon>
              </GraphButton>
            </div>
            <div className="legend-flex">

              <ul className=" legend">
                <li className="legend-rhombus"> Top Node </li>
                <li className="legend-square-exp-collapse">Expandable </li>
                <li className="legend-square-consideration"> Test </li>
                <li className="legend-square-red">Consideration </li>
                <li className="legend-square-orange"> Diagnosis </li>
              </ul>
            </div>

            {graph === "1" && graph1 != "null"
              &&
              <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
                autoungrabify={true} userPanningEnabled={true} className="cyto"
                cy={ref => cytoRef.current = ref}
                elements={CytoscapeComponent.normalizeElements(graph1)} layout={layoutdagre}
                stylesheet={cytoscapeStylesheet} />
            }
            {graph === "2" && graph2 != "null"
              &&
              <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
                autoungrabify={true} userPanningEnabled={true} className="cyto"
                cy={ref => cytoRef.current = ref}
                elements={CytoscapeComponent.normalizeElements(graph2)} layout={layoutdagre}
                stylesheet={cytoscapeStylesheet} />
            }
            {graph === "3" && graph3 != "null"
              &&
              <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
                autoungrabify={true} userPanningEnabled={true} className="cyto"
                cy={ref => cytoRef.current = ref}
                elements={CytoscapeComponent.normalizeElements(graph3)} layout={layoutdagre}
                stylesheet={cytoscapeStylesheet} />
            }
            {graph === "4" && graph4 != "null"
              &&
              <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
                autoungrabify={true} userPanningEnabled={true} className="cyto"
                cy={ref => cytoRef.current = ref}
                elements={CytoscapeComponent.normalizeElements(graph4)} layout={layoutdagre}
                stylesheet={cytoscapeStylesheet} />
            }
            {graph === "5" && graph5 != "null"
              &&
              <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
                autoungrabify={true} userPanningEnabled={true} className="cyto"
                cy={ref => cytoRef.current = ref}
                elements={CytoscapeComponent.normalizeElements(graph5)} layout={layoutdagre}
                stylesheet={cytoscapeStylesheet} />
            }
            {graph === "6" && graph6 != "null"
              &&
              <CytoscapeComponent minZoom={0.5} maxZoom={1.5}
                autoungrabify={true} userPanningEnabled={true} className="cyto"
                cy={ref => cytoRef.current = ref}
                elements={CytoscapeComponent.normalizeElements(graph6)} layout={layoutdagre}
                stylesheet={cytoscapeStylesheet} />
            }
          </div>
        </div>
      </div>
    }
  </div>


);


}

export default App;