import { useState, useEffect } from "react";
import React from "react";
import "./style/App.css";
import CytoscapeComponent from "react-cytoscapejs";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import { useRef } from "react";
import CloseIcon from "@mui/icons-material/Close";
import {
  Button,
  Typography,
  AppBar,
  Toolbar,
  FormGroup,
  Stack,
  Switch,
  Slide,
  Dialog,
  IconButton,
} from "@mui/material";
import svgDave from "./assets/DAVE-3.svg";
import svgText from "./assets/DAVE-2.svg";
import svgFig from "./assets/DAVE-1.svg";
import ColorButton from "./components/styledButtons";
import UserCredentialsDialog from "./components/Dialog";
import StickyNote2OutlinedIcon from "@mui/icons-material/StickyNote2Outlined";
import LooksOneOutlinedIcon from "@mui/icons-material/LooksOneOutlined";
import LooksTwoOutlinedIcon from "@mui/icons-material/LooksTwoOutlined";
import Looks3OutlinedIcon from "@mui/icons-material/Looks3Outlined";
import Looks4OutlinedIcon from "@mui/icons-material/Looks4Outlined";
import Looks5OutlinedIcon from "@mui/icons-material/Looks5Outlined";
import Looks6OutlinedIcon from "@mui/icons-material/Looks6Outlined";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import ImageOutlinedIcon from "@mui/icons-material/ImageOutlined";
import MenuBookRoundedIcon from "@mui/icons-material/MenuBookRounded";
import { saveAs } from "file-saver";

import { layoutdagre } from "./style/cytostyle";
import { cytoscapeStylesheet } from "./style/cytostyle";
import contextMenus from "cytoscape-context-menus";
import "cytoscape-context-menus/cytoscape-context-menus.css";
import DaveCytoscape from "./components/DaveCytoscape";
cytoscape.use(contextMenus);
cytoscape.use(dagre);

// var SERVER_URL = "http://127.0.0.1:5000/";
// var SERVER_URL = "https://www.davemr.com/"

