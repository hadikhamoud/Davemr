## Differential Analysis Visualizer for EMRs

### https://www.davemr.com

A clinical note analysis application that relates input clinical notes entered by medical practitioners, to text book clinical diagnostic algorithms using Natural language processing and machine learning.

<br></br>


![DAVE-3](https://user-images.githubusercontent.com/69105312/169825851-a1e20a1d-f05e-4c0b-b8f3-62235f6ddfeb.svg)


## Resources

#### Graphs are extracted from:
1-The Patient History: evidence-based Approach: ISBN 978-0-07-162494-7

2-Symptoms to Diagnosis: An Evidence Based Guide: ISBN 978-1-260-12111-7


---

- Graph Visualization is done using
[Cytoscape.js] (https://js.cytoscape.org)

- Clinical Notes extracted from American University of Beirut Medical Center and Rafic al Hariri Hospital Lebanon
- Distributional Similarity using DISCO linguatools
[DISCO] (https://www.linguatools.de/disco/)

<br></br>


## **Installation**

1- Clone current repository.

2- Install Python dependencies with uv.

```bash
uv sync
```

3- Install frontend dependencies with pnpm.

```bash
pnpm --dir client install
```

4- Build the frontend (served by Flask from `client/build`).

```bash
pnpm --dir client build
```

5- Run server.

```bash
uv run gunicorn --chdir server app:app --bind 0.0.0.0:5000
```

## **Coolify Deployment (single service)**

This repo now deploys as one service (no docker-compose):

- Coolify should use the root `Dockerfile`.
- The container builds the React client with Node.js 23 + pnpm.
- The runtime uses Python + uv and serves the built client via Flask/Gunicorn.
- No `docker-compose.yml` is required.
