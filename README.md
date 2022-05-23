
# **DAVE**
<img src="https://user-images.githubusercontent.com/69105312/169825851-a1e20a1d-f05e-4c0b-b8f3-62235f6ddfeb.svg" alt="drawing" width="300"/>

## Differential Analysis Visualizer for EMRs

### https://www.davemr.com

Medical support tool that aims to improve clinical decision making through diagnostic algorithms visualization.

<br></br>




## Resources

#### Graphs are extracted from:
1-The Patient History: evidence-based Approach: ISBN 978-0-07-162494-7 

2-Symptoms to Diagnosis: An Evidence Based Guide: ISBN 978-1-260-12111-7


#### Graph Visualization is done using [Cytoscape.js] (https://js.cytoscape.org)

#### Clinical Notes extracted from American University of Beirut Medical Center and Rafic al Hariri Hospital Lebanon

#### Distributional Similarity using DISCO linguatools [DISCO] (https://www.linguatools.de/disco/)

<br></br>


## **Installation**

1- clone current repository

2- install requirements.txt folder

```python
pip install -r requirements.txt
```
3-remove Talisman, uncomment CORS, and install flask_cors for development environment

```python
pip install flask_cors
```

4-use localhost for var SERVER_URL in frontend

```javascript
var SERVER_URL = "0.0.0.0:5000"
```










