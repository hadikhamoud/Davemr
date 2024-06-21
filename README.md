## Differential Analysis Visualizer for EMRs

### https://www.davemr.com

A clinical note analysis application that relates input clinical notes entered by medical practitioners, to text book clinical diagnostic algorithms using Natural language processing and machine learning.

<br></br>


![DAVE-3](https://user-images.githubusercontent.com/69105312/169825851-a1e20a1d-f05e-4c0b-b8f3-62235f6ddfeb.svg)


## Resources

#### Graphs are extracted from:
1-The Patient History: evidence-based Approach: ISBN 978-0-07-162494-7

2-Symptoms to Diagnosis: An Evidence Based Guide: ISBN 978-1-260-12111-7
[]()

---

- Graph Visualization is done using
[Cytoscape.js] (https://js.cytoscape.org)

- Clinical Notes extracted from American University of Beirut Medical Center and Rafic al Hariri Hospital Lebanon
- Distributional Similarity using DISCO linguatools
[DISCO] (https://www.linguatools.de/disco/)

<br></br>


## **Installation**

1- clone current repository

2- install requirements.txt folder

```python
pip install -r requirements.txt
```

3- Within client environment, install node modules
  ```javascript
  npm install
  ```


4 - Run client
```javascript
npm start
```

5- Run server
```python
python app.py
```
