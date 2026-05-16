import streamlit as st
import requests
from PIL import Image
import plotly.graph_objects as go
import time

# Configuração da página
st.set_page_config(
    page_title="Road Surface AI",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Design System - Tokens e Componentes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* ========== DESIGN TOKENS ========== */
    :root {
        /* Colors - Semantic */
        --color-primary-50: #E0F7FF;
        --color-primary-100: #B3EAFF;
        --color-primary-500: #00D9FF;
        --color-primary-700: #0099CC;
        --color-primary-900: #005577;
        
        --color-secondary-50: #F0EDFF;
        --color-secondary-500: #7B68EE;
        --color-secondary-700: #5A47CC;
        
        --color-accent-500: #FF3D71;
        --color-success-500: #00F5A0;
        --color-warning-500: #FFB800;
        --color-error-500: #FF3D71;
        
        /* Neutrals */
        --color-neutral-50: #F8F9FA;
        --color-neutral-100: #E9ECEF;
        --color-neutral-200: #DEE2E6;
        --color-neutral-300: #CED4DA;
        --color-neutral-400: #ADB5BD;
        --color-neutral-500: #6C757D;
        --color-neutral-700: #495057;
        --color-neutral-800: #343A40;
        --color-neutral-900: #212529;
        
        /* Surface colors */
        --surface-primary: #0A0E27;
        --surface-secondary: #141B3D;
        --surface-tertiary: #1F2952;
        --surface-overlay: rgba(20, 27, 61, 0.8);
        
        /* Text colors */
        --text-primary: #FFFFFF;
        --text-secondary: #B8C0E0;
        --text-tertiary: #8891B0;
        --text-disabled: #5A6282;
        
        /* Spacing scale (8px base) */
        --space-1: 0.25rem;  /* 4px */
        --space-2: 0.5rem;   /* 8px */
        --space-3: 0.75rem;  /* 12px */
        --space-4: 1rem;     /* 16px */
        --space-5: 1.5rem;   /* 24px */
        --space-6: 2rem;     /* 32px */
        --space-8: 3rem;     /* 48px */
        --space-10: 4rem;    /* 64px */
        
        /* Border radius */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        --radius-full: 9999px;
        
        /* Shadows */
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
        --shadow-xl: 0 16px 64px rgba(0, 0, 0, 0.3);
        --shadow-glow-primary: 0 0 32px rgba(0, 217, 255, 0.3);
        --shadow-glow-secondary: 0 0 32px rgba(123, 104, 238, 0.3);
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
        
        /* Typography */
        --font-sans: 'Inter', -apple-system, system-ui, sans-serif;
        --font-mono: 'JetBrains Mono', 'Courier New', monospace;
        
        --text-xs: 0.75rem;
        --text-sm: 0.875rem;
        --text-base: 1rem;
        --text-lg: 1.125rem;
        --text-xl: 1.25rem;
        --text-2xl: 1.5rem;
        --text-3xl: 2rem;
        --text-4xl: 2.5rem;
        --text-5xl: 3.5rem;
    }
    
    /* ========== BASE STYLES ========== */
    .stApp {
        background: linear-gradient(135deg, var(--surface-primary) 0%, #1a1f3a 50%, var(--surface-primary) 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        font-family: var(--font-sans);
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Grid pattern overlay */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: 
            linear-gradient(rgba(123, 104, 238, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(123, 104, 238, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }
    
    .main > div {
        position: relative;
        z-index: 1;
    }
    
    /* ========== TYPOGRAPHY ========== */
    h1 {
        font-family: var(--font-sans) !important;
        font-weight: 900 !important;
        font-size: var(--text-5xl) !important;
        background: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-secondary-500) 50%, var(--color-accent-500) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: var(--space-3) !important;
        letter-spacing: -0.04em;
        line-height: 1.1;
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { 
            filter: drop-shadow(0 0 24px rgba(0, 217, 255, 0.4));
            transform: translateY(0);
        }
        50% { 
            filter: drop-shadow(0 0 40px rgba(123, 104, 238, 0.6));
            transform: translateY(-2px);
        }
    }
    
    h2, h3 {
        font-family: var(--font-sans) !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    h2 { font-size: var(--text-2xl) !important; }
    h3 { font-size: var(--text-xl) !important; }
    
    p, span, label, div {
        font-family: var(--font-sans) !important;
        color: var(--text-secondary) !important;
        line-height: 1.6;
    }
    
    .subtitle {
        font-family: var(--font-mono);
        color: var(--text-tertiary);
        text-align: center;
        font-size: var(--text-sm);
        margin-bottom: var(--space-8);
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* ========== COMPONENTS ========== */
    
    /* Card component */
    .element-container:has(> .stImage),
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, var(--surface-overlay), rgba(20, 27, 61, 0.4)) !important;
        backdrop-filter: blur(24px) saturate(180%);
        border-radius: var(--radius-xl);
        border: 1px solid rgba(123, 104, 238, 0.15);
        padding: var(--space-5);
        transition: all var(--transition-base);
        position: relative;
        overflow: hidden;
    }
    
    .element-container:has(> .stImage)::after,
    [data-testid="stFileUploader"]::after {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: var(--radius-xl);
        padding: 1px;
        background: linear-gradient(135deg, 
            rgba(0, 217, 255, 0.2),
            rgba(123, 104, 238, 0.2),
            rgba(255, 61, 113, 0.2)
        );
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        opacity: 0;
        transition: opacity var(--transition-base);
    }
    
    .element-container:has(> .stImage):hover::after,
    [data-testid="stFileUploader"]:hover::after {
        opacity: 1;
    }
    
    .element-container:has(> .stImage):hover,
    [data-testid="stFileUploader"]:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl), var(--shadow-glow-primary);
    }
    
    /* Button component */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-secondary-500) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-4) var(--space-6) !important;
        font-family: var(--font-sans) !important;
        font-weight: 700 !important;
        font-size: var(--text-base) !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        transition: all var(--transition-base) !important;
        box-shadow: var(--shadow-lg), 0 0 20px rgba(0, 217, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
        opacity: 0;
        transition: opacity var(--transition-fast);
    }
    
    .stButton > button:hover::before {
        opacity: 1;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: var(--shadow-xl), 0 0 32px rgba(0, 217, 255, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.99) !important;
    }
    
    /* Metric component */
    [data-testid="stMetricValue"] {
        font-family: var(--font-sans) !important;
        font-weight: 800 !important;
        font-size: var(--text-4xl) !important;
        background: linear-gradient(135deg, var(--color-success-500) 0%, var(--color-primary-500) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: var(--font-mono) !important;
        color: var(--text-tertiary) !important;
        font-size: var(--text-xs) !important;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* Alert components */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 245, 160, 0.12), rgba(0, 217, 255, 0.08)) !important;
        border-left: 4px solid var(--color-success-500) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--space-4) var(--space-5) !important;
        font-family: var(--font-sans) !important;
        font-weight: 600 !important;
        color: var(--color-success-500) !important;
        backdrop-filter: blur(12px);
        box-shadow: var(--shadow-md), 0 0 24px rgba(0, 245, 160, 0.1);
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.12), rgba(123, 104, 238, 0.08)) !important;
        border-left: 4px solid var(--color-primary-500) !important;
        border-radius: var(--radius-md) !important;
        color: var(--color-primary-500) !important;
        backdrop-filter: blur(12px);
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 184, 0, 0.12), rgba(255, 61, 113, 0.08)) !important;
        border-left: 4px solid var(--color-warning-500) !important;
        border-radius: var(--radius-md) !important;
        color: var(--color-warning-500) !important;
        backdrop-filter: blur(12px);
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 61, 113, 0.15), rgba(255, 61, 113, 0.08)) !important;
        border-left: 4px solid var(--color-error-500) !important;
        border-radius: var(--radius-md) !important;
        color: var(--color-error-500) !important;
        backdrop-filter: blur(12px);
    }
    
    /* Upload component */
    [data-testid="stFileUploader"] section {
        border: 2px dashed var(--color-primary-500) !important;
        border-radius: var(--radius-lg) !important;
        background: linear-gradient(145deg, 
            rgba(0, 217, 255, 0.05), 
            rgba(123, 104, 238, 0.05)
        ) !important;
        padding: var(--space-8) !important;
        transition: all var(--transition-base) !important;
    }
    
    [data-testid="stFileUploader"] section:hover {
        border-color: var(--color-secondary-500) !important;
        background: linear-gradient(145deg, 
            rgba(0, 217, 255, 0.1), 
            rgba(123, 104, 238, 0.1)
        ) !important;
        box-shadow: 0 0 40px rgba(0, 217, 255, 0.15);
    }
    
    /* Status badge component */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: var(--space-2);
        padding: var(--space-2) var(--space-4);
        border-radius: var(--radius-full);
        font-family: var(--font-mono);
        font-size: var(--text-xs);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: var(--space-2);
        box-shadow: var(--shadow-md);
        transition: all var(--transition-base);
    }
    
    .status-online {
        background: linear-gradient(135deg, 
            rgba(0, 245, 160, 0.2), 
            rgba(0, 217, 255, 0.2)
        );
        color: var(--color-success-500);
        border: 1px solid var(--color-success-500);
        animation: pulseGlow 2s ease-in-out infinite;
    }
    
    .status-offline {
        background: linear-gradient(135deg, 
            rgba(255, 61, 113, 0.2), 
            rgba(255, 184, 0, 0.2)
        );
        color: var(--color-error-500);
        border: 1px solid var(--color-error-500);
    }
    
    @keyframes pulseGlow {
        0%, 100% { 
            box-shadow: 0 0 16px rgba(0, 245, 160, 0.3);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 28px rgba(0, 245, 160, 0.6);
            transform: scale(1.02);
        }
    }
    
    /* ========== UTILITIES ========== */
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: var(--color-primary-500) transparent transparent transparent !important;
    }
    
    /* Charts */
    .js-plotly-plot {
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        background: var(--surface-secondary);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface-primary);
        border-radius: var(--radius-sm);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, 
            var(--color-primary-500), 
            var(--color-secondary-500)
        );
        border-radius: var(--radius-sm);
        border: 2px solid var(--surface-primary);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, 
            var(--color-primary-700), 
            var(--color-secondary-700)
        );
    }
    
    /* Selection */
    ::selection {
        background: var(--color-primary-500);
        color: white;
    }
    
    /* Focus states */
    *:focus-visible {
        outline: 2px solid var(--color-primary-500);
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

# URL da API
API_URL = "http://localhost:8000"

# Header
st.markdown("<h1>🛣️ ROAD SURFACE AI</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Deep Learning • Computer Vision • Real-Time Classification</p>', unsafe_allow_html=True)

# Status da API
col_status1, col_status2, col_status3 = st.columns([1, 2, 1])
with col_status2:
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.markdown('<div class="status-badge status-online">● API ONLINE</div>', unsafe_allow_html=True)
            api_online = True
        else:
            st.markdown('<div class="status-badge status-offline">● API OFFLINE</div>', unsafe_allow_html=True)
            api_online = False
    except:
        st.markdown('<div class="status-badge status-offline">● API OFFLINE</div>', unsafe_allow_html=True)
        st.error("🚨 Inicie a API primeiro: `python app.py`")
        api_online = False

st.markdown("<br>", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📤 UPLOAD")
    uploaded_file = st.file_uploader(
        "Arraste uma imagem ou clique para selecionar",
        type=['jpg', 'jpeg', 'png'],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Imagem carregada")

with col2:
    st.markdown("### 🎯 RESULTADO")
    
    if uploaded_file and api_online:
        if st.button("CLASSIFICAR AGORA", type="primary"):
            with st.spinner("Processando..."):
                uploaded_file.seek(0)
                
                try:
                    files = {"image": uploaded_file.getvalue()}
                    start = time.time()
                    response = requests.post(f"{API_URL}/predict", files=files)
                    elapsed = (time.time() - start) * 1000
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Emojis e nomes
                        class_display = {
                            'asphalt': ('🛣️', 'ASPHALT'),
                            'belgian_blocks': ('🧱', 'BELGIAN BLOCKS'),
                            'offroad': ('🌾', 'OFF-ROAD')
                        }
                        
                        pred = result['prediction']
                        emoji, name = class_display.get(pred, ('🚗', pred.upper()))
                        conf = result['confidence']
                        
                        st.success(f"## {emoji} {name}")
                        
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric("CONFIANÇA", f"{conf:.1%}")
                        with col_m2:
                            st.metric("LATÊNCIA", f"{elapsed:.0f}ms")
                        
                        # Gráfico com design system colors
                        probs = result['probabilities']
                        
                        colors = ['#00D9FF', '#7B68EE', '#FF3D71']
                        
                        fig = go.Figure(data=[
                            go.Bar(
                                x=[class_display.get(k, ('', k.upper()))[1] for k in probs.keys()],
                                y=list(probs.values()),
                                text=[f"{v:.1%}" for v in probs.values()],
                                textposition='outside',
                                textfont=dict(
                                    family='Inter, sans-serif',
                                    size=14,
                                    color='#B8C0E0',
                                    weight=600
                                ),
                                marker=dict(
                                    color=colors,
                                    line=dict(color='#0A0E27', width=2),
                                    opacity=0.9
                                ),
                                hovertemplate='<b>%{x}</b><br>Probabilidade: %{y:.2%}<extra></extra>'
                            )
                        ])
                        
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(
                                family='Inter, sans-serif',
                                color='#B8C0E0',
                                size=12
                            ),
                            yaxis=dict(
                                range=[0, 1.1],
                                gridcolor='rgba(123, 104, 238, 0.08)',
                                showline=False,
                                title=None,
                                tickformat='.0%'
                            ),
                            xaxis=dict(
                                showgrid=False,
                                showline=False,
                                title=None
                            ),
                            margin=dict(l=20, r=20, t=40, b=20),
                            height=320,
                            showlegend=False,
                            hoverlabel=dict(
                                bgcolor='#141B3D',
                                font_size=13,
                                font_family='Inter'
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                    else:
                        st.error(f"❌ Erro: {response.json().get('detail', 'Desconhecido')}")
                
                except Exception as e:
                    st.error(f"❌ Erro na requisição: {str(e)}")
    
    elif not uploaded_file:
        st.info("👆 Faça upload de uma imagem primeiro")
    elif not api_online:
        st.warning("⚠️ API offline. Inicie com: `python app.py`")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
with col_f2:
    st.markdown("""
    <div style='text-align: center; font-family: var(--font-mono); color: var(--text-tertiary); font-size: var(--text-sm);'>
        <strong style='color: var(--text-secondary);'>DESENVOLVIDO POR</strong><br>
        João Henrique dos Santos Silva & Carlos Vinicius Felix da Silva<br>
        <em>CIn - UFPE | Inteligência Artificial | 2026</em><br><br>
        <strong style='color: var(--text-secondary);'>MODELO:</strong> EfficientNetV2-S | 
        <strong style='color: var(--color-success-500);'>F1-MACRO:</strong> 83.87% | 
        <strong style='color: var(--color-primary-500);'>ACC:</strong> 91.48%
    </div>
    """, unsafe_allow_html=True)
