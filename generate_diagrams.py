"""
Generate Architecture Diagrams for SmartHomeAI Research Paper
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

def create_main_architecture():
    """Create the main 4-tier system architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Colors
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
    for i, (name, icon) in enumerate([('Gemini 2.0\nFlash LLM', '🤖'), 
                                       ('Persistent User\nMemory (JSON)', '💾'),
                                       ('Pattern Detection\nEngine', '🔍')]):
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
    print("✅ Created: 01_system_architecture.png")


def create_dqn_architecture():
    """Create DQN Agent Architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.6, 'Deep Q-Network (DQN) Agent Architecture', fontsize=14, fontweight='bold', ha='center')
    
    # Input: Observation
    box = FancyBboxPatch((0.5, 3), 2.5, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(1.75, 4.5, 'Observation\n(State)', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(1.75, 3.5, '7 features:\nTemp, Humidity,\nTime, Comfort,\nHVAC, Light, Energy', 
            fontsize=7, ha='center', va='center')
    
    # Arrow
    ax.annotate('', xy=(3.2, 4), xytext=(3, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Neural Network
    nn_box = FancyBboxPatch((3.5, 1.5), 5, 5, boxstyle="round,pad=0.05", 
                            facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(nn_box)
    ax.text(6, 6.2, 'Policy Network (MLP)', fontsize=11, ha='center', va='center', fontweight='bold', color='#E65100')
    
    # Input layer
    for i in range(7):
        circle = Circle((4.2, 5.5 - i*0.5), 0.15, facecolor='#1976D2', edgecolor='#0D47A1')
        ax.add_patch(circle)
    ax.text(4.2, 2.3, 'Input\n(7)', fontsize=8, ha='center')
    
    # Hidden layer 1
    for i in range(6):
        circle = Circle((5.5, 5.2 - i*0.55), 0.15, facecolor='#FF9800', edgecolor='#E65100')
        ax.add_patch(circle)
    ax.text(5.5, 2.3, 'Hidden 1\n(64)', fontsize=8, ha='center')
    
    # Hidden layer 2
    for i in range(6):
        circle = Circle((6.8, 5.2 - i*0.55), 0.15, facecolor='#FF9800', edgecolor='#E65100')
        ax.add_patch(circle)
    ax.text(6.8, 2.3, 'Hidden 2\n(64)', fontsize=8, ha='center')
    
    # Output layer
    for i in range(5):
        circle = Circle((8.1, 4.8 - i*0.6), 0.15, facecolor='#4CAF50', edgecolor='#2E7D32')
        ax.add_patch(circle)
    ax.text(8.1, 2.3, 'Output\n(5)', fontsize=8, ha='center')
    
    # Connect layers (simplified)
    for start_y in [5.5, 4.5, 3.5]:
        for end_y in [5.2, 4.1, 3.0]:
            ax.plot([4.35, 5.35], [start_y, end_y], 'gray', alpha=0.2, lw=0.5)
    
    # Arrow to output
    ax.annotate('', xy=(8.7, 4), xytext=(8.5, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Output: Q-Values
    box = FancyBboxPatch((9, 2.5), 2.5, 3, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(10.25, 5.1, 'Q-Values', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(10.25, 4.5, 'Q(s, a₀): Do Nothing', fontsize=8, ha='center')
    ax.text(10.25, 4.1, 'Q(s, a₁): HVAC On', fontsize=8, ha='center')
    ax.text(10.25, 3.7, 'Q(s, a₂): HVAC Off', fontsize=8, ha='center')
    ax.text(10.25, 3.3, 'Q(s, a₃): Light Up', fontsize=8, ha='center')
    ax.text(10.25, 2.9, 'Q(s, a₄): Light Down', fontsize=8, ha='center')
    
    # Action selection
    ax.annotate('', xy=(10.25, 2.2), xytext=(10.25, 2.5), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    box = FancyBboxPatch((9, 1.2), 2.5, 0.9, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(10.25, 1.65, 'argmax Q(s,a)', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Hyperparameters box
    box = FancyBboxPatch((0.3, 0.3), 4, 1.5, boxstyle="round,pad=0.03", 
                         facecolor='#FAFAFA', edgecolor='gray', linewidth=1)
    ax.add_patch(box)
    ax.text(2.3, 1.55, 'Hyperparameters', fontsize=9, ha='center', fontweight='bold')
    ax.text(2.3, 1.15, 'Learning Rate: 0.0005 | Buffer: 20,000', fontsize=7, ha='center')
    ax.text(2.3, 0.85, 'Batch Size: 64 | γ: 0.99', fontsize=7, ha='center')
    ax.text(2.3, 0.55, 'ε: 1.0 → 0.05 (30% exploration)', fontsize=7, ha='center')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/02_dqn_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created: 02_dqn_architecture.png")


def create_agentic_workflow():
    """Create Agentic AI LangGraph Workflow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(7, 7.6, 'Agentic AI Layer: LangGraph State Machine Workflow', fontsize=14, fontweight='bold', ha='center')
    
    # Input
    circle = Circle((1, 4), 0.5, facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(circle)
    ax.text(1, 4, 'START', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrow
    ax.annotate('', xy=(1.8, 4), xytext=(1.5, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Node 1: Analyze Environment
    box = FancyBboxPatch((2, 3), 2.5, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(3.25, 4.5, '1. Analyze\nEnvironment', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(3.25, 3.4, '• Read sensors\n• Load memory\n• Format context', fontsize=7, ha='center', va='center')
    
    # Arrow
    ax.annotate('', xy=(4.8, 4), xytext=(4.5, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Node 2: Make Recommendation
    box = FancyBboxPatch((5, 3), 2.5, 2, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box)
    ax.text(6.25, 4.5, '2. Make\nRecommendation', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(6.25, 3.4, '• Query Gemini\n• Consider patterns\n• Select action', fontsize=7, ha='center', va='center')
    
    # Arrow
    ax.annotate('', xy=(7.8, 4), xytext=(7.5, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Node 3: Explain Decision
    box = FancyBboxPatch((8, 3), 2.5, 2, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(9.25, 4.5, '3. Explain\nDecision', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(9.25, 3.4, '• Generate reason\n• Reference prefs\n• Natural language', fontsize=7, ha='center', va='center')
    
    # Arrow
    ax.annotate('', xy=(10.8, 4), xytext=(10.5, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Node 4: Output State
    box = FancyBboxPatch((11, 3), 2, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(12, 4.5, '4. Output\nState', fontsize=10, ha='center', va='center', fontweight='bold')
    ax.text(12, 3.4, '• Format result\n• Return to UI', fontsize=7, ha='center', va='center')
    
    # End
    circle = Circle((13.5, 4), 0.4, facecolor='#FFCDD2', edgecolor='#C62828', linewidth=2)
    ax.add_patch(circle)
    ax.text(13.5, 4, 'END', fontsize=8, ha='center', va='center', fontweight='bold')
    ax.annotate('', xy=(13.1, 4), xytext=(13, 4), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # State object
    box = FancyBboxPatch((4, 0.5), 6, 2), 
    state_box = FancyBboxPatch((4, 0.5), 6, 2, boxstyle="round,pad=0.05", 
                               facecolor='#FAFAFA', edgecolor='#616161', linewidth=2)
    ax.add_patch(state_box)
    ax.text(7, 2.2, 'AgentState (TypedDict)', fontsize=10, ha='center', fontweight='bold')
    ax.text(7, 1.6, 'current_state: dict    |    recommendation: str    |    reasoning: str', fontsize=8, ha='center')
    ax.text(7, 1.1, 'analysis: str    |    user_memory: list', fontsize=8, ha='center')
    ax.text(7, 0.7, 'State flows through all nodes, accumulating information', fontsize=7, ha='center', style='italic', color='gray')
    
    # Memory integration arrows
    ax.annotate('', xy=(3.25, 3), xytext=(5.5, 2.5), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1, ls='--'))
    ax.annotate('', xy=(6.25, 3), xytext=(6.5, 2.5), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1, ls='--'))
    ax.annotate('', xy=(9.25, 3), xytext=(7.5, 2.5), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1, ls='--'))
    
    # Gemini API box
    box = FancyBboxPatch((4.5, 5.5), 5, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#E8EAF6', edgecolor='#3F51B5', linewidth=2)
    ax.add_patch(box)
    ax.text(7, 6.3, '🤖 Google Gemini 2.0 Flash API', fontsize=10, ha='center', fontweight='bold')
    ax.text(7, 5.8, 'Natural Language Processing & Generation', fontsize=8, ha='center')
    
    # Arrows to Gemini
    ax.annotate('', xy=(5.5, 5.5), xytext=(3.25, 5), arrowprops=dict(arrowstyle='<->', color='#3F51B5', lw=1.5))
    ax.annotate('', xy=(7, 5.5), xytext=(6.25, 5), arrowprops=dict(arrowstyle='<->', color='#3F51B5', lw=1.5))
    ax.annotate('', xy=(8.5, 5.5), xytext=(9.25, 5), arrowprops=dict(arrowstyle='<->', color='#3F51B5', lw=1.5))
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/03_agentic_workflow.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created: 03_agentic_workflow.png")


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
    ax.text(6, 8.5, '👤\nUser', fontsize=9, ha='center', va='center')
    
    # Dashboard
    box = FancyBboxPatch((4, 6.8), 4, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 7.4, 'Streamlit Dashboard', fontsize=11, ha='center', fontweight='bold')
    
    ax.annotate('', xy=(6, 8), xytext=(6, 7.9), arrowprops=dict(arrowstyle='<->', color='#424242', lw=2))
    ax.text(6.5, 8.1, 'Interact', fontsize=8, color='gray')
    
    # Two paths from dashboard
    # Left: Manual Override
    ax.annotate('', xy=(3.5, 6.5), xytext=(4.5, 6.8), arrowprops=dict(arrowstyle='->', color='#F57C00', lw=2))
    ax.text(3.2, 6.7, 'Manual\nOverride', fontsize=8, ha='center', color='#E65100')
    
    # Right: AI Request
    ax.annotate('', xy=(8.5, 6.5), xytext=(7.5, 6.8), arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2))
    ax.text(8.8, 6.7, 'AI\nRequest', fontsize=8, ha='center', color='#7B1FA2')
    
    # Memory (left side)
    box = FancyBboxPatch((1, 5), 3, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box)
    ax.text(2.5, 5.6, '💾 User Memory', fontsize=10, ha='center', fontweight='bold')
    ax.text(2.5, 5.2, 'user_override_memory.json', fontsize=7, ha='center')
    
    # Agentic AI (right side)
    box = FancyBboxPatch((8, 5), 3, 1.2, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(9.5, 5.6, '🤖 Agentic AI', fontsize=10, ha='center', fontweight='bold')
    ax.text(9.5, 5.2, 'LangGraph + Gemini', fontsize=7, ha='center')
    
    # Connection between memory and AI
    ax.annotate('', xy=(8, 5.5), xytext=(4, 5.5), arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.5, ls='--'))
    ax.text(6, 5.7, 'Load relevant overrides', fontsize=7, ha='center', color='gray')
    
    # DQN Agent (center)
    box = FancyBboxPatch((4, 3.2), 4, 1.4, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#FF9800', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 4.1, '🧠 DQN Agent', fontsize=11, ha='center', fontweight='bold')
    ax.text(6, 3.6, 'Policy Network → Action Selection', fontsize=8, ha='center')
    
    # Arrows to DQN
    ax.annotate('', xy=(5, 4.6), xytext=(3, 5), arrowprops=dict(arrowstyle='->', color='#F57C00', lw=1.5))
    ax.annotate('', xy=(7, 4.6), xytext=(9, 5), arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=1.5))
    
    # Environment (bottom)
    box = FancyBboxPatch((3, 1), 6, 1.6, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(6, 2.2, '🏠 Smart Home Environment', fontsize=11, ha='center', fontweight='bold')
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
    ax.text(6, 0.1, '📡 IoT Devices (MQTT)', fontsize=10, ha='center', fontweight='bold')
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
    print("✅ Created: 04_data_flow.png")


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
    ax.text(2, 5.3, 'e.g., "Turn HVAC On"\nat 27°C', fontsize=7, ha='center', style='italic')
    
    # Arrow
    ax.annotate('', xy=(3.8, 6), xytext=(3.5, 6), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 2: Context Capture
    box = FancyBboxPatch((4, 5), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(box)
    ax.text(5.5, 6.6, '2. Context Capture', fontsize=10, ha='center', fontweight='bold', color='#E65100')
    ax.text(5.5, 5.9, 'Record environment:', fontsize=8, ha='center')
    ax.text(5.5, 5.5, '• Temperature: 27°C\n• Time: 14:00\n• Humidity: 65%', fontsize=7, ha='center')
    
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
    ax.text(12.25, 5.5, '≥3 similar =\nConfident', fontsize=8, ha='center')
    
    # Lower row - Application
    # Step 5: Similar Situation
    box = FancyBboxPatch((0.5, 2), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=2)
    ax.add_patch(box)
    ax.text(2, 3.6, '5. Similar Situation', fontsize=10, ha='center', fontweight='bold', color='#455A64')
    ax.text(2, 3, 'New state detected:', fontsize=8, ha='center')
    ax.text(2, 2.5, 'Temp: 27.5°C\n(within ±3°C)', fontsize=7, ha='center')
    
    # Arrow
    ax.annotate('', xy=(3.8, 3), xytext=(3.5, 3), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 6: Retrieve Memory
    box = FancyBboxPatch((4, 2), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(box)
    ax.text(5.5, 3.6, '6. Retrieve Memory', fontsize=10, ha='center', fontweight='bold', color='#2E7D32')
    ax.text(5.5, 2.9, 'Find relevant overrides', fontsize=8, ha='center')
    ax.text(5.5, 2.5, '±3°C temp, ±3hr time', fontsize=7, ha='center')
    
    # Arrow
    ax.annotate('', xy=(7.3, 3), xytext=(7, 3), arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    
    # Step 7: Contextualized Prompt
    box = FancyBboxPatch((7.5, 2), 3, 2, boxstyle="round,pad=0.05", 
                         facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(box)
    ax.text(9, 3.6, '7. LLM Prompt', fontsize=10, ha='center', fontweight='bold', color='#1565C0')
    ax.text(9, 2.9, 'Include user history', fontsize=8, ha='center')
    ax.text(9, 2.5, '"User turned HVAC on\n5 times at ~27°C"', fontsize=7, ha='center', style='italic')
    
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
    ax.text(7, 0.5, '💫 < 66%          ⭐ 66-99%          🔥 100%+', fontsize=8, ha='center')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/05_preference_learning.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created: 05_preference_learning.png")


def create_reward_function():
    """Create Reward Function diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(6, 5.6, 'Multi-Objective Reward Function', fontsize=14, fontweight='bold', ha='center')
    
    # Main equation
    ax.text(6, 4.8, r'$R = 10 \times comfort - 2 \times energy - 20 \times override - 0.5 \times action$', 
            fontsize=14, ha='center', fontfamily='serif')
    
    # Components
    components = [
        ('Comfort Score', '+10×', '#4CAF50', 'Maximize user comfort\n(0 to 1 scale)'),
        ('Energy Usage', '-2×', '#FF9800', 'Minimize power consumption\n(kWh)'),
        ('User Override', '-20×', '#F44336', 'Heavy penalty when user\nmanually corrects'),
        ('Action Penalty', '-0.5', '#9E9E9E', 'Small cost for device\nstate changes')
    ]
    
    for i, (name, weight, color, desc) in enumerate(components):
        x = 0.8 + i * 2.8
        box = FancyBboxPatch((x, 2.2), 2.5, 2, boxstyle="round,pad=0.05", 
                             facecolor=color + '22', edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x + 1.25, 3.8, name, fontsize=10, ha='center', fontweight='bold', color=color)
        ax.text(x + 1.25, 3.3, weight, fontsize=16, ha='center', fontweight='bold', color=color)
        ax.text(x + 1.25, 2.6, desc, fontsize=7, ha='center', va='center')
    
    # Balance indication
    ax.text(6, 1.2, 'Balance: High comfort (×10 weight) vs Energy efficiency (×2) vs Respecting user preferences (×20)', 
            fontsize=9, ha='center', style='italic')
    
    # Outcome examples
    ax.text(6, 0.6, 'Example: Comfort=0.8, Energy=2kWh, No override → R = 8.0 - 4.0 - 0 = +4.0 (Good decision)', 
            fontsize=8, ha='center', color='gray')
    
    plt.tight_layout()
    plt.savefig('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/06_reward_function.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Created: 06_reward_function.png")


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
    ax.text(2.5, 6.1, '✅ Fast numerical optimization', fontsize=8, ha='center')
    ax.text(2.5, 5.7, '✅ Learns from environment', fontsize=8, ha='center')
    ax.text(2.5, 5.3, '✅ Energy-efficient control', fontsize=8, ha='center')
    ax.text(2.5, 4.7, '❌ No natural language', fontsize=8, ha='center', color='#C62828')
    ax.text(2.5, 4.3, '❌ No explainability', fontsize=8, ha='center', color='#C62828')
    ax.text(2.5, 3.9, '❌ Slow to user feedback', fontsize=8, ha='center', color='#C62828')
    
    # Agentic AI Only (right)
    box = FancyBboxPatch((9.5, 3.5), 4, 3.5, boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(box)
    ax.text(11.5, 6.7, 'Agentic AI Only', fontsize=12, ha='center', fontweight='bold', color='#6A1B9A')
    ax.text(11.5, 6.1, '✅ Natural language interface', fontsize=8, ha='center')
    ax.text(11.5, 5.7, '✅ Explainable decisions', fontsize=8, ha='center')
    ax.text(11.5, 5.3, '✅ Context understanding', fontsize=8, ha='center')
    ax.text(11.5, 4.7, '❌ No numerical optimization', fontsize=8, ha='center', color='#C62828')
    ax.text(11.5, 4.3, '❌ Higher latency (API calls)', fontsize=8, ha='center', color='#C62828')
    ax.text(11.5, 3.9, '❌ No learned policies', fontsize=8, ha='center', color='#C62828')
    
    # Combined (center)
    box = FancyBboxPatch((5, 1), 4, 5.5, boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=3)
    ax.add_patch(box)
    ax.text(7, 6.2, 'SmartHomeAI\nHybrid System', fontsize=12, ha='center', fontweight='bold', color='#2E7D32')
    ax.text(7, 5.3, '✅ Fast RL-based control', fontsize=9, ha='center')
    ax.text(7, 4.9, '✅ Natural language interface', fontsize=9, ha='center')
    ax.text(7, 4.5, '✅ Explainable decisions', fontsize=9, ha='center')
    ax.text(7, 4.1, '✅ Learns from overrides', fontsize=9, ha='center')
    ax.text(7, 3.7, '✅ Energy optimization', fontsize=9, ha='center')
    ax.text(7, 3.3, '✅ Personalized experience', fontsize=9, ha='center')
    ax.text(7, 2.7, 'DQN: 2.3ms response\nGemini: Context + Explanation', fontsize=8, ha='center', style='italic')
    ax.text(7, 1.8, '🏆 Best of Both Worlds', fontsize=11, ha='center', fontweight='bold', color='#1B5E20')
    
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
    print("✅ Created: 07_hybrid_comparison.png")


# Create diagrams directory
import os
os.makedirs('d:/SmartHomeAI-main/SmartHomeAI-main/diagrams', exist_ok=True)

# Generate all diagrams
print("🎨 Generating architecture diagrams for research paper...\n")
create_main_architecture()
create_dqn_architecture()
create_agentic_workflow()
create_data_flow()
create_preference_learning()
create_reward_function()
create_comparison_diagram()

print("\n✅ All diagrams generated successfully!")
print("📁 Location: d:/SmartHomeAI-main/SmartHomeAI-main/diagrams/")
