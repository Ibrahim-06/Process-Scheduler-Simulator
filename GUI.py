from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority
from algorithms.round_robin import round_robin
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
import matplotlib.colors as mcolors
import random

class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1000x700")
        self.processes = []
        self.algorithm = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="⚙️ CPU Scheduling Simulator", font=("Helvetica", 18, "bold"), fg="#4B0082").pack(pady=(10))
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Button(input_frame, text="📁 Load from PC", command=self.load_from_file, bg="#DDA0DD").grid(row=0, column=0, padx=5)
        tk.Button(input_frame, text="📝 Enter Manually", command=self.enter_manually, bg="#D8BFD8").grid(row=0, column=1, padx=5)
        tk.Button(input_frame, text="Generate Processes", command=self.run_generator, bg="#c090ff").grid(row=0, column=2, padx=5)

        algo_frame = tk.Frame(self.root)
        algo_frame.pack(pady=10)

        tk.Label(algo_frame, text="Select Algorithm: ").grid(row=0, column=0)
        algo_menu = ttk.Combobox(algo_frame, textvariable=self.algorithm, values=["FCFS", "SJF", "Priority", "Round Robin"])
        algo_menu.grid(row=0, column=1)
        algo_menu.current(0)

        tk.Button(algo_frame, text="▶ Run", command=self.run_algorithm, bg="#9370DB").grid(row=0, column=2, padx=10)
        tk.Button(algo_frame, text="🔍 Compare Algorithms", command=self.compare_algorithms, bg="#7B68EE").grid(row=0, column=3, padx=10)

        self.result_label_frame = tk.Frame(self.root, bg="#4B0082")
        self.result_label_frame.pack(pady=(10, 20))
        
        self.result_label = tk.Label(self.result_label_frame, text="OutPut", font=("Helvetica", 16, "bold","italic"),
                                     fg="white", bg="#4B0082")
        self.result_label.pack(pady=(6,0))
        
        
        self.table = ttk.Treeview(self.result_label_frame, columns=("PID", "Arrival", "Burst", "Priority", "Start", "End", "WT", "TAT"), show="headings", height=10)
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=112)
        self.table.pack(pady=5)
        
        self.avg_label = tk.Label(self.result_label_frame, text="Created by :-  Ibrahim Mohamed  &  Eslam Ahmed  &  Kareem Tamer  &  Mohamed Salah", font=("Helvetica", 12 ,"italic","bold"), fg="white", bg="#4B0082")
        self.avg_label.pack(pady=(5, 11), fill="x")
        self.avg_label.config(anchor="center", justify="center")

        
        
        self.gantt_frame = tk.Frame(self.root, bg="#4B0082")
        self.gantt_frame.pack(pady=(10, 20))
        
        self.title_label = tk.Label(self.gantt_frame, text="Gantt Chart", font=("Helvetica", 16, "bold","italic"),
                                    fg="white", bg="#4B0082")
        self.title_label.pack(pady=(5))
        
        self.figure = plt.Figure(figsize=(9, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.gantt_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

    def load_from_file(self):
        file_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.input_file = file_path
            messagebox.showinfo("Loaded", f"Loaded file: {file_path}")

    def enter_manually(self):
        top = tk.Toplevel(self.root)
        top.title("Enter Process Data")
        label = tk.Label(top, text="Enter data (one process per line: ID Arrival Burst Priority):")
        label.pack(pady=5)
        text = scrolledtext.ScrolledText(top, width=40, height=10)
        text.pack(padx=10, pady=10)

        def save():
            data = text.get("1.0", tk.END).strip()
            with open("Processes.txt", "w") as f:
                f.write(data)
            self.input_file = "Processes.txt"
            top.destroy()
            messagebox.showinfo("Saved", "Data saved to Processes.txt")

        tk.Button(top, text="Save", command=save).pack(pady=5)

    def run_generator(self):
        try:
            subprocess.run(["python", "ProcessGenerator.py"], check=True)
            self.input_file = "Processes.txt"
            messagebox.showinfo("Success", "Precesses Generated Sucessfully ✅")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run generator: {e}")

    def read_process_file(self, path):
        processes = []
        # خلّي الـ quantum اختياري مش إجباري
        quantum = None
        with open(path) as f:
            for line in f:
                parts = line.strip().split()
                if parts[0].lower() == "quantum":
                    quantum = int(parts[1])
                elif len(parts) >= 4:
                    processes.append({
                        "pid": parts[0],
                        "arrival": int(parts[1]),
                        "burst": int(parts[2]),
                        "priority": int(parts[3])
                    })
        # فقط لو quantum مكتوب في الملف
        if quantum is not None:
            self.quantum = quantum
        return processes

    def run_algorithm(self):
        if not hasattr(self, 'input_file'):
            messagebox.showwarning("No Data", "Please load or enter process data first.")
            return
    
        try:
            self.processes = self.read_process_file(self.input_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read process file: {e}")
            return
    
        algo = self.algorithm.get()
    
        for p in self.processes:
            p.pop("start", None)
            p.pop("end", None)
            p.pop("tat", None)
            p.pop("wt", None)
    
        if algo == "FCFS":
            timeline = fcfs(self.processes)
        elif algo == "SJF":
            timeline = sjf(self.processes)
        elif algo == "Priority":
            timeline = priority(self.processes)
        elif algo == "Round Robin":
            quantum = simpledialog.askinteger("Quantum", "Enter Quantum Time (positive integer):", minvalue=1)
            if quantum is None:
                messagebox.showinfo("Cancelled", "Round Robin execution cancelled.")
                return
            self.quantum = quantum
            timeline = round_robin(self.processes, self.quantum)
        else:
            messagebox.showerror("Error", "Unknown algorithm selected.")
            return
    
        self.display_result(timeline)
        self.plot_gantt(timeline)
    
    def display_result(self, timeline):
        for row in self.table.get_children():
            self.table.delete(row)
    
        total_wt = total_tat = 0
        for p in self.processes:
            total_wt += p['wt']
            total_tat += p['tat']
            self.table.insert("", "end", values=(
                p['pid'], p['arrival'], p['burst'], p['priority'],
                p['start'], p['end'], p['wt'], p['tat']
            ))
    
        n = len(self.processes)
        avg_wt = total_wt / n
        avg_tat = total_tat / n
        self.avg_label.config(text=f"Average Waiting Time: {avg_wt:.2f}    |    Average Turnaround Time: {avg_tat:.2f}")
    def compare_algorithms(self):
        if not hasattr(self, 'input_file'):
            messagebox.showwarning("No Data", "Please load or enter process data first.")
            return
    
        try:
            original_processes = self.read_process_file(self.input_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read process file: {e}")
            return
    
        results = []
    
        for algo in ["FCFS", "SJF", "Priority", "Round Robin"]:
            processes = [p.copy() for p in original_processes]
    
            for p in processes:
                p.pop("start", None)
                p.pop("end", None)
                p.pop("tat", None)
                p.pop("wt", None)
    
            if algo == "FCFS":
                fcfs(processes)
            elif algo == "SJF":
                sjf(processes)
            elif algo == "Priority":
                priority(processes)
            elif algo == "Round Robin":
                round_robin(processes, self.quantum)
    
            total_wt = sum(p['wt'] for p in processes)
            total_tat = sum(p['tat'] for p in processes)
            n = len(processes)
            avg_wt = total_wt / n
            avg_tat = total_tat / n
            results.append((algo, avg_wt, avg_tat))
    
        best = min(results, key=lambda x: (x[1], x[2]))
    
        summary = "-------------------------------------------------------------\n".join([f"{algo}: Avg WT = {wt:.2f}, Avg TAT = {tat:.2f}\n" for algo, wt, tat in results])
        summary += f"\n\n✅ The best Algorithm is : {best[0]}"
    
        messagebox.showinfo("Comparison Results", summary)
    

    def plot_gantt(self, timeline):
        self.ax.clear()
    
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlabel("")
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_xlim(0, max([end for _, _, end in timeline]) + 2)
    
        for spine in self.ax.spines.values():
            spine.set_visible(False)
    
        colors = plt.cm.get_cmap('tab10', len(set([p[0] for p in timeline])))
        color_map = {}
        end_times = []
    
        for i, (pid, start, end) in enumerate(timeline):
            if pid not in color_map:
                color_map[pid] = colors(len(color_map) % 10)
    
            self.ax.barh(0, end - start, left=start, height=0.5,
                         color=color_map[pid], edgecolor='white')
            self.ax.text((start + end) / 2, 0, pid, ha='center', va='center',
                         color='white', fontsize=9, fontweight='bold')
            self.ax.text(start, 0.3, f"{start}", ha='center', va='bottom', fontsize=8, color='black')
            end_times.append(end)
    
        self.ax.text(0, 0.3, "0", ha='center', va='bottom', fontsize=8, color='black')
        max_end = max(end_times)
        self.ax.text(max_end, 0.3, f"{max_end}", ha='center', va='bottom', fontsize=8, color='black')
    
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()
