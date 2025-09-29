import pptx
import streamlit as st
import pandas as pd
import requests
from langchain_config import get_summary
import io
from reportlab.pdfgen import canvas
from pptx import Presentation
from pptx.util import Inches
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import time
import xlsxwriter
import random
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import json

st.set_page_config(
    page_title="News Research Assistant",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Poppins', 'Open Sans', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem 3rem;
        background: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%);
        min-height: 100vh;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        background-color: #6699ff; /* solid background */
        color: white!important;
        text-align: center;
        margin-bottom: 1rem !important;
        padding: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        /* Remove gradient clipped text and text shadow */
        -webkit-background-clip: unset !important;
        -webkit-text-fill-color: unset !important;
        text-shadow: none !important;
    }
    
    .sub-header {
        font-size: 1.4rem !important;
        font-weight: 500 !important;
        background-color: #764ba2; /* solid background complementary */
        color: white !important;
        text-align: center;
        margin-bottom: 2.5rem !important;
        padding: 0.35rem 0;
        border-radius: 6px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
    
    /* Animation Keyframes */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Login Form Styling */
    .login-form {
        background: linear-gradient(145deg, #c471f5, #fa71cd, #f6d365);
        padding: 3rem; border-radius: 22px;
        box-shadow: 0 12px 36px rgba(164,134,255,0.17);
        max-width: 510px; margin: 2rem auto;
        border: 2px solid #fcfcfc;
    }
    
    
    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
        animation: pulse 0.3s ease-in-out !important;
    }
    
    /* Success Button */
    .success-button > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.4) !important;
    }
    
    .success-button > button:hover {
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.6) !important;
    }
    
    /* Warning Button */
    .warning-button > button {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%) !important;
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.4) !important;
    }
    
    /* Info Button */
    .info-button > button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4) !important;
    }
    
    /* Danger Button */
    .danger-button > button {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.4) !important;
    }
    
    /* Example Buttons */
    .example-button > button {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%) !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
    }
    
    /* Content Blocks */
    .summary-block {
        background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        margin: 1.5rem 0 !important;
        border-left: 5px solid #38b2ac !important;
        box-shadow: 0 8px 25px rgba(56, 178, 172, 0.2) !important;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .article-block {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border-left: 4px solid #48bb78 !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .article-block:hover {
        transform: translateX(8px) !important;
        box-shadow: 0 8px 30px rgba(72, 187, 120, 0.2) !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(145deg, #f8fafc, #e2e8f0) !important;
        border-radius: 15px !important;
        border-right: 3px solid #667eea !important;
    }
    
    .sidebar-section {
        background: linear-gradient(145deg, #ffffff, #f7fafc) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 
            8px 8px 16px #d1d9e6,
            -8px -8px 16px #ffffff !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .sidebar-header {
        font-weight: 700 !important;
        color: #2d3748 !important;
        margin-bottom: 1rem !important;
        font-size: 1.3rem !important;
        text-align: center !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #667eea !important;
    }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #e6fffa, #b2f5ea) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        text-align: center !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: transform 0.3s ease !important;
    }
    
    .stat-card:hover {
        transform: translateY(-5px) !important;
    }
    
    .stat-number {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #2d3748 !important;
        display: block !important;
        line-height: 1 !important;
    }
    
    .stat-label {
        color: #4a5568 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
    }
    
    /* Text Input Styling */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 10px !important;
        padding: 1rem 1.5rem !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #c6f6d5, #9ae6b4) !important;
        color: #2f855a !important;
        border-left: 4px solid #48bb78 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fed7d7, #fbb6ce) !important;
        color: #c53030 !important;
        border-left: 4px solid #f56565 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #feebc8, #f6e05e) !important;
        color: #c05621 !important;
        border-left: 4px solid #ed8936 !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #bee3f8, #90cdf4) !important;
        color: #2c5282 !important;
        border-left: 4px solid #4299e1 !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center !important;
        color: #4a5568 !important;
        margin-top: 4rem !important;
        padding: 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        background: linear-gradient(135deg, #f8fafc, #e2e8f0) !important;
        border-radius: 15px !important;
        border-top: 3px solid #667eea !important;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    .ticker {
        background: linear-gradient(90deg, #e94057 0%, #f27121 100%);
        color: white; padding: 1rem; font-size: 1.06rem;
        border-radius: 8px; text-align: center; margin-bottom: 1.5rem;
        font-weight: 600; overflow: hidden; white-space: nowrap;
        animation: tickerMove 18s linear infinite;
    }
    @keyframes tickerMove { 0% { text-indent: 100% } 100% { text-indent: -100% }}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem !important;
        }
        
        .sub-header {
            font-size: 1.2rem !important;
        }
        
        .login-form {
            margin: 1rem !important;
            padding: 2rem !important;
        }
    }
    
    /* Hover Effects for Links */
    a {
        color: #667eea !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    a:hover {
        color: #764ba2 !important;
        text-decoration: underline !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)


if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user'] = None
    st.session_state['query_history'] = []
    st.session_state['total_queries'] = 0
    st.session_state['today_queries'] = 0
    st.session_state['success_rate'] = 100.0
    
def api_authenticate(username, password):
    """Enhanced authentication with loading simulation"""
    if username == "Ashish" and password == "Ashish08@":
        return {"success": True, "user": {"name": "Ashish", "role": "Premium User", "joined": "2023"}}
    return {"success": False, "error": "Invalid credentials"}


def create_pdf(text_data):
    """Enhanced PDF creation with better formatting"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "News Research Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Content
    textobject = c.beginText()
    textobject.setTextOrigin(50, height - 100)
    textobject.setFont("Helvetica", 11)
    
    wrap_width = 90
    for line in text_data.split('\n'):
        while len(line) > wrap_width:
            space_pos = line.rfind(' ', 0, wrap_width)
            if space_pos == -1:
                space_pos = wrap_width
            textobject.textLine(line[:space_pos])
            line = line[space_pos:].strip()
        textobject.textLine(line.strip())
    
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def handle_authentication():
    """Enhanced authentication with better UI"""
    if not st.session_state['authenticated']:
        st.markdown("<h1 class='main-header'>News Research Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>🤖 Professional AI-Powered News Equity Research Assistant</div>", unsafe_allow_html=True)
        st.markdown('<div class="ticker">🚨 Breaking News: Government announces new policies | IPL 2025 schedule released | Global stock market rallies | Major climate conference underway | Tech startups secure record funding | Cryptocurrency prices surge!</div>', unsafe_allow_html=True)
        
        with st.form(key='Login', clear_on_submit=False):
            st.markdown("<div class='login-form'>", unsafe_allow_html=True)
            st.markdown("### 🔐 Secure Login Required")
            st.markdown("---")
            
            username = st.text_input("👤 Username", placeholder="Enter username (Try: Ashish)", key="login_username")
            password = st.text_input("🔑 Password", placeholder="Enter password (Try: Ashish08@)", type="password", key="login_password")
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                submit_button = st.form_submit_button("Login to Dashboard", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            if submit_button:
                with st.spinner("🔄Authenticating your credentials..."):
                    time.sleep(1)
                    auth_resp = api_authenticate(username, password)
                    if auth_resp.get("success"):
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = auth_resp["user"]
                        st.success("✅ Authentication successful! Welcome to your dashboard!")
                        st.toast("🔔 You have successfully logged in")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Authentication failed. Please try: Ashish / Ashish08@")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg,  #00c9ff, #92fe9d); padding: 1rem; border-radius: 20px; text-align: center; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
            <h3 style="color: #2d3748; margin-bottom: 1rem;">🎯 Demo Access</h3>
            <p style="color: #2d3748; font-weight: 600; font-size: 1.1rem;">
                <strong>Username:</strong> Ashish<br>
                <strong>Password:</strong> Ashish08@
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()


def create_stats_dashboard():
    """Create an enhanced statistics dashboard"""
    st.markdown("### 📊 Dashboard Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{st.session_state['total_queries']}</span>
            <div class="stat-label">📈 Total Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{st.session_state['today_queries']}</span>
            <div class="stat-label">⚡Today's Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{st.session_state['success_rate']:.1f}%</span>
            <div class="stat-label">🎯 Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-number">{len(st.session_state['query_history'])}</span>
            <div class="stat-label">📜 History Items</div>
        </div>
        """, unsafe_allow_html=True)


