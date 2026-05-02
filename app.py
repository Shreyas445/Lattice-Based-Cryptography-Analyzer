import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# --- Configuration & UI Styling ---
st.set_page_config(layout="wide", page_title="N-Dim Lattice Crypto UI", page_icon="🌌", initial_sidebar_state="expanded")

# --- Hardened Mathematical Core ---
@st.cache_data
def generate_unimodular_matrix(n):
    """Generates a matrix with determinant 1 to scramble the basis without breaking integers."""
    L = np.tril(np.random.randint(-2, 3, size=(n, n)), -1) + np.eye(n)
    U = np.triu(np.random.randint(-2, 3, size=(n, n)), 1) + np.eye(n)
    return np.matmul(L, U).astype(float)

@st.cache_data
def generate_keys(n):
    """Generates the Cryptographic Keys with massive noise tolerance."""
    # Private Key (R): Massive diagonal matrix to easily absorb floating point noise
    diag_strength = 1000 * n 
    R = (np.eye(n) * diag_strength) + np.random.randint(-10, 11, size=(n, n))
    
    # Scrambler (U)
    U = generate_unimodular_matrix(n)
    
    # Public Key (B) = R * U (Ensures noise is handled correctly during decryption)
    B = np.matmul(R, U)
    
    # Pre-compute inverses for speed
    R_inv = np.linalg.inv(R)
    U_inv = np.linalg.inv(U)
    
    return R, U, B, R_inv, U_inv

# --- String Processing ---
def text_to_n_chunks(text, n):
    ascii_vals = [ord(c) for c in text]
    while len(ascii_vals) % n != 0:
        ascii_vals.append(32)  # Pad with space character
    return [np.array(ascii_vals[i:i+n]) for i in range(0, len(ascii_vals), n)]

def n_chunks_to_text(chunks):
    chars = []
    for chunk in chunks:
        for val in chunk:
            # Clip to valid ASCII range to prevent rendering crashes
            valid_ascii = int(np.clip(val, 32, 126)) 
            chars.append(chr(valid_ascii))
    return "".join(chars).strip()

# --- UI Setup ---
st.title("🌌 N-Dimensional Lattice Cryptography")
st.markdown("Watch the math happen in real-time. This visualizer demonstrates how lattice encryption protects data in high-dimensional space.")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ System Parameters")
    N = st.slider("Lattice Dimensions (N)", min_value=2, max_value=50, value=3, step=1)
    noise_level = st.slider("Noise Injection Level", min_value=1.0, max_value=50.0, value=15.0, step=1.0)
    
    R, U, B, R_inv, U_inv = generate_keys(N)
    st.success(f"Keys locked for {N}D space.")

# Session State
if 'encrypted_chunks' not in st.session_state:
    st.session_state.encrypted_chunks = None
if 'original_chunks' not in st.session_state:
    st.session_state.original_chunks = None

# Layout
col_enc, col_dec = st.columns(2, gap="large")

# --- ENCRYPTION PIPELINE ---
with col_enc:
    st.subheader("🔒 1. Encryption Engine")
    message = st.text_area("Secret Message:", "Lattice crypto is quantum resistant!")
    
    if st.button("Encrypt Message", type="primary", use_container_width=True):
        st.session_state.original_chunks = text_to_n_chunks(message, N)
        st.session_state.encrypted_chunks = []
        
        # UI Elements for Animation
        progress_bar = st.progress(0)
        status_text = st.empty()
        visual_console = st.empty()
        
        total_chunks = len(st.session_state.original_chunks)
        
        for i, m in enumerate(st.session_state.original_chunks):
            # Math
            lattice_point = np.matmul(B, m)
            noise = np.random.uniform(-noise_level, noise_level, N)
            c = lattice_point + noise
            st.session_state.encrypted_chunks.append(c)
            
            # Animation UI Update
            progress_bar.progress((i + 1) / total_chunks)
            status_text.markdown(f"**Encrypting block {i+1} of {total_chunks}...**")
            
            with visual_console.container():
                st.code(f"""
Block {i+1} ASCII Vector : {m}
Applying Public Key    : c = B * m
Injecting {noise_level}x Noise : + e
-----------------------------------
Ciphertext Output      : 
{np.round(c, 1)}
                """, language="text")
            time.sleep(0.15) # Control animation speed
            
        status_text.success("✅ Encryption Complete!")
        progress_bar.empty()

    # Show Final Encrypted State
    if st.session_state.encrypted_chunks is not None:
        with st.expander("View Full Ciphertext Payload", expanded=True):
            st.json([list(np.round(c, 2)) for c in st.session_state.encrypted_chunks])


# --- DECRYPTION PIPELINE ---
with col_dec:
    st.subheader("🔓 2. Decryption Engine")
    
    if st.button("Decrypt with Private Key", use_container_width=True):
        if st.session_state.encrypted_chunks is None:
            st.error("Please encrypt a message first.")
        else:
            decrypted_chunks = []
            
            # UI Elements for Animation
            progress_bar_dec = st.progress(0)
            status_text_dec = st.empty()
            visual_console_dec = st.empty()
            
            total_chunks = len(st.session_state.encrypted_chunks)
            
            for i, c in enumerate(st.session_state.encrypted_chunks):
                # Math Core
                # 1. Multiply by R_inv and round immediately to kill noise
                x = np.round(np.matmul(R_inv, c))
                # 2. Multiply by U_inv and round again to handle floating point drift
                m_recovered = np.round(np.matmul(U_inv, x)).astype(int)
                decrypted_chunks.append(m_recovered)
                
                # Animation UI Update
                progress_bar_dec.progress((i + 1) / total_chunks)
                status_text_dec.markdown(f"**Decrypting block {i+1} of {total_chunks}...**")
                
                with visual_console_dec.container():
                    st.code(f"""
Ciphertext Block {i+1}    : 
{np.round(c, 1)}
1. Apply Private Key  : x = R_inv * c
2. Snap to Grid       : round(x)
3. Reverse Scrambler  : U_inv * x
-----------------------------------
Recovered ASCII       : {m_recovered}
                """, language="text")
                time.sleep(0.15) # Control animation speed
            
            recovered_text = n_chunks_to_text(decrypted_chunks)
            
            status_text_dec.success("✅ Decryption Complete!")
            progress_bar_dec.empty()
            
            st.success(f"**Decrypted Message:**\n\n### {recovered_text}")

# --- TAB 2: MATHEMATICAL VISUALIZER ---
st.markdown("---")
st.subheader(f"📊 Cryptographic Heatmaps ({N}D)")
st.markdown("While the math happens above, here is what the keys actually look like. The **Private Key** has a strong structure (easy to solve), while the **Public Key** looks completely chaotic.")

col_heat1, col_heat2 = st.columns(2)
with col_heat1:
    fig1 = go.Figure(data=go.Heatmap(z=R, colorscale='Viridis'))
    fig1.update_layout(title="Private Key (R) - Structured", height=400, template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)
    
with col_heat2:
    # Clip B so the heatmap isn't washed out by massive outliers
    B_clipped = np.clip(B, -np.max(R)*2, np.max(R)*2) 
    fig2 = go.Figure(data=go.Heatmap(z=B_clipped, colorscale='Inferno'))
    fig2.update_layout(title="Public Key (B) - Chaotic", height=400, template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)