function App() {
  let [start, setStart] = useState(true);
  let [icon, setIcon] = useState(false);
  let [Notes, setNotes] = useState("");
  let [showText, setShowText] = useState(true);
  let [legend, setLegend] = useState(false);
  let [more, setMore] = useState(false);
  let [openPNG, setOpenPNG] = useState(false);
  let [book, setBook] = useState("hideChooseBook");
  let [bookChoice, setBookChoice] = useState("Book3");
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
  let [finalData, setfinalData] = useState(null);
  let [datarRest, setDatarRest] = useState("null");
  let [counter, setCounter] = useState(1);
  const [disableVisNow, setDisable] = React.useState(false);
  const [show, setShow] = useState(false);
  let [graph, setGraph] = useState("1");
  const cytoRef = useRef(null);
  const ContextMenuRef = useRef(null);
  let [TopNodeTemp, setTopNodeTemp] = useState(2);
  const [finalDataUpdateCounter, setfinalDataUpdateCounter] = useState(0);
  const [clearGraph, setClearGraph] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      setStart(false);
    }, 1000);

    return () => {
      clearTimeout(timer);
    };
  }, []);

  function displayGraph1() {
    setShowGraph1(false);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("1");
  }

  function displayGraph2() {
    setShowGraph1(true);
    setShowGraph2(false);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("2");
  }

  function displayGraph3() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(false);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("3");
  }

  function displayGraph4() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(false);
    setShowGraph5(true);
    setShowGraph6(true);
    setGraph("4");
  }

  function displayGraph5() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(false);
    setShowGraph6(true);
    setGraph("5");
  }

  function displayGraph6() {
    setShowGraph1(true);
    setShowGraph2(true);
    setShowGraph3(true);
    setShowGraph4(true);
    setShowGraph5(true);
    setShowGraph6(false);
    setGraph("6");
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
    if (showGraph1 == false) return graph1Name;
    if (showGraph2 == false) return graph2Name;
    if (showGraph3 == false) return graph3Name;
    if (showGraph4 == false) return graph4Name;
    if (showGraph5 == false) return graph5Name;
    if (showGraph6 == false) return graph6Name;
  }

  useEffect(() => {
    if (
      cytoRef.current &&
      (showGraph1 ||
        showGraph2 ||
        showGraph3 ||
        showGraph4 ||
        showGraph5 ||
        showGraph6)
    ) {
      let cytoContainer = document.getElementsByClassName(
        "__________cytoscape_container"
      )[0];
      cytoContainer.children[0].classList.add(
        "cyto-graph-container-dimensions"
      );
      cytoRef.current.resize();
    }
  }, [showText]);

  function checkKeyChanged(e) {
    if (!disableVisNow)
      if (e.code === "Space" || e.code === "Enter") {
        postData(`/Addnote`, { text: Notes });
        if (more) {
          postDataRest(`/RestOfNotes`);
        }
      }
  }

  function getRestGraphs() {
    postDataRest(`/RestOfNotes`);
  }

  function visualizeNow() {
    postData(`/Addnote`, { text: Notes });
  }

  function CytoTopNodeEvent() {
    var TopNode = cytoRef.current.getElementById("A" + TopNodeTemp);
    TopNode.addClass("TopNodeGiven");
    cytoRef.current.getElementById("A" + TopNodeTemp).data("TopNode", "1");
    // console.log("Inside CytoEventTopNode " + "[id='A" + TopNodeTemp + "']")
    TopNode.predecessors().forEach(function (ele) {
      if (ele.hasClass("expandable")) {
        ele.successors().toggleClass("collapsedchild" + ele.data("rank") / 3);
      }
    });

    if (!cytoRef.current.destroyed()) {
      cytoRef.current.animate(
        {
          fit: {
            eles: TopNode,
            padding: 20,
          },
        },
        {
          duration: 350,
        }
      );
    }
  }

  function FromEPIC() {
    fetch(`/getnoteepic`)
      .then((response) => response.json())
      .then((data) => {});
  }

  function resetData() {
    if (cytoRef.current) {
      cytoRef.current.destroy();
    }
    setClearGraph(true);
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
    setLegend(false);
    setShowText(true);
    setNotes("");
    ResetNames();
    setMore(false);
    reset(`/reset`);
  }

  function changeBook(bookselected) {
    postBook(`/ChangeBook`, { Book: bookselected });
    setBook("hideChooseBook");
    setBookChoice("Book" + bookselected);
    resetData();
  }

  async function postBook(url = "", data = {}) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
  }

  async function reset(url = "") {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  async function postData(url = "", data = {}) {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const datarTemp = await response.json();
    setDatar(datarTemp);
    if (!datarTemp.Stall) {
      if (datarTemp.NameG1 !== graph1Name) {
        setGraph1Name(datarTemp.NameG1);
        setGraph2Name(datarTemp.NameG2);
        setGraph3Name(datarTemp.NameG3);
        setShowGraph2(true);
        setShowGraph3(true);
        setGraph1("null");
        setGraph2("null");
        setGraph3("null");
        setGraph1(datarTemp.elementsG1);
        setGraph2(datarTemp.elementsG2);
        setGraph3(datarTemp.elementsG3);
        setGraph1Score(datarTemp.ScoreG1);
        setGraph2Score(datarTemp.ScoreG2);
        setGraph3Score(datarTemp.ScoreG3);
        setLegend(true);
        setGraph("1");
        setfinalData(datarTemp.elements);
        setfinalDataUpdateCounter((prevCounter) => prevCounter + 1);
        setShowGraph1(false);

        // if (graph !== "1" && graph !== "2" && graph !== "3") {
        //   setGraph("1");
        // } else {
        //   setGraph(graph);
        // }
      }
    }
  }

  async function postDataRest(url = "") {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const datarTemp = await response.json();
    setDatarRest(datarTemp);
    if (!datarTemp.Stall) {
      setGraph4Name(datarTemp.NameG4);
      if (datarTemp.NameG4 !== graph4Name) {
        setGraph5Name(datarTemp.NameG5);
        setGraph6Name(datarTemp.NameG6);
        setShowGraph4(true);
        setShowGraph5(true);
        setShowGraph6(true);
        setGraph4("null");
        setGraph5("null");
        setGraph6("null");
        setGraph4(datarTemp.elementsG4);
        setGraph5(datarTemp.elementsG5);
        setGraph6(datarTemp.elementsG6);
        setGraph4Score(datarTemp.ScoreG4);
        setGraph5Score(datarTemp.ScoreG5);
        setGraph6Score(datarTemp.ScoreG6);
        setfinalData([...finalData, ...datarTemp.elements]);
      }
    }
  }
  const Transition = React.forwardRef(function Transition(props, ref) {
    return <Slide direction="up" ref={ref} {...props} />;
  });

  return (
    <div className="App">
      {start && (
        <div className="animation">
          <img className="img-animation" src={svgDave}></img>
        </div>
      )}
      {!start && (
        <div className="App">
          <AppBar position="static">
            <Toolbar classes={{ root: "nav" }}>
              <div>
                <Button
                  className="btn-class epic"
                  variant="outlined"
                  onClick={FromEPIC}
                ></Button>
                &nbsp;&nbsp;
                <Button
                  className="btn-class book"
                  variant="outlined"
                  onClick={() => setBook("showChooseBook")}
                >
                  {" "}
                  <MenuBookRoundedIcon
                    sx={{ fontSize: 30 }}
                  ></MenuBookRoundedIcon>
                </Button>
              </div>
              <div>
                <img className="img-title" src={svgFig}></img>
                <img className="img-text" src={svgText}></img>
              </div>
              <div>
                <div>
                  {/* <Button className="btn-class" variant="outlined" onClick={() => cytoRef.current.reset()}>Reset Zoom</Button> */}
                  &nbsp;&nbsp;
                  <Button
                    className="btn-class"
                    variant="outlined"
                    onClick={resetData}
                  >
                    Clear
                  </Button>
                </div>
              </div>
            </Toolbar>
          </AppBar>
          <UserCredentialsDialog
            open={book === "showChooseBook"}
            onSubmit={(bookselected) => changeBook(bookselected)}
            onClose={() => setBook("hideChooseBook")}
            title={"Choose Book"}
            submitText={"submit"}
          ></UserCredentialsDialog>
          {openPNG && (
            <Dialog
              fullScreen
              open={openPNG}
              onClose={() => setOpenPNG(false)}
              TransitionComponent={Transition}
            >
              <AppBar sx={{ position: "relative" }}>
                <Toolbar classes={{ root: "nav-png" }}>
                  <IconButton
                    edge="start"
                    color="inherit"
                    onClick={() => setOpenPNG(false)}
                    aria-label="close"
                  >
                    <CloseIcon />
                  </IconButton>
                  <Button
                    autoFocus
                    variant="outlined"
                    color="inherit"
                    onClick={() =>
                      saveAs(
                        "./PNGs/" + bookChoice + "/" + GetGraphName() + ".png",
                        GetGraphName() + ".png"
                      )
                    }
                  >
                    Save
                  </Button>
                </Toolbar>
              </AppBar>
              <div className="to-png-pop-up">
                <img
                  src={require("../public/PNGs/" +
                    bookChoice +
                    "/" +
                    GetGraphName() +
                    ".png")}
                />
              </div>
            </Dialog>
          )}
          <div className="graphBox">
            {showText && (
              <div className="graphBoxLeft">
                <div className="wrapper">
                  <div className="graphBox-wrapper__clinical-notes__header">
                    <Typography variant="h5">Write your notes here</Typography>
                  </div>
                  <textarea
                    id="clincalNotesTextField"
                    name="clincalNotesTextField"
                    rows="15"
                    cols="100"
                    value={Notes}
                    onChange={(e) => setNotes(e.target.value)}
                    onKeyPress={(e) => checkKeyChanged(e)}
                  ></textarea>
                  <div className="graphBox-wrapper__clinical-notes__action-fields">
                    <FormGroup>
                      <Stack direction="row" spacing={1} alignItems="center">
                        <Switch
                          style={{ color: "#1E5288" }}
                          defaultChecked
                          onChange={() => setDisable(!disableVisNow)}
                          inputProps={{ "aria-label": "ant design" }}
                        />
                        <Typography>Visualize Continuously</Typography>
                      </Stack>
                    </FormGroup>
                    <ColorButton
                      className="visualize-btn"
                      disabled={!disableVisNow}
                      variant="contained"
                      onClick={visualizeNow}
                    >
                      Visualize
                    </ColorButton>
                  </div>
                </div>
              </div>
            )}
            <div className="graphBoxRight">
              <div className="graph-box-right__open-note-button-container">
                <Button
                  className="graph-box-right__open-note-button"
                  variant="contained"
                  onClick={() => setShowText(!showText)}
                >
                  <StickyNote2OutlinedIcon></StickyNote2OutlinedIcon>
                </Button>
                <div className="graph-box-right__button-container">
                  <Button
                    className={`base-class ${
                      showGraph1
                        ? "graph-box-right__graph-buttons"
                        : "graph-box-right__graph-buttons--disabled"
                    }`}
                    disabled={!showGraph1}
                    variant="contained"
                    onClick={() => displayGraph1()}
                  >
                    <LooksOneOutlinedIcon></LooksOneOutlinedIcon>
                  </Button>
                  <label
                    className={`base-class ${
                      !showGraph1
                        ? "graph-box-right__button-container__label"
                        : "graph-box-right__button-container__label--disabled"
                    }`}
                  >
                    {graph1Name} {graph1Score && ": " + graph1Score}
                  </label>
                </div>
                <div className="graph-box-right__button-container">
                  <Button
                    className={`base-class ${
                      showGraph2
                        ? "graph-box-right__graph-buttons"
                        : "graph-box-right__graph-buttons--disabled"
                    }`}
                    disabled={!showGraph2}
                    variant="contained"
                    onClick={() => {
                      displayGraph2();
                    }}
                  >
                    <LooksTwoOutlinedIcon></LooksTwoOutlinedIcon>
                  </Button>
                  <label
                    className={`base-class ${
                      !showGraph2
                        ? "graph-box-right__button-container__label"
                        : "graph-box-right__button-container__label--disabled"
                    }`}
                  >
                    {graph2Name} {graph2Score && ": " + graph2Score}
                  </label>
                </div>
                <div className="graph-box-right__button-container">
                  <Button
                    className={`base-class ${
                      showGraph3
                        ? "graph-box-right__graph-buttons"
                        : "graph-box-right__graph-buttons--disabled"
                    }`}
                    disabled={!showGraph3}
                    variant="contained"
                    onClick={() => displayGraph3()}
                  >
                    <Looks3OutlinedIcon></Looks3OutlinedIcon>
                  </Button>
                  <label
                    className={`base-class ${
                      !showGraph3
                        ? "graph-box-right__button-container__label"
                        : "graph-box-right__button-container__label--disabled"
                    }`}
                  >
                    {graph3Name} {graph3Score && ": " + graph3Score}
                  </label>
                </div>
                {more && (
                  <div>
                    <div className="graph-box-right__button-container">
                      <Button
                        className={`base-class ${
                          showGraph4
                            ? "graph-box-right__graph-buttons"
                            : "graph-box-right__graph-buttons--disabled"
                        }`}
                        disabled={!showGraph4}
                        variant="contained"
                        onClick={() => displayGraph4()}
                      >
                        <Looks4OutlinedIcon></Looks4OutlinedIcon>
                      </Button>
                      <label
                        className={`base-class ${
                          !showGraph4
                            ? "graph-box-right__button-container__label"
                            : "graph-box-right__button-container__label--disabled"
                        }`}
                      >
                        {graph4Name} {graph4Score && ": " + graph4Score}
                      </label>
                    </div>
                    <div className="graph-box-right__button-container">
                      <Button
                        className={`base-class ${
                          showGraph5
                            ? "graph-box-right__graph-buttons"
                            : "graph-box-right__graph-buttons--disabled"
                        }`}
                        disabled={!showGraph5}
                        variant="contained"
                        onClick={() => displayGraph5()}
                      >
                        <Looks5OutlinedIcon></Looks5OutlinedIcon>
                      </Button>
                      <label
                        className={`base-class ${
                          !showGraph5
                            ? "graph-box-right__button-container__label"
                            : "graph-box-right__button-container__label--disabled"
                        }`}
                      >
                        {graph5Name} {graph5Score && ": " + graph5Score}
                      </label>
                    </div>
                    <div className="graph-box-right__button-container">
                      <Button
                        className={`base-class ${
                          showGraph6
                            ? "graph-box-right__graph-buttons"
                            : "graph-box-right__graph-buttons--disabled"
                        }`}
                        disabled={!showGraph6}
                        variant="contained"
                        onClick={() => displayGraph6()}
                      >
                        <Looks6OutlinedIcon></Looks6OutlinedIcon>
                      </Button>
                      <label
                        className={`base-class ${
                          !showGraph6
                            ? "graph-box-right__button-container__label"
                            : "graph-box-right__button-container__label--disabled"
                        }`}
                      >
                        {graph6Name} {graph6Score && ": " + graph6Score}
                      </label>
                    </div>
                  </div>
                )}
                <Button
                  className={`base-class ${
                    graph1 != "null"
                      ? "graph-box-right__graph-buttons"
                      : "graph-box-right__graph-buttons--disabled"
                  }`}
                  disabled={graph1 === "null"}
                  variant="contained"
                  onClick={() => {
                    setMore(!more);
                    getRestGraphs();
                  }}
                >
                  {!more && <MoreHorizIcon></MoreHorizIcon>}
                  {more && <KeyboardArrowUpIcon></KeyboardArrowUpIcon>}
                </Button>
              </div>
              <div className="graph-box-right__to-png-container">
                <Button
                  className={`base-class ${
                    graph1 != "null"
                      ? "graph-box-right__to-png-buttons"
                      : "graph-box-right__to-png-buttons--disabled"
                  }`}
                  disabled={graph1 === "null"}
                  variant="contained"
                  onClick={() => setOpenPNG(!openPNG)}
                >
                  <ImageOutlinedIcon></ImageOutlinedIcon>
                </Button>
              </div>
              {legend && (
                <div className="legend-flex">
                  <ul className=" legend">
                    <li className="legend-rhombus"> Top Node </li>
                    <li className="legend-square-exp-collapse">Expandable </li>
                    <li className="legend-square-red">Consideration </li>
                    <li className="legend-square-orange"> Diagnosis </li>
                  </ul>
                </div>
              )}
              {graph && finalData && (
                <DaveCytoscape
                  cytoElements={CytoscapeComponent.normalizeElements(
                    finalData[parseInt(graph) - 1]
                  )}
                  cytoReference={cytoRef}
                  key={`cytoscape-graph-${graph}-${finalDataUpdateCounter}`}
                  clearGraph={clearGraph}
                  setClearGraph={setClearGraph}
                  setGraph={setGraph}
                ></DaveCytoscape>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
