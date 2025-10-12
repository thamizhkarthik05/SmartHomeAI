import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import random
from scipy import stats

class ABTestFramework:
    """
    A/B testing framework to compare AI performance against different strategies
    """
    
    def __init__(self, data_file="SmartHome_Environment_v1.csv"):
        self.data_file = data_file
        self.test_results = {}
    
    def run_ai_strategy(self, model_path, test_episodes=5, episode_length=288):
        """Run AI strategy"""
        model = DQN.load(model_path)
        env = SmartHomeEnv(data_file=self.data_file)
        
        results = []
        
        for episode in range(test_episodes):
            obs, _ = env.reset()
            # Start at different times for variety
            start_step = random.randint(360, 1200)  # 6 AM to 8 PM
            for _ in range(start_step):
                if env.current_step < len(env.df) - 1:
                    env.current_step += 1
            obs = env._get_obs()
            
            episode_data = {
                'rewards': [],
                'comfort_scores': [],
                'energy_usage': [],
                'temperatures': [],
                'actions': []
            }
            
            for step in range(episode_length):
                action, _ = model.predict(obs, deterministic=True)
                action = int(action)
                
                episode_data['comfort_scores'].append(obs[3])
                episode_data['energy_usage'].append(obs[6])
                episode_data['temperatures'].append(obs[0])
                episode_data['actions'].append(action)
                
                obs, reward, terminated, _, _ = env.step(action)
                episode_data['rewards'].append(reward)
                
                if terminated:
                    break
            
            results.append({
                'episode': episode,
                'total_reward': sum(episode_data['rewards']),
                'avg_comfort': np.mean(episode_data['comfort_scores']),
                'avg_energy': np.mean(episode_data['energy_usage']),
                'avg_temperature': np.mean(episode_data['temperatures']),
                'actions_taken': len([a for a in episode_data['actions'] if a != 0])
            })
        
        return results
    
    def run_baseline_strategy(self, strategy_name, test_episodes=5, episode_length=288):
        """Run baseline strategies for comparison"""
        env = SmartHomeEnv(data_file=self.data_file)
        results = []
        
        for episode in range(test_episodes):
            obs, _ = env.reset()
            start_step = random.randint(360, 1200)
            for _ in range(start_step):
                if env.current_step < len(env.df) - 1:
                    env.current_step += 1
            obs = env._get_obs()
            
            episode_data = {
                'rewards': [],
                'comfort_scores': [],
                'energy_usage': [],
                'temperatures': [],
                'actions': []
            }
            
            for step in range(episode_length):
                # Different baseline strategies
                if strategy_name == "do_nothing":
                    action = 0
                elif strategy_name == "simple_thermostat":
                    temp = obs[0]
                    if temp > 24:
                        action = 1  # Turn fan on
                    elif temp < 20:
                        action = 2  # Turn fan off
                    else:
                        action = 0
                elif strategy_name == "aggressive_comfort":
                    # Always try to maximize comfort
                    temp = obs[0]
                    light = obs[2]
                    if temp > 22:
                        action = 1  # Fan on
                    elif temp < 21:
                        action = 2  # Fan off
                    elif light < 400:
                        action = 3  # Increase light
                    else:
                        action = 0
                elif strategy_name == "energy_saver":
                    # Minimize energy usage
                    if obs[6] > 2.0:  # If energy usage is high
                        if obs[4] == 1:  # If fan is on
                            action = 2  # Turn fan off
                        elif obs[5] > 50:  # If lights are bright
                            action = 4  # Decrease light
                        else:
                            action = 0
                    else:
                        action = 0
                elif strategy_name == "random":
                    action = random.randint(0, 4)
                else:
                    action = 0
                
                episode_data['comfort_scores'].append(obs[3])
                episode_data['energy_usage'].append(obs[6])
                episode_data['temperatures'].append(obs[0])
                episode_data['actions'].append(action)
                
                obs, reward, terminated, _, _ = env.step(action)
                episode_data['rewards'].append(reward)
                
                if terminated:
                    break
            
            results.append({
                'episode': episode,
                'total_reward': sum(episode_data['rewards']),
                'avg_comfort': np.mean(episode_data['comfort_scores']),
                'avg_energy': np.mean(episode_data['energy_usage']),
                'avg_temperature': np.mean(episode_data['temperatures']),
                'actions_taken': len([a for a in episode_data['actions'] if a != 0])
            })
        
        return results
    
    def statistical_significance_test(self, group_a, group_b, metric='total_reward'):
        """Perform statistical significance test between two groups"""
        values_a = [result[metric] for result in group_a]
        values_b = [result[metric] for result in group_b]
        
        # Perform t-test
        t_stat, p_value = stats.ttest_ind(values_a, values_b)
        
        # Calculate effect size (Cohen's d)
        pooled_std = np.sqrt(((np.std(values_a, ddof=1) ** 2) + (np.std(values_b, ddof=1) ** 2)) / 2)
        cohens_d = (np.mean(values_a) - np.mean(values_b)) / pooled_std
        
        return {
            't_statistic': t_stat,
            'p_value': p_value,
            'is_significant': p_value < 0.05,
            'cohens_d': cohens_d,
            'effect_size': 'small' if abs(cohens_d) < 0.5 else 'medium' if abs(cohens_d) < 0.8 else 'large'
        }
    
    def run_comprehensive_ab_test(self, model_path="smart_home_ai_brain.zip"):
        """Run comprehensive A/B test comparing AI against multiple baselines"""
        print("🧪 Running Comprehensive A/B Test")
        print("=" * 50)
        
        # Define test strategies
        strategies = {
            "AI Agent": "ai",
            "Do Nothing": "do_nothing", 
            "Simple Thermostat": "simple_thermostat",
            "Aggressive Comfort": "aggressive_comfort",
            "Energy Saver": "energy_saver",
            "Random Actions": "random"
        }
        
        all_results = {}
        
        # Run AI strategy
        print("🤖 Testing AI Agent...")
        try:
            ai_results = self.run_ai_strategy(model_path, test_episodes=10)
            all_results["AI Agent"] = ai_results
        except Exception as e:
            print(f"❌ Error testing AI: {e}")
            return
        
        # Run baseline strategies
        for strategy_name, strategy_key in strategies.items():
            if strategy_key == "ai":
                continue
            
            print(f"⚙️ Testing {strategy_name}...")
            baseline_results = self.run_baseline_strategy(strategy_key, test_episodes=10)
            all_results[strategy_name] = baseline_results
        
        # Analyze results
        self.analyze_ab_test_results(all_results)
        return all_results
    
    def analyze_ab_test_results(self, results):
        """Analyze and present A/B test results"""
        print("\n" + "=" * 60)
        print("📊 A/B TEST RESULTS ANALYSIS")
        print("=" * 60)
        
        # Calculate summary statistics for each strategy
        summary_stats = {}
        for strategy_name, strategy_results in results.items():
            stats_dict = {}
            for metric in ['total_reward', 'avg_comfort', 'avg_energy', 'avg_temperature', 'actions_taken']:
                values = [result[metric] for result in strategy_results]
                stats_dict[metric] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values)
                }
            summary_stats[strategy_name] = stats_dict
        
        # Display performance comparison table
        print("\n📈 PERFORMANCE COMPARISON")
        print("-" * 80)
        print(f"{'Strategy':<18} {'Reward':<12} {'Comfort':<10} {'Energy':<10} {'Actions':<8}")
        print("-" * 80)
        
        ai_reward = summary_stats["AI Agent"]["total_reward"]["mean"]
        
        for strategy_name, stats in summary_stats.items():
            reward = stats["total_reward"]["mean"]
            improvement = ((reward - ai_reward) / abs(ai_reward)) * 100 if strategy_name != "AI Agent" else 0
            
            print(f"{strategy_name:<18} "
                  f"{reward:>8.1f} ({improvement:+5.1f}%) "
                  f"{stats['avg_comfort']['mean']:>6.3f} "
                  f"{stats['avg_energy']['mean']:>6.2f} "
                  f"{stats['actions_taken']['mean']:>6.1f}")
        
        # Statistical significance tests
        print("\n🔬 STATISTICAL SIGNIFICANCE TESTS")
        print("-" * 60)
        
        ai_results = results["AI Agent"]
        
        for strategy_name, strategy_results in results.items():
            if strategy_name == "AI Agent":
                continue
            
            # Test multiple metrics
            for metric in ['total_reward', 'avg_comfort', 'avg_energy']:
                sig_test = self.statistical_significance_test(ai_results, strategy_results, metric)
                
                significance = "✅ SIGNIFICANT" if sig_test['is_significant'] else "❌ Not Significant"
                effect = sig_test['effect_size'].upper()
                
                print(f"{strategy_name} vs AI ({metric}):")
                print(f"  p-value: {sig_test['p_value']:.4f} | {significance}")
                print(f"  Effect size: {sig_test['cohens_d']:.3f} ({effect})")
                print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS")
        print("-" * 40)
        
        ai_stats = summary_stats["AI Agent"]
        best_comfort = max(summary_stats.items(), key=lambda x: x[1]['avg_comfort']['mean'])
        best_energy = min(summary_stats.items(), key=lambda x: x[1]['avg_energy']['mean'])
        best_reward = max(summary_stats.items(), key=lambda x: x[1]['total_reward']['mean'])
        
        print(f"🏆 Best Overall Performance: {best_reward[0]}")
        print(f"😊 Best Comfort: {best_comfort[0]} ({best_comfort[1]['avg_comfort']['mean']:.3f})")
        print(f"⚡ Most Energy Efficient: {best_energy[0]} ({best_energy[1]['avg_energy']['mean']:.2f} kW)")
        
        # AI Performance Assessment
        ai_rank_reward = sorted(summary_stats.items(), key=lambda x: x[1]['total_reward']['mean'], reverse=True)
        ai_position = next(i for i, (name, _) in enumerate(ai_rank_reward) if name == "AI Agent") + 1
        
        print(f"\n🤖 AI AGENT ASSESSMENT:")
        print(f"   Overall Rank: #{ai_position} out of {len(results)} strategies")
        
        if ai_position == 1:
            print("   Grade: A+ (Best performer)")
        elif ai_position == 2:
            print("   Grade: A (Very good performer)")
        elif ai_position <= len(results) // 2:
            print("   Grade: B (Above average)")
        else:
            print("   Grade: C (Below average - needs improvement)")
        
        # Specific recommendations
        if ai_stats['avg_energy']['mean'] > 3.0:
            print("   ⚠️ Recommendation: Focus on energy efficiency")
        if ai_stats['avg_comfort']['mean'] < 0.7:
            print("   ⚠️ Recommendation: Improve comfort optimization")
        if ai_stats['actions_taken']['mean'] > 50:
            print("   ⚠️ Recommendation: Reduce unnecessary actions")
    
    def generate_ab_test_report(self, results, filename=None):
        """Generate detailed A/B test report"""
        if filename is None:
            filename = f"ab_test_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        # Create comprehensive HTML report
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Smart Home AI A/B Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
                .metric { margin: 10px 0; padding: 10px; border-left: 4px solid #007acc; }
                .significant { color: green; font-weight: bold; }
                .not-significant { color: red; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
        """
        
        html_content += f"""
        <div class="header">
            <h1>🧪 Smart Home AI A/B Test Report</h1>
            <p>Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Test Episodes per Strategy: 10</p>
        </div>
        """
        
        # Add performance table
        html_content += "<h2>📊 Performance Comparison</h2><table>"
        html_content += "<tr><th>Strategy</th><th>Avg Reward</th><th>Avg Comfort</th><th>Avg Energy</th><th>Actions Taken</th></tr>"
        
        for strategy_name, strategy_results in results.items():
            avg_reward = np.mean([r['total_reward'] for r in strategy_results])
            avg_comfort = np.mean([r['avg_comfort'] for r in strategy_results])
            avg_energy = np.mean([r['avg_energy'] for r in strategy_results])
            avg_actions = np.mean([r['actions_taken'] for r in strategy_results])
            
            html_content += f"<tr><td>{strategy_name}</td><td>{avg_reward:.1f}</td><td>{avg_comfort:.3f}</td><td>{avg_energy:.2f}</td><td>{avg_actions:.1f}</td></tr>"
        
        html_content += "</table></body></html>"
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"📄 A/B Test report saved to: {filename}")
        return filename

# Main execution
def main():
    print("🧪 Smart Home AI A/B Testing Framework")
    print("=" * 50)
    
    ab_tester = ABTestFramework()
    
    try:
        results = ab_tester.run_comprehensive_ab_test()
        ab_tester.generate_ab_test_report(results)
        
    except Exception as e:
        print(f"❌ A/B Testing error: {e}")
        print("💡 Make sure you have:")
        print("   1. Trained AI model (smart_home_ai_brain.zip)")
        print("   2. Environment data (SmartHome_Environment_v1.csv)")

if __name__ == "__main__":
    main()