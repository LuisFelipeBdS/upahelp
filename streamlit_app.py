"""
UPA Helper - Plataforma de Auxílio Médico
Visual Retrô WIN98-XP
"""

import streamlit as st
import google.generativeai as genai
from pathlib import Path

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="UPA Helper",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CSS - VISUAL RETRÔ WIN98-XP
# ============================================================================
st.markdown("""
<style>
    /* Reset e configurações gerais */
    @import url('https://fonts.googleapis.com/css2?family=Arial&display=swap');
    
    * {
        font-family: Arial, Helvetica, sans-serif !important;
    }
    
    .stApp {
        background-color: #c0c0c0 !important;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(180deg, #000080 0%, #1084d0 100%);
        color: white;
        padding: 8px 12px;
        font-weight: bold;
        font-size: 14px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-bottom: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .main-header::before {
        content: "🏥";
        font-size: 16px;
    }
    
    /* Container principal estilo janela */
    .window-container {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #ffffff #808080 #808080 #ffffff;
        margin: 10px;
        padding: 0;
    }
    
    .window-content {
        padding: 12px;
        background-color: #c0c0c0;
    }
    
    /* Painéis internos */
    .inner-panel {
        background-color: #ffffff;
        border: 2px solid;
        border-color: #808080 #ffffff #ffffff #808080;
        padding: 10px;
        margin: 8px 0;
    }
    
    .panel-header {
        background-color: #000080;
        color: white;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: bold;
        margin: -10px -10px 10px -10px;
    }
    
    /* Área de texto */
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 2px solid !important;
        border-color: #808080 #ffffff #ffffff #808080 !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-size: 13px !important;
        color: #000000 !important;
    }
    
    .stTextArea label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }
    
    /* Botões estilo Windows 98 */
    .stButton > button {
        background-color: #c0c0c0 !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        color: #000000 !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-size: 12px !important;
        font-weight: normal !important;
        padding: 4px 16px !important;
        border-radius: 0 !important;
        min-height: 25px !important;
    }
    
    .stButton > button:hover {
        background-color: #d4d4d4 !important;
    }
    
    .stButton > button:active {
        border-color: #808080 #ffffff #ffffff #808080 !important;
    }
    
    /* Resultado boxes */
    .result-box {
        background-color: #ffffff;
        border: 2px solid;
        border-color: #808080 #ffffff #ffffff #808080;
        padding: 12px;
        margin: 8px 0;
        font-size: 13px;
        color: #000000;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .result-header {
        background: linear-gradient(180deg, #000080 0%, #1084d0 100%);
        color: white;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: bold;
        margin: -12px -12px 10px -12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Prescrição formatada */
    .prescription-box {
        background-color: #ffffff;
        border: 2px solid;
        border-color: #808080 #ffffff #ffffff #808080;
        padding: 20px;
        margin: 8px 0;
        font-size: 13px;
        color: #000000;
        font-family: Arial, Helvetica, sans-serif !important;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    /* Status bar */
    .status-bar {
        background-color: #c0c0c0;
        border: 2px solid;
        border-color: #808080 #ffffff #ffffff #808080;
        padding: 4px 8px;
        font-size: 11px;
        color: #000000;
        margin-top: 10px;
    }
    
    /* Spinner/Loading */
    .stSpinner > div {
        border-color: #000080 !important;
    }
    
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ajustes de container */
    .block-container {
        padding: 1rem 2rem !important;
        max-width: 100% !important;
    }
    
    /* Divider */
    hr {
        border-color: #808080 !important;
        margin: 15px 0 !important;
    }
    
    /* Colunas */
    .row-widget {
        gap: 10px;
    }
    
    /* Alertas */
    .stAlert {
        background-color: #ffffcc !important;
        border: 2px solid #808080 !important;
        color: #000000 !important;
    }
    
    /* Código/Preformatted */
    code, pre {
        font-family: "Courier New", monospace !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #c0c0c0 !important;
        border: 2px solid !important;
        border-color: #ffffff #808080 #808080 #ffffff !important;
        color: #000000 !important;
    }
    
    /* Input de API Key */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 2px solid !important;
        border-color: #808080 #ffffff #ffffff #808080 !important;
        font-family: Arial, Helvetica, sans-serif !important;
        font-size: 12px !important;
        color: #000000 !important;
    }
    
    .stTextInput label {
        color: #000000 !important;
        font-size: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARREGAR LISTA DE MEDICAMENTOS
# ============================================================================
@st.cache_data
def carregar_medicamentos():
    """Carrega a lista de medicamentos disponíveis na UPA"""
    try:
        med_path = Path(__file__).parent / "medicamentos_upa.txt"
        with open(med_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "Erro ao carregar lista de medicamentos."

MEDICAMENTOS_UPA = carregar_medicamentos()

# ============================================================================
# CONFIGURAÇÃO DO GEMINI
# ============================================================================
def configurar_gemini(api_key: str):
    """Configura a API do Gemini com otimizações para velocidade"""
    genai.configure(api_key=api_key)
    
    # Configuração otimizada para velocidade
    generation_config = {
        "temperature": 0.3,  # Baixa para respostas mais diretas
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 4096,  # Limitado para velocidade
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-preview-09-2025",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    return model

# ============================================================================
# PROMPTS DO SISTEMA
# ============================================================================
SYSTEM_PROMPT = f"""Você é um assistente médico especializado em atendimento de urgência/emergência em UPA.

REGRAS IMPORTANTES:
1. Seja DIRETO e CONCISO nas respostas
2. Use linguagem médica profissional
3. Para prescrições, use APENAS medicamentos desta lista disponível na UPA:

{MEDICAMENTOS_UPA}

4. Formato da prescrição deve ser:
   - Numerado
   - Nome do medicamento + concentração + forma farmacêutica
   - Dose + via de administração + frequência + duração
   - Observações quando necessário

5. Sempre considere alergias e contraindicações mencionadas na história clínica
6. Em caso de emergência grave, sugira encaminhamento apropriado
"""

def gerar_prompt_completo(historia_clinica: str) -> str:
    """Gera o prompt completo para o Gemini"""
    return f"""{SYSTEM_PROMPT}

HISTÓRIA CLÍNICA DO PACIENTE:
{historia_clinica}

Responda no seguinte formato EXATO (use os marcadores exatamente como mostrado):

===HIPÓTESE===
[Principal hipótese diagnóstica - seja específico e direto]

===CONDUTA===
[Conduta sugerida - liste os passos de forma clara e objetiva]

===PRESCRIÇÃO===
[Prescrição formatada e pronta para impressão - use apenas medicamentos da lista fornecida]
"""

# ============================================================================
# FUNÇÕES DE PROCESSAMENTO
# ============================================================================
def processar_resposta(resposta: str) -> dict:
    """Processa a resposta do Gemini e separa as seções"""
    resultado = {
        "hipotese": "",
        "conduta": "",
        "prescricao": ""
    }
    
    try:
        # Extrair hipótese
        if "===HIPÓTESE===" in resposta:
            inicio = resposta.find("===HIPÓTESE===") + len("===HIPÓTESE===")
            fim = resposta.find("===CONDUTA===") if "===CONDUTA===" in resposta else len(resposta)
            resultado["hipotese"] = resposta[inicio:fim].strip()
        
        # Extrair conduta
        if "===CONDUTA===" in resposta:
            inicio = resposta.find("===CONDUTA===") + len("===CONDUTA===")
            fim = resposta.find("===PRESCRIÇÃO===") if "===PRESCRIÇÃO===" in resposta else len(resposta)
            resultado["conduta"] = resposta[inicio:fim].strip()
        
        # Extrair prescrição
        if "===PRESCRIÇÃO===" in resposta:
            inicio = resposta.find("===PRESCRIÇÃO===") + len("===PRESCRIÇÃO===")
            resultado["prescricao"] = resposta[inicio:].strip()
    
    except Exception:
        # Fallback: retorna resposta completa em cada campo
        resultado["hipotese"] = resposta
        resultado["conduta"] = resposta
        resultado["prescricao"] = resposta
    
    return resultado

def formatar_prescricao(prescricao: str) -> str:
    """Formata a prescrição para impressão"""
    linhas = [
        "=" * 60,
        "                    PRESCRIÇÃO MÉDICA",
        "=" * 60,
        "",
        f"Data: ___/___/_____",
        f"Paciente: _________________________________",
        "",
        "-" * 60,
        "",
        prescricao,
        "",
        "-" * 60,
        "",
        "Assinatura/Carimbo: _______________________",
        "",
        "=" * 60
    ]
    return "\n".join(linhas)

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================
def main():
    # Header da janela
    st.markdown('<div class="main-header">UPA Helper - Sistema de Auxílio ao Atendimento Médico</div>', unsafe_allow_html=True)
    
    # Container principal
    st.markdown('<div class="window-content">', unsafe_allow_html=True)
    
    # API Key via secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # Área de entrada da história clínica
    st.markdown("**📋 História Clínica do Paciente:**")
    historia_clinica = st.text_area(
        label="Digite a história clínica",
        placeholder="Ex: Paciente masculino, 45 anos, queixa de dor torácica há 2 horas, tipo opressiva, irradiando para MSE. HAS, DM2. Nega alergias...",
        height=150,
        label_visibility="collapsed"
    )
    
    # Botão de análise
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        analisar = st.button("▶️ Analisar", use_container_width=True)
    with col2:
        limpar = st.button("🗑️ Limpar", use_container_width=True)
    
    if limpar:
        st.session_state.pop("resultado", None)
        st.rerun()
    
    # Processamento
    if analisar:
        if not historia_clinica.strip():
            st.warning("⚠️ Digite a história clínica do paciente.")
        else:
            with st.spinner("🔄 Processando..."):
                try:
                    model = configurar_gemini(api_key)
                    prompt = gerar_prompt_completo(historia_clinica)
                    response = model.generate_content(prompt)
                    resultado = processar_resposta(response.text)
                    st.session_state["resultado"] = resultado
                except Exception as e:
                    st.error(f"❌ Erro ao processar: {str(e)}")
    
    # Exibir resultados
    if "resultado" in st.session_state:
        resultado = st.session_state["resultado"]
        
        st.markdown("---")
        
        # Hipótese Diagnóstica
        st.markdown("**🔍 HIPÓTESE DIAGNÓSTICA:**")
        col_hip, col_btn_hip = st.columns([5, 1])
        with col_hip:
            st.markdown(f'<div class="result-box">{resultado["hipotese"]}</div>', unsafe_allow_html=True)
        with col_btn_hip:
            if st.button("📋 Copiar", key="copy_hip"):
                st.code(resultado["hipotese"], language=None)
                st.info("Selecione e copie o texto acima (Ctrl+C)")
        
        st.markdown("")
        
        # Conduta
        st.markdown("**📝 CONDUTA SUGERIDA:**")
        col_cond, col_btn_cond = st.columns([5, 1])
        with col_cond:
            st.markdown(f'<div class="result-box">{resultado["conduta"]}</div>', unsafe_allow_html=True)
        with col_btn_cond:
            if st.button("📋 Copiar", key="copy_cond"):
                st.code(resultado["conduta"], language=None)
                st.info("Selecione e copie o texto acima (Ctrl+C)")
        
        st.markdown("")
        
        # Prescrição
        st.markdown("**💊 PRESCRIÇÃO MÉDICA:**")
        prescricao_formatada = formatar_prescricao(resultado["prescricao"])
        col_presc, col_btn_presc = st.columns([5, 1])
        with col_presc:
            st.markdown(f'<div class="prescription-box">{prescricao_formatada}</div>', unsafe_allow_html=True)
        with col_btn_presc:
            if st.button("📋 Copiar", key="copy_presc"):
                st.code(prescricao_formatada, language=None)
                st.info("Selecione e copie o texto acima (Ctrl+C)")
    
    # Status bar
    st.markdown('<div class="status-bar">UPA Helper v1.0 | Powered by Gemini 2.0 Flash | Use com responsabilidade médica</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

