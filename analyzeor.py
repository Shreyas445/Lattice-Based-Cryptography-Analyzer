import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide", page_title="N-Dim Lattice Crypto", page_icon="🌌")

# --- Mathematical Core: N-Dimensional Generation ---
@st.cache_data
def generate_unimodular_matrix(n):
    """Generates a matrix with determinant 1 or -1 to scramble the basis."""
    # Multiply a random lower triangular matrix and upper triangular matrix 
    # (both with 1s on the diagonal) to guarantee a determinant of 1.
    L = np.tril(np.random.randint(-3, 4, size=(n, n)), -1) + np.eye(n)
    U = np.triu(np.random.randint(-3, 4, size=(n, n)), 1) + np.eye(n)
    return np.matmul(L, U).astype(int)

@st.cache_data
def generate_keys(n):
    """Generates the Private (Good) and Public (Bad) basis matrices."""
    # Private Key: Strongly diagonally dominant (nice, orthogonal-ish boxes)
    # The larger the dimension, the larger the diagonal needs to be to tolerate noise.
    diag_strength = 20 * n
    R = (np.eye(n) * diag_strength) + np.random.randint(-5, 6, size=(n, n))
    
    # Scrambler
    U = generate_unimodular_matrix(n)
    
    # Public Key: The scrambled, highly skewed basis
    B = np.matmul(R, U)
    return R, U, B

# --- String Processing for N-Dimensions ---
def text_to_n_chunks(text, n):
    """Converts text to ASCII and pads it to fit into N-dimensional vectors."""
    ascii_vals = [ord(c) for c in text]
    while len(ascii_vals) % n != 0:
        ascii_vals.append(32)  # Pad with space character
    return [np.array(ascii_vals[i:i+n]) for i in range(0, len(ascii_vals), n)]

def n_chunks_to_text(chunks):
    """Converts N-dimensional vectors back to a string."""
    chars = []
    for chunk in chunks:
        for val in chunk:
            chars.append(chr(int(np.clip(val, 0, 255)))) # Ensure valid ASCII
    return "".join(chars)

# --- UI Setup ---
st.title("🌌 N-Dimensional Lattice Cryptography")
st.markdown("Scale the math from a simple 2D grid up to a complex 100-dimensional lattice structure.")

# Sidebar Settings
with st.sidebar:
    st.header("⚙️ Cryptosystem Parameters")
    N = st.slider("Lattice Dimensions (N)", min_value=2, max_value=100, value=3, step=1, 
                  help="2D and 3D will render spatial graphs. 4D+ will render Matrix Heatmaps.")
    noise_level = st.slider("Noise Injection Level", min_value=1.0, max_value=15.0, value=5.0, step=0.5)
    
    # Regenerate keys if N changes
    R, U, B = generate_keys(N)
    
    st.markdown("---")
    st.success(f"Keys generated for {N}D space.")

# Main Interface Tabs
tab_crypto, tab_visuals = st.tabs(["🔒 Encryption Pipeline", "📊 Mathematical Visualizer"])

