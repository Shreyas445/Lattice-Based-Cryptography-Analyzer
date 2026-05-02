# 🌌 N-Dimensional Lattice Cryptography Visualizer

An interactive, real-time educational sandbox for understanding Post-Quantum Lattice-Based Cryptography. Built with Python, Streamlit, and Plotly.

This application visualizes the core mechanics of lattice encryption (specifically a hardened toy model of the GGH Cryptosystem). It bridges the gap between abstract mathematical theories and visual understanding, allowing users to scale cryptographic environments from easily comprehensible 2D/3D spatial grids up to complex 50-dimensional matrices.

## ✨ Features

* **Real-Time Spatial Animations (2D & 3D):** Watch the literal geometry of encryption. See your message map to a grid, watch noise push it into empty space (encryption), and observe the private key seamlessly snap it back to the nearest intersection (decryption).
* **High-Dimensional Scaling (4D to 50D+):** Automatically transitions from spatial rendering to Cryptographic Matrix Heatmaps when dimensions exceed human spatial comprehension.
* **Hardened Mathematical Core:** Built to handle high-dimensional floating-point drift. The app safely chunks strings into $N$-dimensional ASCII vectors and processes them through strict rounding gates to prevent data corruption.
* **Modern UI/UX:** Features a sleek dark-mode interface, step-by-step progress pipelines, and interactive camera controls.

---

## 🚀 Quick Start & Installation

### Prerequisites
Ensure you have Python 3.8 or higher installed on your machine. 

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/lattice-crypto-visualizer.git
cd lattice-crypto-visualizer
```

### 2. Install Dependencies
This project relies on three core libraries: Streamlit (for the UI), NumPy (for linear algebra), and Plotly (for animations).
```bash
pip install streamlit numpy plotly
```

### 3. Run the Application
```bash
streamlit run app.py
```
*The application will automatically open in your default web browser at `http://localhost:8501`.*

---

## 📖 How It Works: The Mathematics

Lattice-based cryptography relies on the **Closest Vector Problem (CVP)**—a mathematical puzzle that is currently considered secure against future quantum computers. 

The security hinges on a cryptographic "trapdoor" created by two different maps of the exact same grid:

1. **The Private Key (Good Basis):** A highly structured, nearly orthogonal matrix. It creates a neat grid of compact boxes, making it mathematically trivial to find the closest lattice intersection.
2. **The Public Key (Bad Basis):** A completely chaotic, highly skewed matrix that generates the *exact same grid*. To an attacker, the space looks like unnavigable, razor-thin slivers.

<img width="665" height="256" alt="image" src="https://github.com/user-attachments/assets/0c37ccff-a63f-430a-b64c-a2edbe6d1314" />
<br>
<img width="664" height="306" alt="image" src="https://github.com/user-attachments/assets/9550b39c-dc34-4165-8111-afd817bdde32" />


### The Pipeline
* **Encryption ($c = B \cdot m + e$):** The sender multiplies the message ($m$) by the Public Key ($B$) to find a lattice point, then injects random noise ($e$) to push the point off the grid into empty space. 
* **Decryption ($m = U^{-1} \cdot \lfloor R^{-1} \cdot c \rceil$):** An attacker with the bad map gets lost trying to find the original point. The receiver, holding the Private Key ($R$), applies their structured map. Because their grid is neat and wide, they simply round to the nearest integer, which strips away the noise and recovers the original message.
<img width="1407" height="351" alt="image" src="https://github.com/user-attachments/assets/6b5e3002-3da2-4330-a8ab-3ace52eb5653" />
<br>

### for 3 dimentional

<img width="847" height="570" alt="image" src="https://github.com/user-attachments/assets/9988eb59-4a95-4f7e-a51e-8412350b0e3c" />

### for 2d

<img width="1430" height="588" alt="image" src="https://github.com/user-attachments/assets/3ab081e0-1bd4-4c3e-96a0-86804c5c638f" />

---

## 🎮 Interface Guide

### Tab 1: Encryption Pipeline
* **Input:** Type any string message.
* **Process:** The app automatically chunks your text into arrays matching your chosen dimension, applies the Public Key, and injects noise. 
* **Output:** Displays the raw, encrypted float vectors (Ciphertext) and the step-by-step decryption recovery log.

### Tab 2: Spatial Animation (Visualizer)
* **2D & 3D Mode ($N \le 3$):** Renders the basis vectors and animated data points. Click "Animate Encryption" to watch the noise vector push the ciphertext off the grid, and "Animate Decryption" to watch the closest-vector snap.
* **Heatmap Mode ($N \ge 4$):** Visualizes the structural difference between the neatly organized Private Key ($R$) matrix and the scrambled, chaotic Public Key ($B$) matrix.

---

## 🛠️ Built With

* [Streamlit](https://streamlit.io/) - The web framework
* [NumPy](https://numpy.org/) - $N$-Dimensional matrix mathematics
* [Plotly](https://plotly.com/python/) - Interactive graphing and animation engine

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
