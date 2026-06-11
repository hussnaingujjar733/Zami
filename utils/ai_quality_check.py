"""
AI Quality Check for Renovation Photos
Analyzes before/after photos for quality and work completion
"""

import os
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import json

def analyze_photo_quality(image_path):
    """Analyze a single photo for quality metrics"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"score": 50, "error": "Cannot read image"}
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Blur detection
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 100:
            blur_score = max(0, int(laplacian_var / 100 * 50))
        else:
            blur_score = min(100, int(laplacian_var / 500 * 100))
        
        # Brightness check
        brightness = np.mean(gray)
        if brightness < 50:
            brightness_score = 30
        elif brightness < 100:
            brightness_score = 60
        elif brightness < 200:
            brightness_score = 90
        else:
            brightness_score = 70
        
        # Overall score
        score = int((blur_score + brightness_score) / 2)
        
        return {
            "score": score,
            "is_blurry": blur_score < 50,
            "brightness": "good" if brightness_score > 70 else "poor",
            "message": "✅ Good quality" if score > 70 else "⚠️ Needs improvement"
        }
    except Exception as e:
        return {"score": 50, "error": str(e)}

def compare_before_after(before_path, after_path):
    """Compare before and after photos"""
    try:
        before = cv2.imread(before_path)
        after = cv2.imread(after_path)
        
        if before is None or after is None:
            return {"change_percentage": 0, "completed": False}
        
        # Resize to same dimensions
        before_resized = cv2.resize(before, (500, 500))
        after_resized = cv2.resize(after, (500, 500))
        
        # Convert to grayscale
        before_gray = cv2.cvtColor(before_resized, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after_resized, cv2.COLOR_BGR2GRAY)
        
        # Calculate difference
        diff = cv2.absdiff(before_gray, after_gray)
        change_pct = np.sum(diff > 30) / diff.size * 100
        
        return {
            "change_percentage": round(change_pct, 1),
            "completed": change_pct > 20,
            "message": "✅ Work detected" if change_pct > 20 else "⚠️ No significant changes"
        }
    except Exception as e:
        return {"change_percentage": 0, "completed": False, "error": str(e)}

def analyze_project_photos(project_id, before_photos, after_photos):
    """Complete analysis for a project"""
    results = {
        "project_id": project_id,
        "analyzed_at": datetime.now().isoformat(),
        "before_quality": [],
        "after_quality": [],
        "comparisons": [],
        "overall_score": 0,
        "final_verdict": "pending"
    }
    
    scores = []
    
    # Analyze before photos
    for path in before_photos:
        quality = analyze_photo_quality(path)
        results["before_quality"].append({"path": path, "score": quality["score"]})
        scores.append(quality["score"])
    
    # Analyze after photos
    for path in after_photos:
        quality = analyze_photo_quality(path)
        results["after_quality"].append({"path": path, "score": quality["score"]})
        scores.append(quality["score"])
    
    # Compare before/after
    min_len = min(len(before_photos), len(after_photos))
    for i in range(min_len):
        comparison = compare_before_after(before_photos[i], after_photos[i])
        results["comparisons"].append(comparison)
        scores.append(comparison["change_percentage"])
    
    # Overall score
    if scores:
        results["overall_score"] = int(sum(scores) / len(scores))
    
    # Verdict
    if results["overall_score"] >= 70:
        results["final_verdict"] = "approved"
        results["message"] = "✅ Work verified successfully!"
    elif results["overall_score"] >= 50:
        results["final_verdict"] = "manual_review"
        results["message"] = "⚠️ Needs manual verification"
    else:
        results["final_verdict"] = "rejected"
        results["message"] = "❌ Please retake photos"
    
    return results

def save_analysis(project_id, results):
    """Save analysis to file"""
    os.makedirs(f"uploads/projects/project_{project_id}", exist_ok=True)
    with open(f"uploads/projects/project_{project_id}/ai_report.json", "w") as f:
        json.dump(results, f, indent=2)