# --- TAB 1: ENCRYPTION PIPELINE ---
with tab_crypto:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Input & Encrypt")
        message = st.text_area("Enter your secret message:", "Lattice crypto is quantum resistant!")
        
        if st.button("Encrypt Message", type="primary", use_container_width=True):
            with st.status(f"Processing in {N}D Space...", expanded=True) as status:
                st.write(f"1. Chunking text into {N}-dimensional vectors...")
                m_chunks = text_to_n_chunks(message, N)
                
                st.write("2. Multiplying by Public Key (Bad Basis)...")
                st.write("3. Injecting random noise into empty space...")
                
                encrypted_chunks = []
                for m in m_chunks:
                    lattice_point = np.matmul(B, m)
                    noise = np.random.uniform(-noise_level, noise_level, N)
                    c = lattice_point + noise
                    encrypted_chunks.append(c)
                    time.sleep(0.05)
                
                st.session_state.enc_data = encrypted_chunks
                status.update(label="Encryption Complete", state="complete", expanded=False)
            
            st.success("Message Encrypted!")
            with st.expander("View Raw Ciphertext"):
                st.json([list(np.round(c, 2)) for c in encrypted_chunks])

    with col2:
        st.subheader("2. Decrypt & Recover")
        if st.button("Decrypt with Private Key", use_container_width=True):
            if 'enc_data' not in st.session_state:
                st.warning("Please encrypt a message first.")
            else:
                with st.status("Solving Closest Vector Problem...", expanded=True) as status:
                    st.write("1. Applying inverse of Private Key (Good Map)...")
                    R_inv = np.linalg.inv(R)
                    U_inv = np.linalg.inv(U)
                    
                    st.write("2. Rounding coordinates to strip noise...")
                    decrypted_chunks = []
                    for c in st.session_state.enc_data:
                        x = np.matmul(R_inv, c)
                        y = np.round(x) # The magic step that removes the noise
                        m_recovered = np.matmul(U_inv, y).astype(int)
                        decrypted_chunks.append(m_recovered)
                        time.sleep(0.05)
                        
                    recovered_text = n_chunks_to_text(decrypted_chunks)
                    status.update(label="Decryption Complete", state="complete", expanded=False)
                    
                st.success(f"**Recovered String:** {recovered_text}")

# --- TAB 2: ADAPTIVE VISUALIZER ---
with tab_visuals:
    st.subheader(f"Visualizing {N}-Dimensional Data")
    
    if N == 2:
        st.info("Displaying 2D Spatial Grid")
        fig = go.Figure()
        # Draw basis vectors
        fig.add_trace(go.Scatter(x=[0, B[0,0]], y=[0, B[1,0]], mode='lines+text', line=dict(color='red', width=3), name='Public Vector 1'))
        fig.add_trace(go.Scatter(x=[0, B[0,1]], y=[0, B[1,1]], mode='lines+text', line=dict(color='red', width=3), name='Public Vector 2'))
        fig.add_trace(go.Scatter(x=[0, R[0,0]], y=[0, R[1,0]], mode='lines+text', line=dict(color='green', width=3), name='Private Vector 1'))
        fig.add_trace(go.Scatter(x=[0, R[0,1]], y=[0, R[1,1]], mode='lines+text', line=dict(color='green', width=3), name='Private Vector 2'))
        fig.update_layout(height=600, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif N == 3:
        st.info("Displaying 3D Spatial Grid")
        fig = go.Figure()
        # Draw 3D basis vectors
        for i in range(3):
            fig.add_trace(go.Scatter3d(x=[0, B[0,i]], y=[0, B[1,i]], z=[0, B[2,i]], mode='lines', line=dict(color='red', width=5), name=f'Public Vector {i+1}'))
            fig.add_trace(go.Scatter3d(x=[0, R[0,i]], y=[0, R[1,i]], z=[0, R[2,i]], mode='lines', line=dict(color='green', width=5), name=f'Private Vector {i+1}'))
        fig.update_layout(height=700, template="plotly_dark", scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(f"Dimensions ({N}) exceed spatial rendering capability. Switching to Cryptographic Matrix Heatmaps.")
        st.markdown("In high dimensions, we visualize the **structure** of the keys. The Private Key has a strong diagonal structure (easy to solve). The Public Key looks like random noise (hard to solve).")
        
        col_heat1, col_heat2 = st.columns(2)
        with col_heat1:
            st.markdown("**Private Key Matrix (R) - Structured & Solvable**")
            fig1 = go.Figure(data=go.Heatmap(z=R, colorscale='Viridis'))
            fig1.update_layout(height=500, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col_heat2:
            st.markdown("**Public Key Matrix (B) - Chaotic & Skewed**")
            # We use log scale or clip it because the values in B get astronomically large in high dimensions
            B_clipped = np.clip(B, -np.max(R)*5, np.max(R)*5) 
            fig2 = go.Figure(data=go.Heatmap(z=B_clipped, colorscale='Inferno'))
            fig2.update_layout(height=500, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)