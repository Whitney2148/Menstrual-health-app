import pandas as pd
import numpy as np
import networkx as nx
from sklearn.ensemble import RandomForestClassifier
import warnings
import os
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
# 1. KNOWLEDGE GRAPH CONSTRUCTION (Lightweight)
# ==============================

class MenstrualKnowledgeGraph:
    """Lightweight Knowledge Graph for menstrual health domain"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self._build_base_knowledge_graph()
    
    def _build_base_knowledge_graph(self):
        """Build the comprehensive knowledge graph"""
        print("🕸️ Building Menstrual Health Knowledge Graph...")
        
        # Node types and instances
        nodes = {
            'phase': ['follicular', 'ovulatory', 'luteal', 'menstrual'],
            'symptom': ['cramps', 'headache', 'fatigue', 'bloating', 'mood_swings'],
            'hygiene_product': ['pad', 'tampon', 'menstrual_cup', 'period_underwear'],
            'medication': ['ibuprofen', 'naproxen', 'paracetamol'],
            'lifestyle': ['exercise', 'nutrition', 'sleep', 'stress_management']
        }
        
        # Add nodes with attributes
        for node_type, node_list in nodes.items():
            for node in node_list:
                self.graph.add_node(node, type=node_type)
        
        # Define relationships (edges)
        relationships = [
            # Phase-symptom relationships
            ('follicular', 'high_energy', 'phase_characteristic'),
            ('ovulatory', 'fertile_mucus', 'phase_characteristic'),
            ('luteal', 'mood_swings', 'common_symptom'),
            ('luteal', 'bloating', 'common_symptom'),
            ('menstrual', 'cramps', 'common_symptom'),
            ('menstrual', 'fatigue', 'common_symptom'),
            
            # Symptom-medication relationships
            ('cramps', 'ibuprofen', 'indicated_for'),
            ('cramps', 'naproxen', 'indicated_for'),
            ('headache', 'paracetamol', 'indicated_for'),
            
            # Flow-hygiene relationships
            ('light_flow', 'pad', 'recommended_for'),
            ('light_flow', 'period_underwear', 'recommended_for'),
            ('moderate_flow', 'tampon', 'recommended_for'),
            ('heavy_flow', 'menstrual_cup', 'recommended_for'),
            
            # Lifestyle recommendations
            ('cramps', 'exercise', 'relieved_by'),
            ('bloating', 'nutrition', 'managed_by'),
            ('fatigue', 'sleep', 'improved_by'),
            ('mood_swings', 'stress_management', 'managed_by'),
        ]
        
        # Add edges
        for source, target, relationship in relationships:
            self.graph.add_edge(source, target, relationship=relationship, weight=1.0)
        
        print(f"✅ Knowledge Graph built: {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges")
    
    def query_recommendations(self, symptoms: list, current_phase: str, flow_intensity: str) -> dict:
        """Query the knowledge graph for personalized recommendations"""
        recommendations = {
            'medications': [],
            'hygiene_products': [],
            'lifestyle_tips': [],
            'phase_specific': [],
            'risk_alerts': [],
            'symptoms_identified': symptoms
        }
        
        # Query based on symptoms
        for symptom in symptoms:
            for _, target, data in self.graph.edges(symptom, data=True):
                if data['relationship'] == 'indicated_for':
                    if target not in recommendations['medications']:
                        recommendations['medications'].append(target)
            
            for _, target, data in self.graph.edges(symptom, data=True):
                if data['relationship'] in ['relieved_by', 'managed_by', 'improved_by']:
                    tip = f"For {symptom}: {data['relationship']} with {target}"
                    if tip not in recommendations['lifestyle_tips']:
                        recommendations['lifestyle_tips'].append(tip)
        
        # Query based on phase
        if current_phase and current_phase in self.graph.nodes:
            for _, target, data in self.graph.edges(current_phase, data=True):
                if data['relationship'] in ['phase_characteristic', 'common_symptom']:
                    insight = f"During {current_phase} phase: {target}"
                    if insight not in recommendations['phase_specific']:
                        recommendations['phase_specific'].append(insight)
        
        # Query based on flow intensity
        flow_node = f"{flow_intensity.lower()}_flow"
        if flow_node in self.graph.nodes:
            for _, target, data in self.graph.edges(flow_node, data=True):
                if data['relationship'] == 'recommended_for':
                    if target not in recommendations['hygiene_products']:
                        recommendations['hygiene_products'].append(target)
        
        # Add default recommendations if none found
        if not recommendations['medications'] and symptoms:
            recommendations['medications'] = ['ibuprofen', 'paracetamol']
        
        if not recommendations['hygiene_products']:
            recommendations['hygiene_products'] = ['pad', 'tampon']
        
        return recommendations

# ==============================
# 2. TEMPORAL PREDICTION MODULE (Lightweight)
# ==============================

class TemporalPredictor:
    """Predict menstrual cycle phases and onset"""
    
    def __init__(self):
        # Simple rule-based predictor for deployment
        pass
    
    def predict_phase(self, user_data):
        """Predict menstrual phase based on cycle day"""
        day_in_cycle = user_data.get('day_in_cycle', 15)
        
        if day_in_cycle <= 5:
            return "menstrual"
        elif day_in_cycle <= 13:
            return "follicular"
        elif day_in_cycle <= 15:
            return "ovulatory"
        else:
            return "luteal"
    
    def predict_onset(self, user_data):
        """Predict days until next period onset"""
        base_cycle = 28
        current_day = user_data.get('day_in_cycle', 15)
        days_until_onset = max(1, base_cycle - current_day)
        return days_until_onset

# ==============================
# 3. COMPLETE SYSTEM INTEGRATION (Lightweight)
# ==============================

class CompleteMenstrualHealthSystem:
    """Lightweight system for deployment"""
    
    def __init__(self):
        self.temporal_predictor = TemporalPredictor()
        self.knowledge_graph = MenstrualKnowledgeGraph()
    
    def analyze_user_comprehensive(self, user_data: dict) -> dict:
        """Comprehensive user analysis"""
        # Extract symptoms
        symptoms = []
        pain_level = user_data.get('pain_nrs', 0)
        if pain_level >= 3:
            symptoms.append('cramps')
        if user_data.get('headaches', 'Medium') in ['Medium', 'High', 'Very High']:
            symptoms.append('headache')
        if user_data.get('fatigue', 'Medium') in ['Medium', 'High', 'Very High']:
            symptoms.append('fatigue')
        if user_data.get('bloating', 'Medium') in ['Medium', 'High', 'Very High']:
            symptoms.append('bloating')
        
        current_phase = user_data.get('phase', '').lower()
        flow_intensity = user_data.get('flow_intensity', 'moderate').lower()
        
        # Query knowledge graph
        kg_recommendations = self.knowledge_graph.query_recommendations(
            symptoms, current_phase, flow_intensity
        )
        
        # Generate advice
        advice_parts = ["Based on your symptoms and menstrual phase, here are personalized recommendations:\n"]
        
        if kg_recommendations.get('medications'):
            advice_parts.append(f"💊 **Medication Options**: {', '.join(kg_recommendations['medications'])}")
        
        if kg_recommendations.get('hygiene_products'):
            advice_parts.append(f"🩸 **Hygiene Products**: {', '.join(kg_recommendations['hygiene_products'])}")
        
        if kg_recommendations.get('lifestyle_tips'):
            advice_parts.append(f"🏃 **Lifestyle Tips**:")
            for tip in kg_recommendations['lifestyle_tips'][:3]:
                advice_parts.append(f"   • {tip}")
        
        if kg_recommendations.get('phase_specific'):
            advice_parts.append(f"📅 **Phase Insights**:")
            for insight in kg_recommendations['phase_specific'][:2]:
                advice_parts.append(f"   • {insight}")
        
        if symptoms:
            advice_parts.append(f"🎯 **Symptoms Addressed**: {', '.join(symptoms)}")
        
        # Add predictions
        predicted_phase = self.temporal_predictor.predict_phase(user_data)
        predicted_onset = self.temporal_predictor.predict_onset(user_data)
        advice_parts.append(f"📊 **Cycle Predictions**:")
        advice_parts.append(f"   • Next period in approximately {predicted_onset} days")
        advice_parts.append(f"   • Likely entering {predicted_phase} phase soon")
        
        # Add general tips
        advice_parts.append("\n💡 **General Wellness Tips**:")
        advice_parts.append("   • Stay hydrated and maintain a balanced diet")
        advice_parts.append("   • Get 7-9 hours of quality sleep nightly")
        advice_parts.append("   • Gentle exercise can reduce symptoms")
        advice_parts.append("   • Track your cycle to understand patterns")
        
        full_advice = "\n".join(advice_parts)
        
        return {
            'advice': full_advice,
            'knowledge_graph_recommendations': kg_recommendations,
            'symptoms_identified': symptoms,
            'llm_used': False,
            'kg_used': True,
            'predictions': {
                'next_period_in_days': predicted_onset,
                'predicted_phase': predicted_phase
            }
        }

# ==============================
# 4. SIMPLIFIED SYSTEM FOR WEB APP
# ==============================

class WebMenstrualSystem:
    """Simplified wrapper for web application"""
    
    def __init__(self):
        self.system = CompleteMenstrualHealthSystem()
        self.loaded = False
    
    def load(self):
        """Load the system"""
        self.loaded = True
        print("✅ Lightweight Menstrual Health System loaded successfully!")
        return True
    
    def analyze(self, user_data):
        """Analyze user data"""
        if not self.loaded:
            return {"error": "System not loaded"}
        
        return self.system.analyze_user_comprehensive(user_data)