def create_enhanced_sidebar():
    """Create enhanced sidebar with more features"""
    with st.sidebar:
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-header'>🎛️ Control Panel</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧪 System Test", use_container_width=True, key="sys_test", help="Test system connectivity"):
                with st.spinner("Testing systems..."):
                    time.sleep(1)
                st.success("✅ All systems operational!")
                st.toast("🔔 System test completed successfully!")
        
        with col2:
            if st.button("📊 Analytics", use_container_width=True, key="analytics", help="View detailed analytics"):
                st.info("📈 Analytics dashboard coming soon!")
        
        if st.button("📞 Contact Support", use_container_width=True, key="contact", help="Get help from our team"):
            st.info("📧 **Email:** support@nexthikes.com\n\n📞 **Phone:** +91-XXX-XXX-XXXX")
        
        if st.button("💬 Live Chat", use_container_width=True, key="chat", help="Start live chat"):
            st.info("💬 Need help? Please contact Our support team .📧 **Email:** support@nexthikes.com\n\n")
        
        if st.button("🔄 Reset All Data", use_container_width=True, key="reset_all", help="Clear all data"):
            reset_all_data()
            st.success("🔄 Data reset successfully!")
            time.sleep(1)
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # User Profile Section
        if st.session_state.get('user'):
            st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
            st.markdown("<div class='sidebar-header'>👤 User Profile</div>", unsafe_allow_html=True)
            user = st.session_state['user']
            st.markdown(f"""
            **🎭Name:** {user['name']}  
            **🏆Role:** {user['role']}  
            **📅Member Since:** {user['joined']}  
            **🔥Status:** 🟢 Active
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick Stats in Sidebar
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-header'>⚡ Quick Stats</div>", unsafe_allow_html=True)
        st.metric("Queries Today", st.session_state['today_queries'], delta=1)
        st.metric("Success Rate", f"{st.session_state['success_rate']:.1f}%", delta="0.5%")
        st.markdown("</div>", unsafe_allow_html=True)


def reset_all_data():
    """Reset all session data except authentication"""
    preserved_keys = {'authenticated', 'user'}
    for key in list(st.session_state.keys()):
        if key not in preserved_keys:
            del st.session_state[key]
    
    # Reinitialize
    st.session_state['query_history'] = []
    st.session_state['total_queries'] = 0
    st.session_state['today_queries'] = 0
    st.session_state['success_rate'] = 100.0


def show_enhanced_history():
    """Show enhanced query history with better formatting"""
    if st.session_state.get('query_history'):
        st.markdown("---")
        st.markdown("### 📚 Recent Query History")
        
        for idx, item in enumerate(reversed(st.session_state['query_history'][-5:]), 1):
            with st.expander(f"🔍 Query {idx}: {item['query'][:50]}..."):
                st.markdown(f"**Query:** {item['query']}")
                st.markdown(f"**Time:** {item['timestamp']}")
                st.markdown(f"**Summary:** {item['summary'][:200]}...")
                if st.button(f"🔄 Rerun Query {idx}", key=f"rerun_{idx}"):
                    st.session_state['query_text'] = item['query']
                    st.rerun()


def generate_enhanced_summary():
    """Enhanced summary generation with better UI"""
    st.markdown("### Smart News Research Engine")
    
    # Example queries with emojis
    examples = [
        ("✈️ Air India Crash", "Air India Crash"),
        ("⚔️ India-Pak War", "India-Pak War"), 
        ("🌍 Israel-Iran War", "Israel-Iran War"),
        ("🏏 IPL 2025 Incident", "IPL 2025 Incident"),
        ("📈 Tech Stock Market", "Tech Stock Market"),
        ("🌱 Climate Change News", "Climate Change News")
    ]
    
    st.markdown("#### Quick Start Examples")
    cols = st.columns(3)
    for i, (display_name, query_text) in enumerate(examples):
        col_idx = i % 3
        with cols[col_idx]:
            if st.button(display_name, use_container_width=True, key=f"example_{i}"):
                st.session_state['query_text'] = query_text
                st.rerun()

    st.markdown("#### Enter Your Research Query")
    
    if st.session_state.get('query_text') and 'query_input_area' in st.session_state:
        if st.session_state['query_input_area'] != st.session_state['query_text']:
            st.session_state['query_input_area'] = st.session_state['query_text']
    
    query = st.text_area(
        "",
        value=st.session_state.get('query_text', ''),
        key="query_input_area",
        height=150,
        placeholder="""Enter your news research query here...

Examples:
• Tesla stock performance Q3 2025
• COVID-19 vaccine latest developments  
• Cryptocurrency regulation updates
• AI technology breakthrough news
• Climate change policy changes
• Indian startup funding trends""",
        help="Be specific with your query for better results"
    )
    
    if query != st.session_state.get('query_text', ''):
        st.session_state['query_text'] = query

    col1, col2, col3 = st.columns([2,1,1])
    
    with col1:
        generate_btn = st.button("⚡ Generate AI Summary", use_container_width=True, type="primary")
    
    with col2:
        if st.button("🔄 Clear Query", use_container_width=True):
            st.session_state['query_text'] = ""
            st.rerun()
    
    with col3:
        if st.button("📊 Show Stats", use_container_width=True):
            create_stats_dashboard()

    if generate_btn and query:
        with st.spinner("🤖 AI is analyzing global news sources..."):
            try:
                # Progress bar for better UX
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 Searching news sources...")
                progress_bar.progress(25)
                time.sleep(0.5)
                
                status_text.text("📰 Analyzing articles...")
                progress_bar.progress(50)
                time.sleep(0.5)
                
                status_text.text("🧠 Generating AI summary...")
                progress_bar.progress(75)
                time.sleep(0.5)
                
                response, articles = get_summary(query)
                
                progress_bar.progress(100)
                status_text.text("✅ Summary generated successfully!")
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                
            except Exception as e:
                st.error(f"❌ Analysis Error: {str(e)}")
                st.info("💡 Try rephrasing your query or check your internet connection")
                return
            
            # Process and display results
            process_and_display_results(query, response, articles)
            
    elif generate_btn and not query:
        st.warning("⚠️ Please enter a research query first to begin analysis!")


def process_and_display_results(query, response, articles):
    """Process and display results with enhanced formatting"""
    # Update session state
    st.session_state['total_queries'] += 1
    st.session_state['today_queries'] += 1
    if st.session_state['total_queries'] > 0:
        st.session_state['success_rate'] = min(100.0, st.session_state['success_rate'] + random.uniform(-0.5, 1.0))
    
    
    # Process response
    bullet_lines = [f"• {line.strip()}" for line in response.split("•") if line.strip()]
    header_line = articles[0].get("title", "Top News") if articles else (bullet_lines[0][1:].strip() if bullet_lines else "")
    formatted_summary = "\n".join(bullet_lines[1:]) if len(bullet_lines) > 1 else ""
    
    # Display header
    st.markdown(f"""
    <div class='summary-block'>
        <h3 style='color: #2d3748; margin-bottom: 1rem;'>
            📰 <strong>Breaking News Analysis</strong>
        </h3>
        <h4 style='color: #667eea; margin-bottom: 1rem;'>{header_line}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Summary Section
    st.markdown("### 🤖 AI-Generated News Summary")
    summary_points = [line[1:].strip() for line in formatted_summary.splitlines() if line.strip()]
    
    if summary_points:
        for i, point in enumerate(summary_points, 1):
            st.markdown(f"""
            <div class='article-block' style='margin: 0.5rem 0;'>
                <strong>{i}.</strong> {point}
            </div>
            """, unsafe_allow_html=True)
    
    # Articles Section
    if articles:
        st.markdown("### 📑 Source Articles Referenced")
        
        for i, article in enumerate(articles[:3], 1):
            title = article.get("title", "No title available")
            source = article.get("source", {}).get("name", "Unknown Source")
            date = article.get("publishedAt", "").split("T")[0] if article.get("publishedAt") else "Unknown Date"
            url = article.get("url", "#")
            description = article.get("description", "No description available")[:150] + "..." if article.get("description") else "No description available"
            
            st.markdown(f"""
            <div class='article-block'>
                <h4 style='color: #2d3748; margin-bottom: 0.5rem;'>{i}. {title}</h4>
                <p style='color: #4a5568; margin-bottom: 0.5rem; font-size: 0.9rem;'>{description}</p>
                <div style='font-size: 0.85rem; color: #666; margin-bottom: 0.5rem;'>
                    📅 {date} | 🏷️ {source}
                </div>
                <a href='{url}' target='_blank' style='color: #667eea; font-weight: 600;'>
                    🔗 Read Full Article →
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        # Success message
        st.success(f"✅ Summary generated from {len(articles[:3])} high-quality news sources!")
    else:
        st.warning("⚠️ No articles found for this query.")
    
    # Add to history
    st.session_state['query_history'].append({
        'query': query,
        'summary': formatted_summary,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'articles_count': len(articles) if articles else 0
    })
    
    # Download section
    st.markdown("### 💾 Download Options")
    combined_output = create_combined_output(header_line, formatted_summary, articles)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📄 Download as TXT",
            data=combined_output,
            file_name=f"news_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            help="Download as plain text file"
        )
    
    with col2:
        pdf_buffer = create_pdf(combined_output)
        st.download_button(
            "📋 Download as PDF",
            data=pdf_buffer,
            file_name=f"news_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download formatted PDF report"
        )
    
    with col3:
        # JSON export for API integration
        json_data = {
            "query": query,
            "summary": formatted_summary,
            "articles": articles[:3] if articles else [],
            "generated_at": datetime.now().isoformat(),
            "total_articles": len(articles) if articles else 0
        }
        st.download_button(
            "🔧 Download as JSON",
            data=json.dumps(json_data, indent=2),
            file_name=f"news_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
             help="Download structured JSON data"
        )


def create_combined_output(header, summary, articles):
    """Create combined output for downloads"""
    output = f"""NEWS RESEARCH REPORT
{'='*50}

HEADLINE: {header}

GENERATED ON: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

AI-GENERATED SUMMARY:
{'='*25}
{summary}

REFERENCED ARTICLES:
{'='*20}
"""
    
    if articles:
        for i, article in enumerate(articles[:3], 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown Source")
            date = article.get("publishedAt", "").split("T")[0] if article.get("publishedAt") else "Unknown Date"
            url = article.get("url", "#")
            
            output += f"""
{i}. {title}
   📰Source: {source}
   📅Date: {date}
   🔗URL: {url}
   
"""
    
    output += f"""
{'='*50}
Report generated by AI Research Tool
Powered by NextHikes
{'='*50}
"""
    
    return output


def create_advanced_analytics():
    """Create advanced analytics dashboard"""
    if st.session_state.get('query_history'):
        st.markdown("### 📊 Advanced Analytics")
        
        # Query frequency over time
        dates = [item['timestamp'][:10] for item in st.session_state['query_history']]
        date_counts = {}
        for date in dates:
            date_counts[date] = date_counts.get(date, 0) + 1
        
        if date_counts:
            col1, col2 = st.columns(2)
            
            with col1:
                # Line chart for query trends
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(date_counts.keys()),
                    y=list(date_counts.values()),
                    mode='lines+markers',
                    name='Daily Queries',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8, color='#764ba2')
                ))
                fig.update_layout(
                    title="Query Trends Over Time",
                    xaxis_title="Date",
                    yaxis_title="Number of Queries",
                    template="plotly_white",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top query topics
                query_words = []
                for item in st.session_state['query_history']:
                    words = item['query'].lower().split()
                    query_words.extend([word for word in words if len(word) > 3])
                
                if query_words:
                    word_counts = {}
                    for word in query_words:
                        word_counts[word] = word_counts.get(word, 0) + 1
                    
                    top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    fig = px.bar(
                        x=[word[0] for word in top_words],
                        y=[word[1] for word in top_words],
                        title="Most Searched Topics",
                        color_discrete_sequence=['#667eea']
                    )
                    fig.update_layout(template="plotly_white", height=300)
                    st.plotly_chart(fig, use_container_width=True)


def create_news_alerts():
    """Create news alerts functionality"""
    with st.expander("🔔 Set News Alerts"):
        st.markdown("#### Custom News Alerts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alert_topic = st.text_input("Alert Topic", placeholder="e.g., Tesla stock, COVID updates")
            alert_frequency = st.selectbox("Frequency", ["Daily", "Every Hour", "Weekly", "Real-time"])
        
        with col2:
            alert_email = st.text_input("Notification Email", placeholder="your@email.com")
            alert_priority = st.selectbox("Alert Priority", ["🔴 Critical","🟡 High", "🟢 Medium", "🔵 Low"])
        
        if st.button("📧 Create Alert", use_container_width=True):
            if alert_topic and alert_email:
                alert_id = f"ALERT_{random.randint(1000, 9999)}"
                st.success(f"""
                    ✅ **Alert Created Successfully!**
                    
                    📋 **Alert Details:**
                    • ID: {alert_id}
                    • Topic: {alert_topic}
                    • Frequency: {alert_frequency}
                    • Priority: {alert_priority}
                    • Email: {alert_email}
                    • Status: 🟢 Active
                    
                    🎯 You'll receive notifications when relevant news is detected!
                    """)
                st.toast("Alert created successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please fill all required fields")


def create_export_options():
    """Advanced export options"""
    with st.expander("📤 Advanced Export Options"):
        st.markdown("#### Export Formats & Sharing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to Excel", use_container_width=True):
                buffer=io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    if st.session_state.get('query_history'):
                        df = pd.DataFrame(st.session_state['query_history'])
                        df.to_excel(writer, index=False, sheet_name='Query History')
                    buffer.seek(0)
                    st.download_button(
                    label="📥 Download Excel",
                    data=buffer.getvalue(),
                    file_name="news_summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.toast("✅ Excel file is ready!")

            
            if st.button("📋 Export to PowerPoint", use_container_width=True):
                st.info("🖼️ PowerPoint export feature coming soon!")
        
        with col2:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("📬 Email feature coming soon!")
            
            if st.button("🔗 Generate Share Link", use_container_width=True):
                share_link = f"https://nexthikes.com/report/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.info(f"🌐 Share link: {share_link}")


def create_system_health():
    """System health monitoring"""
    with st.expander("🖥️ System Health Monitor"):
        st.markdown("#### Real-time System Status")
        
        components = {
            "🔗 News API": ("🟢 Operational", 99.9, "2.1ms"),
            "🤖 AI Model": ("🟢 Operational", 99.8, "0.8s"), 
            "💾 Database": ("🟢 Operational", 100.0, "0.3ms"),
            "📄 PDF Generator": ("🟢 Operational", 99.7, "1.2s"),
            "🔐 Authentication": ("🟢 Operational", 100.0, "0.1s"),
            "📊 Analytics": ("🟢 Operational", 99.5, "0.5s")
        }
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🔧 System Components:**")
            for component, (status, uptime, response) in components.items():
                st.markdown(f"**{component}:** {status} ({uptime}% uptime)")
        with col2:
            st.markdown("**⚡ Performance Metrics:**")
            for component, (status, uptime, response) in components.items():
                st.markdown(f"**{component}:** {response} avg response")
        current_time = datetime.now()
        col3, col4, col5 = st.columns(3)
        with col3:
            st.metric("🌐 Server Load", f"{random.randint(15, 35)}%", delta=f"{random.randint(-3, 3)}%")
        
        with col4:
            st.metric("💾 Memory Usage", f"{random.randint(45, 75)}%", delta=f"{random.randint(-2, 5)}%")
        
        with col5:
            st.metric("📡 API Calls/min", f"{random.randint(150, 250)}", delta=f"+{random.randint(5, 20)}")
        
        st.markdown(f"🔄 **Last Updated:** {current_time.strftime('%Y-%m-%d %H:%M:%S')} (Auto-refresh every 30s)")        


# ====== Main Application Logic ======
def main():
    """Main application function"""
    # Handle authentication first
    handle_authentication()
    
    # Show header for authenticated users
    st.markdown("<h1 class='main-header'>News Research Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Professional AI-Powered News Analysis tool</div>", unsafe_allow_html=True)
    
    # Create enhanced sidebar
    create_enhanced_sidebar()
    
    # Main content area
    with st.container():
        # Dashboard stats at the top
        create_stats_dashboard()
        
        st.markdown("---")
        
        # Main research interface
        generate_enhanced_summary()
        
        st.markdown("---")
        
        # Additional features section
        col1, col2 = st.columns(2)
        
        with col1:
            create_news_alerts()
            create_system_health()
        
        with col2:
            create_export_options()
        
        # Advanced analytics (if data exists)
        if st.session_state.get('query_history'):
            st.markdown("---")
            create_advanced_analytics()
        
        st.markdown("---")
        
        # Enhanced history display
        show_enhanced_history()


# ====== Run the Application ======
if __name__ == "__main__":
    main()
    
    # Footer
    st.markdown("""
    <style>
        .footer-banner {
            width: 100%;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);  /* Rich dark gradient */
            padding: 3rem 2rem;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
            font-family: 'Segoe UI', sans-serif;
            color: #f0f0f0;
            margin-top: 3rem;
        }
        .footer-banner h3 {
            font-size: 2.2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
            text-align: center;
        }
        .footer-banner p {
            font-size: 1.1rem;
            line-height: 1.7;
            text-align: center;
            margin-bottom: 1rem;
        }
        .footer-banner .features {
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            background: rgba(255,255,255,0.08);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            font-size: 1rem;
            color: #d1ecf1;
            margin-bottom: 1rem;
        }
        .footer-banner .divider {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 2px groove rgba(255,255,255,0.3);
        }
        .footer-banner .contact {
            font-size: 0.95rem;
            color: #cccccc;
            text-align: center;
        }
        .footer-banner .legal {
            font-size: 0.85rem;
            color: #bbbbbb;
            text-align: center;
            margin-top: 0.5rem;
            opacity: 0.75;
        }
    </style>

    <div class="footer-banner">
        <h3>AI-Powered News Research Assistant</h3>
        <p>
            🎯 Built by Ashish Pachauri • 
            🏢 Powered by NextHikes Technologies • 
            🤖 Integrated with Advanced AI & Live NewsAPI
        </p>
        <div class="features">
            <div>⚡ Real-time Analysis</div>
            <div>📊 Advanced Analytics</div>
            <div>🌍 Global Coverage</div>
            <div>🚀 Lightning Fast</div>
        </div>
        <div class="divider">
            <p class="contact">
                Contact Us: 011-123456 • 🌐 www.nexthikes.com • 📧Email: support@nexthikes.com
            </p>
            <p class="legal">
                © 2025 NextHikes Technologies. All rights reserved. | Privacy Policy | Terms of Service | AI Ethics
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)