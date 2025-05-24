import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class MultiArmedBanditNavigation:
    def __init__(self):
        # Membuat grid 6x6
        self.grid_size = 6
        
        # Mendefinisikan block obstacle
        self.blocked = [(0,0), (0,5), (1,3), (1,5), (2,0), (2,5), 
                       (3,1), (3,3), (4,1), (4,3), (4,4), (5,4)]
        
        # Mendefinisikan posisi start dan posisi goal
        self.start_positions = [(0,1), (0,2), (0,3), (0,4)]
        self.goal = (4,5)
        
        # Mendefinisikan posisi awal agent pada start pertama
        self.agent_x = 0
        self.agent_y = 1
        
        # Mendefinisikan gerakan yang dapat dilakukan
        self.moves = [(0,1), (1,0), (0,-1), (-1,0)]
        self.move_names = ['Kanan', 'Bawah', 'Kiri', 'Atas']
        
        # Mendifinisikan nilai untuk setiap aksi pada setiap posisi
        self.action_values = {}
        
        # Pengaturan learning
        self.exploration_chance = 0.2  # 20% eksplorasi
        self.learning_rate = 0.1
        
        # Statistik
        self.episode = 0
        self.step_count = 0
        self.episode_reward = 0
        self.episode_rewards = []
        self.max_episodes = 10  # Membatasi hanya 10 episode
        self.max_steps_per_episode = 30  # Membatasi hanya 30 langkah per episode
        
        # Path untuk visualisasi
        self.current_path = []
        
        # Status episode
        self.episode_finished = False
        
    def reset_episode(self):
        """Reset untuk episode baru"""
        if self.episode < self.max_episodes:
            self.agent_x = 0
            self.agent_y = 1
            self.episode_reward = 0
            self.step_count = 0
            self.current_path = [(0, 1)]
            self.episode_finished = False
            
    def is_valid_move(self, x, y):
        """Cek apakah posisi valid"""
        # Cek batas grid
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return False
        
        # Cek obstacle
        if (x, y) in self.blocked:
            return False
            
        return True
    
    def get_reward(self, old_x, old_y, new_x, new_y):
        """Hitung reward berdasarkan gerakan"""
        # Jika sampai goal
        if new_x == 4 and new_y == 5:
            return 100
        
        # Jika menabrak (tidak bergerak)
        if old_x == new_x and old_y == new_y:
            return -10
        
        # Hitung jarak ke goal
        old_distance = abs(old_x - 4) + abs(old_y - 5)
        new_distance = abs(new_x - 4) + abs(new_y - 5)
        
        # Reward berdasarkan jarak
        if new_distance < old_distance:
            return 3  # Mendekati goal
        elif new_distance > old_distance:
            return -2  # Menjauh dari goal
        else:
            return -1  # Jarak sama
    
    def choose_action(self):
        """Pilih aksi menggunakan epsilon-greedy"""
        current_pos = (self.agent_x, self.agent_y)
        
        # Jika posisi belum pernah dikunjungi, inisialisasi nilai
        if current_pos not in self.action_values:
            self.action_values[current_pos] = [0.0, 0.0, 0.0, 0.0]
        
        # Eksplorasi atau eksploitasi
        if random.random() < self.exploration_chance:
            # Eksplorasi: pilih aksi random
            return random.randint(0, 3)
        else:
            # Eksploitasi: pilih aksi dengan nilai tertinggi
            values = self.action_values[current_pos]
            best_action = 0
            best_value = values[0]
            
            for i in range(1, 4):
                if values[i] > best_value:
                    best_value = values[i]
                    best_action = i
            
            return best_action
    
    def update_values(self, pos, action, reward):
        """Update nilai aksi"""
        if pos not in self.action_values:
            self.action_values[pos] = [0.0, 0.0, 0.0, 0.0]
        
        # Update nilai
        old_value = self.action_values[pos][action]
        new_value = old_value + self.learning_rate * (reward - old_value)
        self.action_values[pos][action] = new_value
    
    def step(self):
        """Satu langkah dari agent"""
        if self.episode >= self.max_episodes:
            return True  # Selesai semua episode
            
        if self.episode_finished:
            # Mulai episode baru
            self.episode += 1
            self.reset_episode()
            if self.episode >= self.max_episodes:
                return True
        
        # Pilih aksi
        action = self.choose_action()
        
        # Simpan posisi lama
        old_x, old_y = self.agent_x, self.agent_y
        
        # Hitung posisi baru
        move_x, move_y = self.moves[action]
        new_x = old_x + move_x
        new_y = old_y + move_y
        
        # Cek apakah gerakan valid
        if self.is_valid_move(new_x, new_y):
            self.agent_x = new_x
            self.agent_y = new_y
        
        # Hitung reward
        reward = self.get_reward(old_x, old_y, self.agent_x, self.agent_y)
        self.episode_reward += reward
        
        # Update nilai aksi
        self.update_values((old_x, old_y), action, reward)
        
        # Tambah ke path
        self.current_path.append((self.agent_x, self.agent_y))
        self.step_count += 1
        
        # Cek apakah episode selesai
        if (self.agent_x == 4 and self.agent_y == 5) or self.step_count >= self.max_steps_per_episode:
            self.episode_rewards.append(self.episode_reward)
            self.episode_finished = True
        
        return False  # Masih ada episode yang berjalan
    
    def get_best_action_arrow(self, x, y):
        """Dapatkan panah untuk aksi terbaik di posisi"""
        pos = (x, y)
        
        # Skip jika obstacle atau goal
        if pos in self.blocked or pos == self.goal:
            return ''
        
        # Skip jika belum ada nilai
        if pos not in self.action_values:
            return ''
        
        # Cari aksi dengan nilai tertinggi
        values = self.action_values[pos]
        if max(values) == 0:
            return ''
        
        best_action = 0
        best_value = values[0]
        for i in range(1, 4):
            if values[i] > best_value:
                best_value = values[i]
                best_action = i
        
        arrows = ['→', '↓', '←', '↑']
        return arrows[best_action]
    
    def draw_grid(self, ax):
        """Gambar grid dan semua elemen"""
        ax.clear()
        ax.set_xlim(-0.5, self.grid_size - 0.5)
        ax.set_ylim(-0.5, self.grid_size - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()  # Balik Y axis
        
        # Gambar garis grid
        for i in range(self.grid_size + 1):
            ax.axhline(i - 0.5, color='black', linewidth=0.5)
            ax.axvline(i - 0.5, color='black', linewidth=0.5)
        
        # Gambar obstacle (kotak abu-abu)
        for obs_x, obs_y in self.blocked:
            square = patches.Rectangle((obs_y - 0.5, obs_x - 0.5), 1, 1, 
                                     facecolor='gray', edgecolor='black')
            ax.add_patch(square)
        
        # Gambar semua titik start (kotak hijau)
        for start_pos in self.start_positions:
            start_square = patches.Rectangle((start_pos[1] - 0.5, start_pos[0] - 0.5), 1, 1, 
                                           facecolor='lightgreen', edgecolor='green')
            ax.add_patch(start_square)
            ax.text(start_pos[1], start_pos[0], 'START', ha='center', va='center', 
                   fontsize=6, fontweight='bold')
        
        # Gambar goal (kotak kuning)
        goal_square = patches.Rectangle((self.goal[1] - 0.5, self.goal[0] - 0.5), 1, 1, 
                                      facecolor='yellow', edgecolor='gold')
        ax.add_patch(goal_square)
        ax.text(self.goal[1], self.goal[0], 'GOAL', ha='center', va='center', 
               fontsize=8, fontweight='bold')
        
        # Gambar agent (lingkaran biru)
        agent_circle = patches.Circle((self.agent_y, self.agent_x), 0.3, 
                                    facecolor='blue', edgecolor='darkblue')
        ax.add_patch(agent_circle)
        
        # Gambar panah untuk policy yang dipelajari
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                arrow = self.get_best_action_arrow(i, j)
                if arrow and not (i == self.agent_x and j == self.agent_y):
                    ax.text(j, i, arrow, ha='center', va='center', 
                           fontsize=14, color='red', fontweight='bold')
        
        # Gambar path (garis merah putus-putus)
        if len(self.current_path) > 1:
            # Ambil 10 langkah terakhir
            recent_path = self.current_path[-10:]  
            path_y = [pos[1] for pos in recent_path]
            path_x = [pos[0] for pos in recent_path]
            ax.plot(path_y, path_x, 'r--', alpha=0.6, linewidth=2)
        
        # Judul dengan informasi
        episode_text = f"Episode: {self.episode + 1}/{self.max_episodes}"
        reward_text = f"Reward: {self.episode_reward}"
        steps_text = f"Steps: {self.step_count}"
        exploration_text = f"Exploration: {self.exploration_chance*100:.0f}%"
        
        title = f"Simple Multi-Armed Bandit Navigation\n{episode_text} | {reward_text} | {steps_text} | {exploration_text}"
        ax.set_title(title)
        
        # Hilangkan tick marks
        ax.set_xticks([])
        ax.set_yticks([])

def run_simulation():
    """Jalankan simulasi dengan visualisasi"""
    nav = MultiArmedBanditNavigation()
    
    print("Multi-Armed Bandit Navigation")
    print("=" * 50)
    print(f"Grid Size: {nav.grid_size}x{nav.grid_size}")
    print(f"Max Episodes: {nav.max_episodes}")
    print(f"Max Steps per Episode: {nav.max_steps_per_episode}")
    print(f"Exploration Rate: {nav.exploration_chance*100:.0f}%")
    print(f"Learning Rate: {nav.learning_rate}")
    print("\nStarting simulation...\n")
    
    # Setup matplotlib
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Flag untuk memastikan summary hanya print sekali
    summary_printed = False
    
    def animate(frame):
        nonlocal summary_printed  # Pindah ke awal fungsi
        
        # Jalankan satu langkah
        finished = nav.step()
        
        # Gambar grid
        nav.draw_grid(ax1)
        
        # Gambar grafik reward
        if nav.episode_rewards:
            episodes = list(range(1, len(nav.episode_rewards) + 1))
            ax2.clear()
            ax2.plot(episodes, nav.episode_rewards, 'b-o', markersize=6, linewidth=2)
            ax2.set_xlabel('Episode')
            ax2.set_ylabel('Total Reward')
            ax2.set_title('Learning Progress')
            ax2.grid(True, alpha=0.3)
            ax2.set_xlim(0.5, nav.max_episodes + 0.5)
            
            # Garis rata-rata
            if len(nav.episode_rewards) > 1:
                avg_reward = sum(nav.episode_rewards) / len(nav.episode_rewards)
                ax2.axhline(y=avg_reward, color='r', linestyle='--', 
                           alpha=0.7, label=f'Average: {avg_reward:.1f}')
                ax2.legend()
        
        # Print progress
        if nav.episode_finished and not finished:
            success = "✅ SUCCESS!" if nav.agent_x == 4 and nav.agent_y == 5 else "❌ Failed"
            print(f"Episode {nav.episode + 1}: {success} | "
                  f"Reward: {nav.episode_reward} | Steps: {nav.step_count}")
        
        # Stop animation jika selesai
        if finished and not summary_printed:
            summary_printed = True
            print(f"\n🎯 Simulation Complete!")
            print(f"Total Episodes: {len(nav.episode_rewards)}")
            if nav.episode_rewards:
                print(f"Average Reward: {sum(nav.episode_rewards) / len(nav.episode_rewards):.1f}")
                print(f"Best Reward: {max(nav.episode_rewards)}")
                success_count = sum(1 for r in nav.episode_rewards if r > 90)
                print(f"Success Rate: {success_count}/{len(nav.episode_rewards)} ({success_count/len(nav.episode_rewards)*100:.0f}%)")
    
    # Buat animasi
    anim = FuncAnimation(fig, animate, interval=500, cache_frame_data=False)
    
    plt.tight_layout()
    plt.show()
    
    return nav

# Jalankan simulasi
if __name__ == "__main__":
    navigator = run_simulation()