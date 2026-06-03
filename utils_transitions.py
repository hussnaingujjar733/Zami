"""
utils_transitions.py — ZAMI Premium Page Transitions
Smooth fade, slide, and micro-animations for trillion dollar feel
"""

import streamlit as st

def inject_page_transitions():
    """Injects smooth page transition effects"""
    
    transitions_html = """
    <style>
    /* ─────────────────────────────────────────────
       PAGE TRANSITION ANIMATIONS
    ───────────────────────────────────────────── */
    
    /* Fade in animation for main content */
    .main > div {
        animation: pageFadeIn 0.5s cubic-bezier(0.2, 0.8, 0.4, 1) forwards;
    }
    
    @keyframes pageFadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Staggered animations for cards */
    .card {
        animation: cardSlideUp 0.5s ease-out forwards;
        opacity: 0;
    }
    
    @keyframes cardSlideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Individual card delays */
    .card:nth-child(1) { animation-delay: 0s; }
    .card:nth-child(2) { animation-delay: 0.08s; }
    .card:nth-child(3) { animation-delay: 0.16s; }
    .card:nth-child(4) { animation-delay: 0.24s; }
    .card:nth-child(5) { animation-delay: 0.32s; }
    .card:nth-child(6) { animation-delay: 0.40s; }
    
    /* Button press ripple effect */
    .stButton button {
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
    }
    
    .stButton button:active {
        transform: scale(0.96) !important;
    }
    
    /* Input focus glow animation */
    .stTextInput input:focus,
    .stSelectbox select:focus,
    .stTextArea textarea:focus {
        animation: inputGlow 0.3s ease-out;
    }
    
    @keyframes inputGlow {
        from {
            box-shadow: 0 0 0 0 rgba(34, 197, 94, 0);
        }
        to {
            box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
        }
    }
    
    /* Hover lift animation for cards */
    .card {
        transition: all 0.4s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
    }
    
    .card:hover {
        transform: translateY(-8px) !important;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
    }
    
    /* Loading shimmer animation */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .shimmer-effect {
        background: linear-gradient(90deg, 
            rgba(255,255,255,0) 0%, 
            rgba(255,255,255,0.05) 50%, 
            rgba(255,255,255,0) 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    /* Pulse animation for DPE badge on load */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .dpe-badge-big {
        animation: pulse 0.5s ease-out;
    }
    
    /* Smooth scroll behavior */
    html {
        scroll-behavior: smooth;
    }
    
    /* Micro-interaction for radio buttons */
    .stRadio label {
        transition: all 0.2s cubic-bezier(0.2, 0.8, 0.4, 1) !important;
    }
    
    .stRadio label:active {
        transform: scale(0.95) !important;
    }
    
    /* Fade transition for sidebar */
    section[data-testid="stSidebar"] {
        animation: sidebarFadeIn 0.4s ease-out;
    }
    
    @keyframes sidebarFadeIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Number counter animation */
    .metric-value-huge {
        animation: countUp 0.8s ease-out;
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Progress bar animation */
    .stProgress > div > div > div > div {
        transition: width 0.5s ease-out !important;
    }
    
    /* Success message animation */
    .stAlert {
        animation: slideInRight 0.4s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Tooltip fade in */
    [data-testid="stTooltipHoverTarget"]:hover + div {
        animation: tooltipFade 0.2s ease-out;
    }
    
    @keyframes tooltipFade {
        from { opacity: 0; transform: translateY(-5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    
    <script>
    // Smooth page transition on link clicks
    document.addEventListener('DOMContentLoaded', function() {
        // Add loading class when any button is clicked
        const buttons = document.querySelectorAll('.stButton button');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                // Add loading effect
                this.style.opacity = '0.7';
                setTimeout(() => {
                    this.style.opacity = '1';
                }, 300);
            });
        });
        
        // Animate numbers when they come into view
        const observerOptions = {
            threshold: 0.3,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const numberObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        document.querySelectorAll('.metric-value-huge').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s ease-out';
            numberObserver.observe(el);
        });
    });
    </script>
    """
    st.markdown(transitions_html, unsafe_allow_html=True)


def add_loading_spinner():
    """Adds a custom loading spinner"""
    spinner_html = """
    <style>
    .custom-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid rgba(34, 197, 94, 0.1);
        border-top: 3px solid #22c55e;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """
    st.markdown(spinner_html, unsafe_allow_html=True)