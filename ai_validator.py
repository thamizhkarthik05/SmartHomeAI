import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SmartHomeAIValidator:
    """
    Comprehensive validation framework for Smart Home AI
    """
    
    def __init__(self, model_path="smart_home_ai_brain.zip", data_file="SmartHome_Environment_v1.csv"):
        self.model = DQN.load(model_path)
        self.env = SmartHomeEnv(data_file=data_file)
        self.validation_results = {}
        
        # Define optimal ranges for validation
        self.optimal_ranges = {
            'temperature': (20, 24),      # Ideal temperature range
            'comfort': (0.6, 1.0),        # Good comfort range
            'energy': (0, 3.0),           # Reasonable energy usage
            'light_day': (300, 1000),     # Good lighting during day
            'light_night': (0, 100)       # Low lighting at night
        }
        
        # Action meanings for analysis
        self.action_names = {
            0: "Do Nothing",
            1: "Turn Fan ON", 
            2: "Turn Fan OFF",
            3: "Increase Light",
            4: "Decrease Light"
        }
    
    def run_validation_episode(self, episode_length=1440, start_step=0):
        """Run a complete validation episode and collect metrics"""
        obs, _ = self.env.reset()
        
        # Skip to start step
        for _ in range(start_step):
            if self.env.current_step < len(self.env.df) - 1:
                self.env.current_step += 1
        obs = self.env._get_obs()
        
        episode_data = []
        total_reward = 0
        
        for step in range(episode_length):
            if self.env.current_step >= len(self.env.df) - 1:
                break
                
            # Get AI action
            action, _ = self.model.predict(obs, deterministic=True)
            action = int(action)
            
            # Store pre-action state
            hour = (self.env.current_step // 60) % 24
            minute = self.env.current_step % 60
            
            episode_data.append({
                'step': step,
                'time': f"{hour:02d}:{minute:02d}",
                'hour': hour,
                'temperature': obs[0],
                'perceived_temp': obs[1], 
                'light': obs[2],
                'comfort': obs[3],
                'fan_state': obs[4],
                'light_percent': obs[5],
                'energy': obs[6],
                'action': action,
                'action_name': self.action_names[action]
            })
            
            # Execute action
            obs, reward, terminated, _, _ = self.env.step(action)
            episode_data[-1]['reward'] = reward
            total_reward += reward
            
            if terminated:
                break
        
        return pd.DataFrame(episode_data), total_reward
    
    def validate_comfort_optimization(self, df):
        """Validate if AI maintains good comfort levels"""
        comfort_scores = df['comfort'].values
        
        metrics = {
            'avg_comfort': np.mean(comfort_scores),
            'min_comfort': np.min(comfort_scores),
            'comfort_above_60': np.mean(comfort_scores >= 0.6) * 100,
            'comfort_above_80': np.mean(comfort_scores >= 0.8) * 100,
            'comfort_stability': 1 - np.std(comfort_scores)  # Lower std = more stable
        }
        
        # Grade comfort performance
        if metrics['avg_comfort'] >= 0.8:
            grade = "A+ Excellent"
        elif metrics['avg_comfort'] >= 0.7:
            grade = "A Good"
        elif metrics['avg_comfort'] >= 0.6:
            grade = "B Average"
        elif metrics['avg_comfort'] >= 0.5:
            grade = "C Below Average"
        else:
            grade = "F Poor"
            
        metrics['grade'] = grade
        return metrics
    
    def validate_energy_efficiency(self, df):
        """Validate energy usage patterns"""
        energy_scores = df['energy'].values
        
        metrics = {
            'avg_energy': np.mean(energy_scores),
            'max_energy': np.max(energy_scores),
            'energy_spikes': np.sum(energy_scores > 5.0),  # Count high usage periods
            'energy_efficiency': np.mean(df['comfort']) / (np.mean(energy_scores) + 0.1)  # Comfort per energy
        }
        
        # Grade energy efficiency
        if metrics['avg_energy'] <= 2.0:
            grade = "A+ Very Efficient"
        elif metrics['avg_energy'] <= 3.0:
            grade = "A Efficient"
        elif metrics['avg_energy'] <= 4.0:
            grade = "B Moderate"
        elif metrics['avg_energy'] <= 5.0:
            grade = "C Inefficient"
        else:
            grade = "F Very Inefficient"
            
        metrics['grade'] = grade
        return metrics
    
    def validate_temperature_control(self, df):
        """Validate temperature management"""
        temps = df['temperature'].values
        target_range = self.optimal_ranges['temperature']
        
        in_range = np.logical_and(temps >= target_range[0], temps <= target_range[1])
        
        metrics = {
            'avg_temperature': np.mean(temps),
            'temp_in_range': np.mean(in_range) * 100,
            'temp_variance': np.var(temps),
            'overheating_events': np.sum(temps > 26),
            'too_cold_events': np.sum(temps < 18)
        }
        
        # Analyze fan usage effectiveness
        fan_actions = df[df['action'].isin([1, 2])]  # Fan on/off actions
        if len(fan_actions) > 0:
            fan_temp_impact = []
            for idx in fan_actions.index:
                if idx + 5 < len(df):  # Check 5 steps later
                    temp_change = df.loc[idx + 5, 'temperature'] - df.loc[idx, 'temperature']
                    if df.loc[idx, 'action'] == 1:  # Fan turned on
                        fan_temp_impact.append(temp_change)
            
            if fan_temp_impact:
                metrics['fan_effectiveness'] = np.mean(fan_temp_impact)
            else:
                metrics['fan_effectiveness'] = 0
        else:
            metrics['fan_effectiveness'] = 0
            
        return metrics
    
    def validate_lighting_intelligence(self, df):
        """Validate lighting decisions based on time of day"""
        day_hours = df[df['hour'].between(6, 22)]  # 6 AM to 10 PM
        night_hours = df[~df['hour'].between(6, 22)]  # Night time
        
        metrics = {
            'day_avg_light': np.mean(day_hours['light']) if len(day_hours) > 0 else 0,
            'night_avg_light': np.mean(night_hours['light']) if len(night_hours) > 0 else 0,
            'appropriate_day_lighting': 0,
            'appropriate_night_lighting': 0
        }
        
        if len(day_hours) > 0:
            metrics['appropriate_day_lighting'] = np.mean(day_hours['light'] >= 300) * 100
            
        if len(night_hours) > 0:
            metrics['appropriate_night_lighting'] = np.mean(night_hours['light'] <= 200) * 100
            
        # Light adjustment intelligence
        light_actions = df[df['action'].isin([3, 4])]  # Light up/down actions
        metrics['light_adjustments'] = len(light_actions)
        
        return metrics
    
    def validate_action_intelligence(self, df):
        """Validate the intelligence of action choices"""
        action_counts = df['action'].value_counts()
        
        metrics = {
            'total_actions': len(df),
            'do_nothing_pct': (action_counts.get(0, 0) / len(df)) * 100,
            'fan_actions_pct': ((action_counts.get(1, 0) + action_counts.get(2, 0)) / len(df)) * 100,
            'light_actions_pct': ((action_counts.get(3, 0) + action_counts.get(4, 0)) / len(df)) * 100,
            'action_diversity': len(action_counts)  # How many different actions used
        }
        
        # Check if actions are contextually appropriate
        hot_periods = df[df['temperature'] > 24]
        cold_periods = df[df['temperature'] < 20]
        
        if len(hot_periods) > 0:
            fan_on_when_hot = np.sum(hot_periods['action'] == 1)  # Turn fan on when hot
            metrics['fan_on_when_hot_pct'] = (fan_on_when_hot / len(hot_periods)) * 100
        else:
            metrics['fan_on_when_hot_pct'] = 0
            
        if len(cold_periods) > 0:
            fan_off_when_cold = np.sum(cold_periods['action'] == 2)  # Turn fan off when cold
            metrics['fan_off_when_cold_pct'] = (fan_off_when_cold / len(cold_periods)) * 100
        else:
            metrics['fan_off_when_cold_pct'] = 0
            
        return metrics
    
    def compare_with_baseline(self, df):
        """Compare AI performance with simple baseline strategies"""
        # Baseline 1: Always do nothing
        baseline_1_reward = np.sum(df['comfort'] * 10 - df['energy'] * 2)
        
        # Baseline 2: Simple thermostat (fan on if temp > 23, off if temp < 21)
        baseline_2_actions = []
        baseline_2_reward = 0
        
        for _, row in df.iterrows():
            if row['temperature'] > 23:
                action = 1  # Fan on
                energy_penalty = 0.5  # Extra energy for fan
            elif row['temperature'] < 21:
                action = 2  # Fan off
                energy_penalty = 0
            else:
                action = 0  # Do nothing
                energy_penalty = 0
            
            baseline_2_actions.append(action)
            baseline_2_reward += row['comfort'] * 10 - (row['energy'] + energy_penalty) * 2
        
        ai_reward = np.sum(df['reward'])
        
        metrics = {
            'ai_reward': ai_reward,
            'baseline_1_reward': baseline_1_reward,
            'baseline_2_reward': baseline_2_reward,
            'improvement_over_baseline_1': ((ai_reward - baseline_1_reward) / abs(baseline_1_reward)) * 100,
            'improvement_over_baseline_2': ((ai_reward - baseline_2_reward) / abs(baseline_2_reward)) * 100
        }
        
        return metrics
    
    def run_comprehensive_validation(self, test_periods=None):
        """Run complete validation across different time periods"""
        if test_periods is None:
            test_periods = [
                {"name": "Morning Rush", "start": 420, "length": 180},     # 7 AM - 10 AM
                {"name": "Afternoon", "start": 720, "length": 240},        # 12 PM - 4 PM  
                {"name": "Evening", "start": 1080, "length": 240},         # 6 PM - 10 PM
                {"name": "Night", "start": 1320, "length": 180},           # 10 PM - 1 AM
                {"name": "Full Day", "start": 360, "length": 1440}         # 6 AM - 6 AM next day
            ]
        
        validation_results = {}
        
        print("🔍 Running Comprehensive AI Validation...")
        print("=" * 60)
        
        for period in test_periods:
            print(f"\n📋 Testing: {period['name']}")
            
            # Run validation episode
            df, total_reward = self.run_validation_episode(
                episode_length=period['length'], 
                start_step=period['start']
            )
            
            if len(df) == 0:
                print(f"❌ No data for {period['name']}")
                continue
            
            # Run all validation tests
            results = {
                'period_name': period['name'],
                'total_reward': total_reward,
                'episode_length': len(df),
                'comfort_metrics': self.validate_comfort_optimization(df),
                'energy_metrics': self.validate_energy_efficiency(df),
                'temperature_metrics': self.validate_temperature_control(df),
                'lighting_metrics': self.validate_lighting_intelligence(df),
                'action_metrics': self.validate_action_intelligence(df),
                'baseline_comparison': self.compare_with_baseline(df)
            }
            
            validation_results[period['name']] = results
            
            # Print summary for this period
            self.print_period_summary(results)
        
        # Generate overall report
        self.generate_validation_report(validation_results)
        return validation_results
    
    def print_period_summary(self, results):
        """Print summary for a validation period"""
        comfort = results['comfort_metrics']
        energy = results['energy_metrics']
        
        print(f"  🏠 Comfort: {comfort['avg_comfort']:.2f}/1.0 ({comfort['grade']})")
        print(f"  ⚡ Energy: {energy['avg_energy']:.2f} kW ({energy['grade']})")
        print(f"  💰 Total Reward: {results['total_reward']:.1f}")
        print(f"  📊 Steps: {results['episode_length']}")
    
    def generate_validation_report(self, results):
        """Generate comprehensive validation report"""
        print("\n" + "="*80)
        print("📊 SMART HOME AI VALIDATION REPORT")
        print("="*80)
        
        # Overall performance summary
        overall_scores = []
        for period_name, result in results.items():
            if period_name == "Full Day":
                continue  # Skip full day for average calculation
            comfort_score = result['comfort_metrics']['avg_comfort']
            energy_score = min(1.0, 3.0 / (result['energy_metrics']['avg_energy'] + 0.1))
            overall_scores.append((comfort_score + energy_score) / 2)
        
        if overall_scores:
            avg_performance = np.mean(overall_scores)
            print(f"\n🎯 OVERALL AI PERFORMANCE: {avg_performance:.2f}/1.0")
            
            if avg_performance >= 0.8:
                print("🏆 GRADE: A+ (Excellent Smart Home AI)")
            elif avg_performance >= 0.7:
                print("🥇 GRADE: A (Good Smart Home AI)")
            elif avg_performance >= 0.6:
                print("🥈 GRADE: B (Average Smart Home AI)")
            elif avg_performance >= 0.5:
                print("🥉 GRADE: C (Below Average)")
            else:
                print("❌ GRADE: F (Poor Performance)")
        
        # Detailed breakdown
        for period_name, result in results.items():
            print(f"\n{'─'*40}")
            print(f"📅 {period_name.upper()}")
            print(f"{'─'*40}")
            
            # Comfort analysis
            comfort = result['comfort_metrics']
            print(f"😊 COMFORT ANALYSIS:")
            print(f"   Average Comfort: {comfort['avg_comfort']:.3f}/1.0")
            print(f"   Comfort > 60%: {comfort['comfort_above_60']:.1f}% of time")
            print(f"   Comfort > 80%: {comfort['comfort_above_80']:.1f}% of time")
            print(f"   Grade: {comfort['grade']}")
            
            # Energy analysis  
            energy = result['energy_metrics']
            print(f"\n⚡ ENERGY ANALYSIS:")
            print(f"   Average Energy: {energy['avg_energy']:.2f} kW")
            print(f"   Energy Efficiency: {energy['energy_efficiency']:.2f}")
            print(f"   Grade: {energy['grade']}")
            
            # Action intelligence
            actions = result['action_metrics']
            print(f"\n🎮 ACTION INTELLIGENCE:")
            print(f"   Do Nothing: {actions['do_nothing_pct']:.1f}%")
            print(f"   Fan Control: {actions['fan_actions_pct']:.1f}%")
            print(f"   Light Control: {actions['light_actions_pct']:.1f}%")
            print(f"   Fan On When Hot: {actions['fan_on_when_hot_pct']:.1f}%")
            
            # Baseline comparison
            baseline = result['baseline_comparison']
            print(f"\n📈 PERFORMANCE vs BASELINES:")
            print(f"   AI Reward: {baseline['ai_reward']:.1f}")
            print(f"   vs Do Nothing: {baseline['improvement_over_baseline_1']:+.1f}%")
            print(f"   vs Simple Thermostat: {baseline['improvement_over_baseline_2']:+.1f}%")
        
        print(f"\n{'='*80}")
        print("✅ VALIDATION COMPLETE")
        print(f"📄 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
    
    def save_validation_report(self, results, filename=None):
        """Save validation results to JSON file"""
        if filename is None:
            filename = f"ai_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Deep convert all values
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {k: convert_numpy(v) if not isinstance(v, dict) 
                                   else {k2: convert_numpy(v2) for k2, v2 in v.items()} 
                                   for k, v in value.items()}
            else:
                json_results[key] = convert_numpy(value)
        
        with open(filename, 'w') as f:
            json.dump(json_results, f, indent=2, default=convert_numpy)
            
        print(f"💾 Validation report saved to: {filename}")
        return filename

# Main validation runner
def main():
    print("🤖 Smart Home AI Validation Framework")
    print("="*50)
    
    try:
        validator = SmartHomeAIValidator()
        results = validator.run_comprehensive_validation()
        validator.save_validation_report(results)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have:")
        print("   1. Trained the AI model (run train.py first)")
        print("   2. SmartHome_Environment_v1.csv data file")
    except Exception as e:
        print(f"❌ Validation error: {e}")

if __name__ == "__main__":
    main()