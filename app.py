import streamlit as st
from streamlit_option_menu import option_menu

import aes_cipher
import des_cipher
import hashing
import playfair
import rc4_cipher
import rsa_cipher
import vernam
import vigenere

# ==========================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==========================================
st.set_page_config(
    page_title="CryptoShield Premium",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for RSA Keys
if 'rsa_public' not in st.session_state:
    st.session_state.rsa_public = None
if 'rsa_private' not in st.session_state:
    st.session_state.rsa_private = None

# ==========================================
# 2. INJECT CSS STYLES & ANIMATIONS
# ==========================================
def inject_premium_ui():
    st.markdown("""
    <style>
        /* Hide Streamlit Default Header and Footer for SaaS Look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Modern Deep Gradient Background */
        .stApp {
            background: radial-gradient(circle at top right, #0F172A 0%, #020617 100%) !important;
            color: #E2E8F0;
        }
        
        /* Smooth Fade-in Animation for Main Content */
        [data-testid="stAppViewBlockContainer"] {
            animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(15px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Advanced Logo Styling with Neon Glow */
        .logo-container {
            text-align: center;
            padding: 25px 0 15px 0;
            position: relative;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .logo-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(6, 182, 212, 0.8);
            background: linear-gradient(to right, #ffffff, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .logo-subtitle {
            font-size: 0.75rem;
            font-weight: 700;
            color: #06B6D4;
            letter-spacing: 3px;
            text-transform: uppercase;
            background: rgba(6, 182, 212, 0.1);
            padding: 4px 12px;
            border-radius: 20px;
            display: inline-block;
            border: 1px solid rgba(6, 182, 212, 0.3);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(6, 182, 212, 0.15);
            border: 1px solid rgba(6, 182, 212, 0.3);
        }
        
        /* Metric Styling */
        .metric-title {
            font-size: 0.9rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #06B6D4, #3B82F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Streamlit inputs styling override to match theme */
        .stTextInput>div>div>input {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px;
        }
        .stTextInput>div>div>input:focus {
            border-color: #06B6D4 !important;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3) !important;
        }
        .stTextArea>div>div>textarea {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px;
        }
        .stTextArea>div>div>textarea:focus {
            border-color: #06B6D4 !important;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.3) !important;
        }
        .stSelectbox>div>div>div {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px;
        }
        
        /* Button Styling */
        .stButton>button {
            width: 100%;
            background: linear-gradient(90deg, #06B6D4, #3B82F6) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.5) !important;
            background: linear-gradient(90deg, #3B82F6, #06B6D4) !important;
        }
        
        /* Result Box styling */
        .result-box {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 8px;
            padding: 15px;
            color: #10B981;
            font-family: monospace;
            word-break: break-all;
            margin-top: 15px;
        }

        /* Animated Server Status Indicator */
        .server-status {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 15px;
            margin: 25px 0 15px 0;
            backdrop-filter: blur(10px);
        }
        .status-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 0.8rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #10B981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10B981;
            animation: pulse-green 2s infinite;
        }
        @keyframes pulse-green {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        .status-bar-bg {
            background: rgba(255, 255, 255, 0.1);
            height: 6px;
            border-radius: 3px;
            overflow: hidden;
        }
        .status-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #06B6D4, #8B5CF6);
            width: 98%;
            animation: load-bar 4s infinite alternate ease-in-out;
        }
        @keyframes load-bar {
            0% { width: 95%; }
            100% { width: 99%; }
        }
    </style>
    """, unsafe_allow_html=True)

inject_premium_ui()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <div class="logo-title">🛡️ CryptoShield</div>
            <div class="logo-subtitle">Premium Engine</div>
        </div>
    """, unsafe_allow_html=True)
    
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Symmetric Algorithms", "Asymmetric Algorithms", "Hashing"],
        icons=['house', 'shield-lock', 'key', 'hash'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#06B6D4", "font-size": "1.1rem"}, 
            "nav-link": {
                "font-size": "0.95rem", "text-align": "left", "margin": "4px 0", 
                "padding": "10px 15px", "color": "#94A3B8", "border-radius": "10px", 
                "transition": "all 0.3s ease", "font-weight": "500"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, rgba(6, 182, 212, 0.15) 0%, rgba(6, 182, 212, 0.05) 100%)", 
                "color": "#ffffff", "border-left": "4px solid #06B6D4", 
                "box-shadow": "inset 2px 0 10px rgba(6, 182, 212, 0.1)", "font-weight": "600"
            },
        }
    )
    
    st.markdown("<div style='flex-grow: 1; min-height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="server-status">
            <div class="status-header">
                <span>Crypto Engine</span>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 0.75rem; color: #10B981; font-weight: 700;">ONLINE</span>
                    <div class="status-dot"></div>
                </div>
            </div>
            <div class="status-bar-bg">
                <div class="status-bar-fill"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. PAGES
# ==========================================

if selected_page == "Home":
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: rgba(15, 23, 42, 0.4); border-radius: 16px; border: 1px solid rgba(6, 182, 212, 0.2); margin-bottom: 30px;">
        <h1 style="font-size: 3rem; font-weight: 800; color: white; margin-bottom: 10px;">Security Cryptography Algorithms</h1>
        <p style="font-size: 1.2rem; color: #94A3B8; max-width: 800px; margin: 0 auto; line-height: 1.6;">
            A modern platform for understanding and implementing cryptographic algorithms with real-world applications.
            Explore classical ciphers, modern symmetric/asymmetric encryption, and secure hashing functions seamlessly.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Technologies Section
    st.markdown("<h2 style='color: white; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;'>Core Technologies</h2>", unsafe_allow_html=True)
    
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    with t_col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🐍</div>
            <h3 style="color: white; margin-top: 0; font-size: 1.2rem;">Python</h3>
            <p style="color: #94A3B8; font-size: 0.85rem;">Core programming language for implementing algorithms securely and efficiently.</p>
        </div>
        """, unsafe_allow_html=True)
    with t_col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🚀</div>
            <h3 style="color: white; margin-top: 0; font-size: 1.2rem;">Streamlit</h3>
            <p style="color: #94A3B8; font-size: 0.85rem;">Frontend framework providing a beautiful, reactive, and pure-Python web interface.</p>
        </div>
        """, unsafe_allow_html=True)
    with t_col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">⚙️</div>
            <h3 style="color: white; margin-top: 0; font-size: 1.2rem;">Git</h3>
            <p style="color: #94A3B8; font-size: 0.85rem;">Version control system ensuring code integrity, tracking, and collaborative potential.</p>
        </div>
        """, unsafe_allow_html=True)
    with t_col4:
        st.markdown("""
        <div class="glass-card" style="text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">🐙</div>
            <h3 style="color: white; margin-top: 0; font-size: 1.2rem;">GitHub</h3>
            <p style="color: #94A3B8; font-size: 0.85rem;">Repository hosting service for open-source distribution and CI/CD pipelines.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # GitHub Integration Footer
    st.markdown("<h2 style='color: white; margin-top: 30px; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;'>Open Source & Contribution</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: white; margin-top:0;">Join the Development</h3>
        <p style="color: #94A3B8; line-height: 1.6;">
            This project is proudly open-source and hosted on GitHub. We welcome contributions, bug reports, and feature requests. To get started, clone the repository and follow the setup instructions in the README.
        </p>
        <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid rgba(255,255,255,0.05);">
            <code style="color: #06B6D4; font-family: monospace; font-size: 1.1rem;">git clone https://github.com/Mahmoudsherif00/Security-Project-.git</code>
        </div>
        <a href="https://github.com/Mahmoudsherif00/Security-Project-" target="_blank" style="text-decoration: none;">
            <button style="background: linear-gradient(90deg, #1f2937, #111827); color: white; border: 1px solid #374151; padding: 10px 24px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: all 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                ⭐ View Repository on GitHub
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

elif selected_page == "Symmetric Algorithms":
    st.markdown("<h1 style='color: white; margin-bottom: 20px;'>Symmetric Encryption Suite</h1>", unsafe_allow_html=True)
    
    col_alg, col_space = st.columns([1, 2])
    with col_alg:
        algo = st.selectbox("Select Cipher Algorithm", ["AES", "DES", "RC4", "Playfair", "Vernam", "Vigenere"])
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-top:0;'>Input Configuration</h3>", unsafe_allow_html=True)
        
        with st.form("symmetric_form"):
            mode = st.radio("Operation Mode", ["Encrypt", "Decrypt"], horizontal=True)
            text_input = st.text_area("Input Text (Plaintext or Ciphertext)", height=150)
            
            # Determine appropriate key input format
            key_help = ""
            if algo == "AES":
                key_help = "Key must be exactly 16, 24, or 32 characters long."
            elif algo == "DES":
                key_help = "Key must be exactly 8 characters long."
                
            key_input = st.text_input("Secret Key", type="password", help=key_help)
            process_btn = st.form_submit_button(f"Execute Operation")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_output:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-top:0;'>Execution Output</h3>", unsafe_allow_html=True)
        
        if process_btn:
            if not text_input or not key_input:
                st.error("Please provide both Input Text and Secret Key.")
            else:
                try:
                    result = ""
                    with st.spinner("Processing..."):
                        if algo == "AES":
                            if mode == "Encrypt":
                                result = aes_cipher.encrypt(text_input, key_input)
                            else:
                                result = aes_cipher.decrypt(text_input, key_input)
                                
                        elif algo == "DES":
                            if mode == "Encrypt":
                                result = des_cipher.encrypt(text_input, key_input)
                            else:
                                result = des_cipher.decrypt(text_input, key_input)
                                
                        elif algo == "RC4":
                            if mode == "Encrypt":
                                result = rc4_cipher.encrypt(text_input, key_input)
                            else:
                                result = rc4_cipher.decrypt(text_input, key_input)
                                
                        elif algo == "Playfair":
                            if mode == "Encrypt":
                                result = playfair.encrypt(text_input, key_input)
                            else:
                                result = playfair.decrypt(text_input, key_input)
                                
                        elif algo == "Vernam":
                            if len(key_input) < len(text_input) and mode == "Encrypt":
                                st.warning("Warning: Vernam key is typically as long as the plaintext. Repeating key.")
                                key_expanded = (key_input * ((len(text_input) // len(key_input)) + 1))[:len(text_input)]
                            else:
                                key_expanded = key_input
                            
                            if mode == "Encrypt":
                                result = vernam.encrypt(text_input, key_expanded)
                            else:
                                # For decrypt, we approximate the required key length from b64 string length, or just pass it
                                result = vernam.decrypt(text_input, key_input * 100) # Quick hack to ensure it's long enough
                                
                        elif algo == "Vigenere":
                            if mode == "Encrypt":
                                result = vigenere.encrypt(text_input, key_input)
                            else:
                                result = vigenere.decrypt(text_input, key_input)
                    
                    st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
                    st.success("Operation completed successfully!")
                except Exception as e:
                    st.error(f"Error during execution: {str(e)}")
        else:
            st.info("Awaiting execution. Output will appear here.")
            
        st.markdown("</div>", unsafe_allow_html=True)


elif selected_page == "Asymmetric Algorithms":
    st.markdown("<h1 style='color: white; margin-bottom: 20px;'>RSA Asymmetric Cryptography</h1>", unsafe_allow_html=True)
    
    # Key Generation Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; margin-top:0;'>Key Management</h3>", unsafe_allow_html=True)
    
    col_k1, col_k2, col_k3 = st.columns([1, 1, 2])
    with col_k1:
        key_size = st.selectbox("Key Size", [1024, 2048])
    with col_k2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate RSA Key Pair"):
            with st.spinner("Generating cryptographically secure primes..."):
                pub, priv = rsa_cipher.generate_keys(keysize=key_size)
                st.session_state.rsa_public = pub
                st.session_state.rsa_private = priv
            st.success("Key Pair Generated!")
            
    with col_k3:
        if st.session_state.rsa_public is not None:
            st.success("Keys are currently loaded in session memory.")
            st.markdown(f"<div style='font-size: 0.8rem; color: #94A3B8;'>Public Exponent (e): {st.session_state.rsa_public.e}</div>", unsafe_allow_html=True)
        else:
            st.warning("No keys loaded. Please generate a key pair.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Encryption/Decryption Section
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-top:0;'>Operation Configuration</h3>", unsafe_allow_html=True)
        
        with st.form("rsa_form"):
            mode = st.radio("RSA Operation", ["Encrypt (Requires Public Key)", "Decrypt (Requires Private Key)"], horizontal=False)
            text_input = st.text_area("Input Text", height=150)
            process_btn = st.form_submit_button(f"Execute RSA")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_output:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-top:0;'>Output</h3>", unsafe_allow_html=True)
        
        if process_btn:
            if not text_input:
                st.error("Please provide Input Text.")
            else:
                try:
                    result = ""
                    with st.spinner("Processing RSA..."):
                        if "Encrypt" in mode:
                            if st.session_state.rsa_public is None:
                                st.error("Cannot encrypt: No public key found.")
                            else:
                                result = rsa_cipher.encrypt(text_input, st.session_state.rsa_public)
                                st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
                                st.success("Encrypted successfully!")
                        else:
                            if st.session_state.rsa_private is None:
                                st.error("Cannot decrypt: No private key found.")
                            else:
                                result = rsa_cipher.decrypt(text_input, st.session_state.rsa_private)
                                st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
                                st.success("Decrypted successfully!")
                except Exception as e:
                    st.error(f"RSA Error: {str(e)}")
        else:
            st.info("Awaiting execution.")
        st.markdown("</div>", unsafe_allow_html=True)


elif selected_page == "Hashing":
    st.markdown("<h1 style='color: white; margin-bottom: 20px;'>Cryptographic Hashing</h1>", unsafe_allow_html=True)
    
    col_input, col_output = st.columns(2)
    
    with col_input:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-top:0;'>Input Configuration</h3>", unsafe_allow_html=True)
        
        with st.form("hash_form"):
            hash_algo = st.selectbox("Select Hash Function", ["MD5", "SHA-1", "SHA-256"])
            text_input = st.text_area("Text to Hash", height=150)
            process_btn = st.form_submit_button("Generate Hash Digest")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_output:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white; margin-top:0;'>Hash Digest Output</h3>", unsafe_allow_html=True)
        
        if process_btn:
            if not text_input:
                st.error("Please provide text to hash.")
            else:
                try:
                    with st.spinner("Hashing..."):
                        digest = hashing.hash_text(text_input, hash_algo)
                    st.markdown(f'''
                        <div style="font-size: 0.9rem; color: #94A3B8; margin-bottom: 5px;">{hash_algo} Digest:</div>
                        <div class="result-box" style="font-size: 1.2rem; font-weight: bold; text-align: center; word-break: break-all;">{digest}</div>
                    ''', unsafe_allow_html=True)
                    st.success("Hash generated!")
                except Exception as e:
                    st.error(f"Hashing error: {str(e)}")
        else:
            st.info("Awaiting input.")
        st.markdown("</div>", unsafe_allow_html=True)
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)