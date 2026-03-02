"""
Generate Architecture Diagrams for SmartHomeAI Research Paper (Clean Version)
No emoji characters - uses text labels only for compatibility
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
import os

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

os.makedirs('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams', exist_ok=True)

def create_main_architecture():
    """Create the main 4-tier system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    colors = {
        'presentation': '#E3F2FD',
        'agentic': '#F3E5F5',
        'rl': '#FFF3E0',
        'environment': '#E8F5E9',
        'component': '#FFFFFF',
        'arrow': '#424242'
    }
    
    # Title
    ax.text(7, 11.5, 'SmartHomeAI: Hybrid System Architecture', fontsize=16, fontweight='bold', ha='center')
    
    # Layer 1: Presentation Layer
    layer1 = FancyBboxPatch((0.5, 9.2), 13, 2, boxstyle="round,pad=0.05", 
                            facecolor=colors['presentation'], edgecolor='#1976D2', linewidth=2)
    ax.add_patch(layer1)
    ax.text(7, 10.9, 'PRESENTATION LAYER', fontsize=12, fontweight='bold', ha='center', color='#1976D2')
    
    # Presentation components
    for i, (name, desc) in enumerate([('Streamlit\nDashboard', 'Web UI'), 
                                       ('Real-time\nVisualizations', 'Plotly Charts'),
                                       ('Natural Language\nChat Interface', 'User Input')]):
        x = 2 + i * 4
        box = FancyBboxPatch((x, 9.4), 3, 1.2, boxstyle="round,pad=0.03", 
                             facecolor=colors['component'], edgecolor='#1976D2', linewidth=1)
        ax.add_patch(box)
        ax.text(x + 1.5, 10.1, name, fontsize=9, ha='center', va='center', fontweight='bold')
        ax.text(x + 1.5, 9.6, desc, fontsize=7, ha='center', va='center', color='gray')
    
    # Arrow down
    ax.annotate('', xy=(7, 8.9), xytext=(7, 9.2), arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=2))
    
    # Layer 2: Agentic AI Layer
    layer2 = FancyBboxPatch((0.5, 5.8), 13, 3, boxstyle="round,pad=0.05", 
                            facecolor=colors['agentic'], edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(layer2)
    ax.text(7, 8.5, 'AGENTIC AI LAYER (LangGraph + Gemini)', fontsize=12, fontweight='bold', ha='center', color='#7B1FA2')
    
    # State machine flow
    nodes = ['Analyze\nEnvironment', 'Make\nRecommendation', 'Explain\nDecision', 'Output\nState']
    for i, name in enumerate(nodes):
        x = 1.5 + i * 3.2
        box = FancyBboxPatch((x, 7.2), 2.5, 1, boxstyle="round,pad=0.03", 
                             facecolor=colors['component'], edgecolor='#7B1FA2', linewidth=1)
        ax.add_patch(box)
        ax.text(x + 1.25, 7.7, name, fontsize=8, ha='center', va='center', fontweight='bold')
        if i < len(nodes) - 1:
            ax.annotate('', xy=(x + 2.7, 7.7), xytext=(x + 2.5, 7.7), 
                       arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=1.5))
    
    # Supporting components
    for i, (name, icon) in enumerate([('Gemini 2.0\nFlash LLM', 'AI'), 
                                       ('Persistent User\nMemory (JSON)', 'Storage'),
                                       ('Pattern Detection\nEngine', 'Analysis')]):
        x = 2 + i * 4
        box = FancyBboxPatch((x, 6), 3, 1, boxstyle="round,pad=0.03", 
                             facecolor=colors['component'], edgecolor='#7B1FA2', linewidth=1)
        ax.add_patch(box)
        ax.text(x + 1.5, 6.5, name, fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrow down
    ax.annotate('', xy=(7, 5.5), xytext=(7, 5.8), arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=2))
    
    # Layer 3: RL Layer
    layer3 = FancyBboxPatch((0.5, 3.2), 13, 2.2, boxstyle="round,pad=0.05", 
                            facecolor=colors['rl'], edgecolor='#F57C00', linewidth=2)
    ax.add_patch(layer3)
    ax.text(7, 5.1, 'REINFORCEMENT LEARNING LAYER (DQN)', fontsize=12, fontweight='bold', ha='center', color='#E65100')
    
    # RL components
    for i, (name, desc) in enumerate([('Policy Network\n(MLP)', '64-64 neurons'), 
                                       ('Target Network\n(MLP)', 'Stable targets'),
                                       ('Experience Replay\nBuffer', '20,000 transitions')]):
        x = 2 + i * 4
        box = FancyBboxPatch((x, 4), 3, 1, boxstyle="round,pad=0.03", 
                             facecolor=colors['component'], edgecolor='#F57C00', linewidth=1)
        ax.add_patch(box)
        ax.text(x + 1.5, 4.55, name, fontsize=8, ha='center', va='center', fontweight='bold')
        ax.text(x + 1.5, 4.15, desc, fontsize=7, ha='center', va='center', color='gray')
    
    # Action space
    ax.text(7, 3.5, 'Action Space: [Do Nothing | HVAC On | HVAC Off | Light Up | Light Down]', 
            fontsize=9, ha='center', style='italic')
    
    # Arrow down
    ax.annotate('', xy=(7, 2.9), xytext=(7, 3.2), arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=2))
    
    # Layer 4: Environment Layer
    layer4 = FancyBboxPatch((0.5, 0.3), 13, 2.5, boxstyle="round,pad=0.05", 
                            facecolor=colors['environment'], edgecolor='#388E3C', linewidth=2)
    ax.add_patch(layer4)
    ax.text(7, 2.5, 'ENVIRONMENT / SIMULATION LAYER (Gymnasium)', fontsize=12, fontweight='bold', ha='center', color='#2E7D32')
    
    # Environment components
    for i, (name, desc) in enumerate([('Temperature\nDynamics', 'Physics sim'), 
                                       ('Occupancy\nPatterns', 'Time-based'),
                                       ('Reward\nCalculator', 'Multi-objective')]):
        x = 2 + i * 4
        box = FancyBboxPatch((x, 1.4), 3, 0.9, boxstyle="round,pad=0.03", 
                             facecolor=colors['component'], edgecolor='#388E3C', linewidth=1)
        ax.add_patch(box)
        ax.text(x + 1.5, 1.95, name, fontsize=8, ha='center', va='center', fontweight='bold')
        ax.text(x + 1.5, 1.6, desc, fontsize=7, ha='center', va='center', color='gray')
    
    # Observation space
    ax.text(7, 0.7, 'Observation Space: [Temp, Humidity, Time, Comfort, HVAC, Light, Energy]', 
            fontsize=9, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/01_system_architecture.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: 01_system_architecture.png")


def create_data_flow():
    """Create Data Flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(6, 9.6, 'SmartHomeAI: Data Flow Architecture', fontsize=14, fontweight='bold', ha='center')
    
    # User
    circle = Circle((6, 8.5), 0.6, facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(circle)
    ax.text(6, 8.5, 'USER', fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Dashboard
    box = FancyBboxPatch((4, 6.8), 4, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 7.4, 'Streamlit Dashboard', fontsize=11, ha='center', fontweight='bold')
    
    ax.annotate('', xy=(6, 8), xytext=(6, 7.9), arrowprops=dict(arrowstyle='<->', color='#424242', lw=2))
    ax.text(6.5, 8.1, 'Interact', fontsize=8, color='gray')
    
    # Two paths from dashboard
    ax.annotate('', xy=(3.5, 6.5), xytext=(4.5, 6.8), arrowprops=dict(arrowstyle='->', color='#F57C00', lw=2))
    ax.text(3.2, 6.7, 'Manual\nOverride', fontsize=8, ha='center', color='#E65100')
    
    ax.annotate('', xy=(8.5, 6.5), xytext=(7.5, 6.8), arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))
    ax.text(8.8, 6.7, 'AI\nRequest', fontsize=8, ha='center', color='#7B1FA2')
    
    # Memory (left side)
    box = FancyBboxPatch((1, 5), 3, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box)
    ax.text(2.5, 5.6, 'User Memory', fontsize=10, ha='center', fontweight='bold')
    ax.text(2.5, 5.2, 'user_override_memory.json', fontsize=7, ha='center')
    
    # Agentic AI (right side)
    box = FancyBboxPatch((8, 5), 3, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(9.5, 5.6, 'Agentic AI', fontsize=10, ha='center', fontweight='bold')
    ax.text(9.5, 5.2, 'LangGraph + Gemini', fontsize=7, ha='center')
    
    # Connection between memory and AI
    ax.annotate('', xy=(8, 5.5), xytext=(4, 5.5), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.5, ls='--'))
    ax.text(6, 5.7, 'Load relevant overrides', fontsize=7, ha='center', color='gray')
    
    # DQN Agent (center)
    box = FancyBboxPatch((4, 3.2), 4, 1.4, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 4.1, 'DQN Agent', fontsize=11, ha='center', fontweight='bold')
    ax.text(6, 3.6, 'Policy Network -> Action Selection', fontsize=8, ha='center')
    
    # Arrows to DQN
    ax.annotate('', xy=(5, 4.6), xytext=(3, 5), arrowprops=dict(arrowstyle='->', color='#F57C00', lw=1.5))
    ax.annotate('', xy=(7, 4.6), xytext=(9, 5), arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=1.5))
    
    # Environment (bottom)
    box = FancyBboxPatch((3, 1), 6, 1.6, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 2.2, 'Smart Home Environment', fontsize=11, ha='center', fontweight='bold')
    ax.text(6, 1.7, 'Temperature | Humidity | Lighting | HVAC | Energy', fontsize=8, ha='center')
    ax.text(6, 1.3, 'Gymnasium Simulation', fontsize=7, ha='center', color='gray')
    
    # Bidirectional arrow between DQN and Environment
    ax.annotate('', xy=(5.5, 2.6), xytext=(5.5, 3.2), arrowprops=dict(arrowstyle='->', color='#388E3C', lw=2))
    ax.annotate('', xy=(6.5, 3.2), xytext=(6.5, 2.6), arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))
    ax.text(5, 2.9, 'Action', fontsize=7, color='#388E3C')
    ax.text(7, 2.9, 'Reward\n+ Obs', fontsize=7, color='#C62828', ha='center')
    
    # IoT Devices
    box = FancyBboxPatch((3, -0.5), 6, 1, boxstyle="round,pad=0.05", 
                         facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 0.1, 'IoT Devices (MQTT)', fontsize=10, ha='center', fontweight='bold')
    ax.text(6, -0.3, 'Sensors | HVAC | Lights | Fan', fontsize=8, ha='center')
    
    ax.annotate('', xy=(6, 0.5), xytext=(6, 1), arrowprops=dict(arrowstyle='<->', color='#607D8B', lw=1.5))
    
    # Legend
    legend_box = FancyBboxPatch((9.5, 1.5), 2.3, 2.5, boxstyle="round,pad=0.03", 
                                facecolor='#FAFAFA', edgecolor='gray', linewidth=1)
    ax.add_patch(legend_box)
    ax.text(10.65, 3.75, 'Data Flow', fontsize=9, ha='center', fontweight='bold')
    ax.plot([9.7, 10.3], [3.4, 3.4], color='#7B1FA2', lw=2)
    ax.text(10.5, 3.4, 'AI Path', fontsize=7, va='center')
    ax.plot([9.7, 10.3], [3.0, 3.0], color='#F57C00', lw=2)
    ax.text(10.5, 3.0, 'Override Path', fontsize=7, va='center')
    ax.plot([9.7, 10.3], [2.6, 2.6], color='#388E3C', lw=2)
    ax.text(10.5, 2.6, 'Control', fontsize=7, va='center')
    ax.plot([9.7, 10.3], [2.2, 2.2], color='#C62828', lw=2)
    ax.text(10.5, 2.2, 'Feedback', fontsize=7, va='center')
    ax.plot([9.7, 10.3], [1.8, 1.8], color='#9E9E9E', lw=1.5, ls='--')
    ax.text(10.5, 1.8, 'Memory', fontsize=7, va='center')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/04_data_flow.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: 04_data_flow.png")


def create_preference_learning():
    """Create User Preference Learning diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.6, 'Bidirectional User Preference Learning System', fontsize=14, fontweight='bold', ha='center')
    
    # Step 1: User Override
    box = FancyBboxPatch((0.5, 5), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(2, 6.6, '1. User Override', fontsize=10, ha='center', fontweight='bold', color='#1565C0')
    ax.text(2, 6, 'User clicks manual\ncontrol button', fontsize=8, ha='center')
    ax.text(2, 5.3, 'e.g., "Turn HVAC On"\nat 27C', fontsize=7, ha='center', style='italic')
    
    # Arrow
    ax.annotate('', xy=(3.8, 6), xytext=(3.5, 6), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 2: Context Capture
    box = FancyBboxPatch((4, 5), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box)
    ax.text(5.5, 6.6, '2. Context Capture', fontsize=10, ha='center', fontweight='bold', color='#E65100')
    ax.text(5.5, 5.9, 'Record environment:', fontsize=8, ha='center')
    ax.text(5.5, 5.5, '- Temperature: 27C\n- Time: 14:00\n- Humidity: 65%', fontsize=7, ha='center')
    
    # Arrow
    ax.annotate('', xy=(7.3, 6), xytext=(7, 6), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 3: Memory Storage
    box = FancyBboxPatch((7.5, 5), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(9, 6.6, '3. Memory Storage', fontsize=10, ha='center', fontweight='bold', color='#2E7D32')
    ax.text(9, 5.9, 'Save to JSON file', fontsize=8, ha='center')
    ax.text(9, 5.4, 'user_override_memory.json\n(Last 100 overrides)', fontsize=7, ha='center')
    
    # Arrow
    ax.annotate('', xy=(10.8, 6), xytext=(10.5, 6), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 4: Pattern Detection
    box = FancyBboxPatch((11, 5), 2.5, 2, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(12.25, 6.6, '4. Pattern\nDetection', fontsize=10, ha='center', fontweight='bold', color='#6A1B9A')
    ax.text(12.25, 5.5, '>=3 similar =\nConfident', fontsize=8, ha='center')
    
    # Lower row - Application
    # Step 5: Similar Situation
    box = FancyBboxPatch((0.5, 2), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=2)
    ax.add_patch(box)
    ax.text(2, 3.6, '5. Similar Situation', fontsize=10, ha='center', fontweight='bold', color='#455A64')
    ax.text(2, 3, 'New state detected:', fontsize=8, ha='center')
    ax.text(2, 2.5, 'Temp: 27.5C\n(within +/-3C)', fontsize=7, ha='center')
    
    # Arrow
    ax.annotate('', xy=(3.8, 3), xytext=(3.5, 3), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 6: Retrieve Memory
    box = FancyBboxPatch((4, 2), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(5.5, 3.6, '6. Retrieve Memory', fontsize=10, ha='center', fontweight='bold', color='#2E7D32')
    ax.text(5.5, 2.9, 'Find relevant overrides', fontsize=8, ha='center')
    ax.text(5.5, 2.5, '+/-3C temp, +/-3hr time', fontsize=7, ha='center')
    
    # Arrow
    ax.annotate('', xy=(7.3, 3), xytext=(7, 3), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 7: Contextualized Prompt
    box = FancyBboxPatch((7.5, 2), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(9, 3.6, '7. LLM Prompt', fontsize=10, ha='center', fontweight='bold', color='#1565C0')
    ax.text(9, 2.9, 'Include user history', fontsize=8, ha='center')
    ax.text(9, 2.5, '"User turned HVAC on\n5 times at ~27C"', fontsize=7, ha='center', style='italic')
    
    # Arrow
    ax.annotate('', xy=(10.8, 3), xytext=(10.5, 3), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 8: Personalized Recommendation
    box = FancyBboxPatch((11, 2), 2.5, 2, boxstyle="round,pad=0.05", 
                         facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(box)
    ax.text(12.25, 3.6, '8. Personalized\nRecommendation', fontsize=9, ha='center', fontweight='bold', color='#1B5E20')
    ax.text(12.25, 2.5, '"Turn HVAC On"\n+ Explanation', fontsize=8, ha='center')
    
    # Connecting arrows between rows
    ax.annotate('', xy=(12.25, 4.8), xytext=(12.25, 4.2), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.5, ls='--'))
    ax.annotate('', xy=(2, 4.8), xytext=(2, 4.2), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.5, ls='--'))
    
    # Feedback loop
    ax.annotate('', xy=(2, 5), xytext=(12.25, 4), 
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2, 
                               connectionstyle="arc3,rad=0.4"))
    ax.text(7, 4.6, 'Continuous Learning Loop', fontsize=9, ha='center', color='#C62828', fontweight='bold')
    
    # Confidence levels
    box = FancyBboxPatch((4.5, 0.3), 5, 1.2, boxstyle="round,pad=0.03", 
                         facecolor='#FAFAFA', edgecolor='gray', linewidth=1)
    ax.add_patch(box)
    ax.text(7, 1.25, 'Confidence Thresholds', fontsize=9, ha='center', fontweight='bold')
    ax.text(7, 0.85, '1-2 overrides: Learning  |  3-4: Emerging  |  5+: Confident (Auto-suggest)', fontsize=8, ha='center')
    ax.text(7, 0.5, '< 66%          66-99%          100%+', fontsize=8, ha='center')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/05_preference_learning.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: 05_preference_learning.png")


def create_comparison_diagram():
    """Create RL vs Agentic AI comparison diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.6, 'Hybrid Approach: RL + Agentic AI Synergy', fontsize=14, fontweight='bold', ha='center')
    
    # RL Only (left)
    box = FancyBboxPatch((0.5, 3.5), 4, 3.5, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box)
    ax.text(2.5, 6.7, 'RL Only', fontsize=12, ha='center', fontweight='bold', color='#E65100')
    ax.text(2.5, 6.1, '[+] Fast numerical optimization', fontsize=8, ha='center')
    ax.text(2.5, 5.7, '[+] Learns from environment', fontsize=8, ha='center')
    ax.text(2.5, 5.3, '[+] Energy-efficient control', fontsize=8, ha='center')
    ax.text(2.5, 4.7, '[-] No natural language', fontsize=8, ha='center', color='#C62828')
    ax.text(2.5, 4.3, '[-] No explainability', fontsize=8, ha='center', color='#C62828')
    ax.text(2.5, 3.9, '[-] Slow to user feedback', fontsize=8, ha='center', color='#C62828')
    
    # Agentic AI Only (right)
    box = FancyBboxPatch((9.5, 3.5), 4, 3.5, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(11.5, 6.7, 'Agentic AI Only', fontsize=12, ha='center', fontweight='bold', color='#6A1B9A')
    ax.text(11.5, 6.1, '[+] Natural language interface', fontsize=8, ha='center')
    ax.text(11.5, 5.7, '[+] Explainable decisions', fontsize=8, ha='center')
    ax.text(11.5, 5.3, '[+] Context understanding', fontsize=8, ha='center')
    ax.text(11.5, 4.7, '[-] No numerical optimization', fontsize=8, ha='center', color='#C62828')
    ax.text(11.5, 4.3, '[-] Higher latency (API calls)', fontsize=8, ha='center', color='#C62828')
    ax.text(11.5, 3.9, '[-] No learned policies', fontsize=8, ha='center', color='#C62828')
    
    # Combined (center)
    box = FancyBboxPatch((5, 1), 4, 5.5, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=3)
    ax.add_patch(box)
    ax.text(7, 6.2, 'SmartHomeAI\nHybrid System', fontsize=12, ha='center', fontweight='bold', color='#2E7D32')
    ax.text(7, 5.3, '[+] Fast RL-based control', fontsize=9, ha='center')
    ax.text(7, 4.9, '[+] Natural language interface', fontsize=9, ha='center')
    ax.text(7, 4.5, '[+] Explainable decisions', fontsize=9, ha='center')
    ax.text(7, 4.1, '[+] Learns from overrides', fontsize=9, ha='center')
    ax.text(7, 3.7, '[+] Energy optimization', fontsize=9, ha='center')
    ax.text(7, 3.3, '[+] Personalized experience', fontsize=9, ha='center')
    ax.text(7, 2.7, 'DQN: 2.3ms response\nGemini: Context + Explanation', fontsize=8, ha='center', style='italic')
    ax.text(7, 1.8, 'BEST OF BOTH WORLDS', fontsize=11, ha='center', fontweight='bold', color='#1B5E20')
    
    # Arrows
    ax.annotate('', xy=(5, 4.5), xytext=(4.5, 5.2), arrowprops=dict(arrowstyle='->', color='#F57C00', lw=2))
    ax.annotate('', xy=(9, 4.5), xytext=(9.5, 5.2), arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))
    
    ax.text(4.2, 4.3, 'Fast\nControl', fontsize=7, ha='center', color='#E65100')
    ax.text(9.8, 4.3, 'Smart\nInterface', fontsize=7, ha='center', color='#6A1B9A')
    
    # Performance comparison
    box = FancyBboxPatch((0.5, 0.3), 13, 1.8, boxstyle="round,pad=0.03", 
                         facecolor='#FAFAFA', edgecolor='gray', linewidth=1)
    ax.add_patch(box)
    ax.text(7, 1.85, 'Performance Comparison', fontsize=10, ha='center', fontweight='bold')
    ax.text(7, 1.4, 'Response Time: DQN 2.3ms + Gemini ~1.8s  |  Comfort Score: 0.72  |  Energy: 2.31 kWh', fontsize=8, ha='center')
    ax.text(7, 0.95, 'vs Rule-based: +23% reward  |  vs Energy-saver: +22% comfort  |  Preference adaptation: 3-5 overrides', fontsize=8, ha='center')
    ax.text(7, 0.55, 'A/B Testing: SmartHomeAI outperforms all baseline strategies', fontsize=8, ha='center', style='italic', color='#2E7D32')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/07_hybrid_comparison.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: 07_hybrid_comparison.png")


def create_observation_action_space():
    """Create Observation and Action Space diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(7, 5.6, 'DQN Observation and Action Space Design', fontsize=14, fontweight='bold', ha='center')
    
    # Observation Space (left)
    box = FancyBboxPatch((0.5, 0.5), 6, 4.5, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(3.5, 4.7, 'Observation Space (7D Vector)', fontsize=12, ha='center', fontweight='bold', color='#1565C0')
    
    obs_features = [
        ('Temperature', '15-35C', 'Normalized'),
        ('Humidity', '20-80%', 'Normalized'),
        ('Time of Day', '0-24h', 'Normalized'),
        ('Comfort Score', '0-1', 'Calculated'),
        ('HVAC Status', '0/1', 'Binary'),
        ('Light Level', '0-100%', 'Normalized'),
        ('Energy Usage', '0-10kWh', 'Cumulative')
    ]
    
    for i, (name, range_val, norm) in enumerate(obs_features):
        y = 4.1 - i * 0.5
        ax.text(1, y, f's[{i}]:', fontsize=9, fontweight='bold')
        ax.text(1.8, y, name, fontsize=9)
        ax.text(4.2, y, range_val, fontsize=8, color='gray')
        ax.text(5.5, y, norm, fontsize=7, color='#1976D2')
    
    ax.text(3.5, 0.8, 'Box(low=0, high=1, shape=(7,))', fontsize=8, ha='center', style='italic')
    
    # Action Space (right)
    box = FancyBboxPatch((7.5, 0.5), 6, 4.5, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(10.5, 4.7, 'Action Space (5 Discrete)', fontsize=12, ha='center', fontweight='bold', color='#2E7D32')
    
    actions = [
        ('a=0', 'Do Nothing', 'Maintain current state'),
        ('a=1', 'HVAC On', 'Activate heating/cooling'),
        ('a=2', 'HVAC Off', 'Deactivate HVAC'),
        ('a=3', 'Light Up', 'Increase brightness +10%'),
        ('a=4', 'Light Down', 'Decrease brightness -10%')
    ]
    
    for i, (action, name, desc) in enumerate(actions):
        y = 4.1 - i * 0.7
        ax.text(8, y, action, fontsize=9, fontweight='bold', color='#2E7D32')
        ax.text(9.2, y, name, fontsize=10, fontweight='bold')
        ax.text(11, y, desc, fontsize=8, color='gray')
    
    ax.text(10.5, 0.8, 'Discrete(5)', fontsize=8, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/08_obs_action_space.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: 08_obs_action_space.png")


def create_training_pipeline():
    """Create Training Pipeline diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(7, 5.6, 'DQN Training Pipeline', fontsize=14, fontweight='bold', ha='center')
    
    # Steps
    steps = [
        ('1. Data\nLoading', 'CSV Dataset\n43,200 samples', '#E3F2FD', '#1976D2'),
        ('2. Environment\nSetup', 'Gymnasium\nSmartHomeEnv', '#FFF3E0', '#F57C00'),
        ('3. Agent\nInitialization', 'DQN MLP\n64-64 layers', '#F3E5F5', '#7B1FA2'),
        ('4. Training\nLoop', '100K timesteps\nBatch=64', '#E8F5E9', '#388E3C'),
        ('5. Validation\n& Save', 'Evaluate + Save\n.zip model', '#FFEBEE', '#C62828')
    ]
    
    for i, (title, desc, fill, edge) in enumerate(steps):
        x = 0.5 + i * 2.7
        box = FancyBboxPatch((x, 2.5), 2.4, 2.5, boxstyle="round,pad=0.05", 
                             facecolor=fill, edgecolor=edge, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 1.2, 4.6, title, fontsize=10, ha='center', va='center', fontweight='bold', color=edge)
        ax.text(x + 1.2, 3.3, desc, fontsize=8, ha='center', va='center')
        
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + 2.6, 3.75), xytext=(x + 2.4, 3.75), 
                       arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Hyperparameters box
    box = FancyBboxPatch((2, 0.3), 10, 1.5, boxstyle="round,pad=0.03", 
                         facecolor='#FAFAFA', edgecolor='gray', linewidth=1)
    ax.add_patch(box)
    ax.text(7, 1.55, 'Training Hyperparameters', fontsize=10, ha='center', fontweight='bold')
    ax.text(7, 1.1, 'Learning Rate: 0.0005  |  Buffer Size: 20,000  |  Batch Size: 64  |  Gamma: 0.99', fontsize=9, ha='center')
    ax.text(7, 0.7, 'Exploration: 1.0 -> 0.05 (30% of training)  |  Target Update: 500 steps  |  Network: MLP 64-64', fontsize=8, ha='center')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/09_training_pipeline.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: 09_training_pipeline.png")


# Generate all diagrams
print("Generating architecture diagrams for research paper...\n")
create_main_architecture()
create_data_flow()
create_preference_learning()
create_comparison_diagram()
create_observation_action_space()
create_training_pipeline()

print("\nAll diagrams generated successfully!")
print("Location: d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/")
