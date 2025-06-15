# 🧠 OS Process Scheduler Simulator (Python GUI) #

A Python-based GUI simulator for CPU scheduling algorithms.

This project simulates how various **CPU scheduling algorithms** manage a set of generated processes.  
It provides an interactive graphical interface to input data, generate processes, and visualize the scheduling timeline using **Gantt Charts**.

---

## 🚀 Features

- ✅ Process Generator based on user input
- ✅ GUI built with Tkinter
- ✅ Supports the following scheduling algorithms:
  - **FCFS (First-Come First-Served)**
  - **SJF (Shortest Job First)**
  - **Round Robin**
  - **Priority Scheduling**
- ✅ Gantt Chart visualization for each algorithm
- ✅ Easy-to-use interface for students and learners

---

## 📷 Demo


https://github.com/user-attachments/assets/06a23357-a780-45b0-b907-83d6debda168




---

## 🧪 How to Run

bash
# Clone the repo
git clone https://github.com/your-username/Process-Scheduler-Simulator.git
cd Process-Scheduler-Simulator

# Make sure you have Python 3 installed
python GUI.py


> All required algorithm files and `process_generator.py` should be in the same directory.

---

## 📝 Project Structure


├── GUI.py                     # Main GUI file
├── process_generator.py       # Generates processes based on input
├── fcfs.py          # FCFS scheduling algorithm
├── sjf.py          # SJF (Preemptive) scheduling
├── round_robin.py             # Round Robin algorithm
├── priority.py # Priority scheduling algorithm
├── input.txt                  # Input values (auto-loaded)
├── processes.txt                 # Generated process data


---

## 📚 Algorithms Overview

### 🟠 FCFS – First Come First Served
- Simple and non-preemptive.
- Executes processes in the order they arrive.

### 🔵 SJF – Shortest Job First
- Chooses the process with the smallest execution time.
- Can be **preemptive (SRTF)** or non-preemptive.

### 🟢 Round Robin
- Each process gets a small time slot (quantum).
- Suitable for time-sharing systems.

### 🟣 Priority Scheduling
- Each process is assigned a priority.
- Higher priority processes are executed first.

---

## 📥 Sample Input


5
3 7 2 1 4


> Where `5` is the number of processes and the rest are burst times or priorities based on the algorithm.

---

## 👨‍💻 Developed By

**Ibrahim Mohamed**  
Student @ Egyptian Chinese University  
Passionate about Operating Systems, Problem Solving, and GUI Development.

---

## 📄 License

This project is for educational use only.

---

## ❤ Contributions

Feel free to fork the repo, improve the design, or add more algorithms. Pull requests are welcome!
