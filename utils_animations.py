"""
utils_animations.py — ZAMI Premium Animations
Lottie animations for luxury feel
"""

import streamlit.components.v1 as components
import json
import requests


def add_lottie_animation(url, height=200, width="100%"):
    """
    Add premium Lottie animation to page
    
    Args:
        url: Lottie animation JSON URL
        height: Animation height in pixels
        width: Animation width (default: 100%)
    """
    animation_html = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player 
        src="{url}" 
        background="transparent" 
        speed="1" 
        style="width: {width}; height: {height}px;" 
        loop 
        autoplay>
    </lottie-player>
    """
    components.html(animation_html, height=height)


def add_hero_animation():
    """Premium hero section animation — property energy visualization"""
    url = "https://assets9.lottiefiles.com/packages/lf20_drxtv7ye.json"
    add_lottie_animation(url, height=180, width="80%")


def add_subsidy_animation():
    """Money/subsidy animation for financial section"""
    url = "https://assets7.lottiefiles.com/packages/lf20_qxyqt3ii.json"
    add_lottie_animation(url, height=150, width="60%")


def add_roi_animation():
    """Growth chart animation for ROI section"""
    url = "https://assets5.lottiefiles.com/packages/lf20_xyjvkxex.json"
    add_lottie_animation(url, height=150, width="60%")