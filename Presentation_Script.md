# PPT Presentation Script: Memory Forensics in Modern Operating Systems

**Presenter:** Manoj Santhoju
**Time:** Approx. 15-20 Minutes
**Goal:** Defend the research project, demonstrating technical depth and academic rigour.

---

## Slide 1: Title Slide
**Visual:** Project Title, Your Name (Manoj Santhoju), Student ID (23394544), Supervisor (Dr. Zakaria Sabir), NCI Logo.
**Script:**
"Good morning/afternoon everyone. My name is Manoj Santhoju, and today I will be presenting my MSc research project titled 'Memory Forensics in Modern Operating Systems: Techniques and Tool Comparison'. This project investigates the challenges of digital forensics on modern platforms and proposes a Unified Framework to address them."

## Slide 2: Agenda
**Visual:** Bullet points: Introduction, Research Problem, Methodology (Unified Framework), Implementation, Evaluation/Demo, Conclusion.
**Script:**
"Here is the agenda for today. I will start by outlining the research problem—specifically why modern OS protections make forensics difficult. Then, I will introduce my solution: the Unified Memory Forensics Framework. We will dive into the implementation details, look at the experimental results, and conclude with key findings."

## Slide 3: Research Problem & Motivation
**Visual:** Icons representing 'Volatile Memory', 'Malware (Fileless)', 'Encryption', and 'Kernel Protection'.
**Script:**
"Traditional forensics relies on hard drive analysis. However, modern cyber threats are increasingly 'fileless', living entirely in the computer's RAM.
Simultaneously, operating systems like Windows 11 and recent Linux kernels have introduced strict security features—like Kernel Patch Protection and Address Space Randomization—that, ironically, break traditional forensic tools.
The problem is: Investigators have to juggle multiple broken tools for different OSs, leading to inefficient investigations."

## Slide 4: Research Question & Objectives
**Visual:** The core Research Question text.
**Script:**
"This leads to my primary research question:
*How can we standardise memory forensics analysis across heterogenous operating systems while maintaining detection accuracy against modern obfuscation techniques?*
My objective was to build a single, unified framework that abstracts the complexity of underlying tools like Volatility and Rekall."

## Slide 5: The Solution: Unified Memory Forensics Framework
**Visual:** High-level architecture diagram. A central "Framework" box connecting to "Windows", "Linux", "macOS" on one side and "Volatility", "Rekall" on the other.
**Script:**
"To solve this, I developed the Unified Memory Forensics Framework.
It is a Python-based middleware that acts as an intelligent wrapper. It automatically detects the operating system of a memory dump and selects the best underlying tool—Volatility 3 for Windows/Linux or Rekall for macOS.
Crucially, it normalizes the output into a standard JSON format, allowing for consistent analysis regardless of the source OS."

## Slide 6: Implementation Details (Technical Depth)
**Visual:** Screenshot of the `framework.py` code or the Class structure (`UnifiedForensicsFramework` class).
**Script:**
"Let's look at the implementation. The core of the system is the `UnifiedForensicsFramework` class in Python.
I implemented a `Plugin System` that allows for modular analysis. For example, the `MalwareDetector` plugin scans the normalized process list for known suspicious patterns using Regex and Heuristics.
I also integrated an `OSDetector` module that analyzes the file header to automatically determine if a dump is from Windows, Linux, or macOS."

## Slide 7: Automation & Reliability
**Visual:** Screenshots of the `test_complete_malware.sh` script or the Console Output showing the 10-step process.
**Script:**
"Reliability was a key focus. I created extensive automation scripts—Bash for Linux/Mac and Batch for Windows.
These scripts automate the entire forensic lifecycle:
1. Cleaning previous artifacts.
2. Simulating a malware attack (spawning a dummy malicious process).
3. capturing a memory dump.
4. Analyzing it with the framework.
This ensures my experiments are reproducible and consistent."

## Slide 8: Evaluation & Results
**Visual:** The "Detection Rate vs Event Rate" graph (from your report) ~or~ a Table comparison.
**Script:**
"I evaluated the framework by simulating high-load environments.
This chart shows the Detection Rate (Y-axis) versus Event Rate (X-axis).
You can see that the framework maintains over 95% accuracy in low-to-medium load scenarios. Even at high loads (200 events/sec), it retains roughly 70% accuracy, which is significant for real-time analysis."

## Slide 9: Live Demo / Walkthrough (Optional)
**Visual:** A video clip or screenshot series of the tool detecting 'nc.exe'.
**Script:**
"In my testing, I deployed a simulated malware process named 'nc.exe'.
As you can see in this output, the framework successfully flagged it as 'RISK: HIGH' and correctly identified its Parent Process ID. This validates the plugin's capability to detect anomalies in a heterogeneous environment."

## Slide 10: Conclusion & Future Work
**Visual:** Summary points: "Unified Interface", "Cross-Platform", "Open Source".
**Script:**
"In conclusion, this project successfully demonstrates that a unified abstraction layer can simplify memory forensics without sacrificing accuracy.
For future work, I plan to integrate AI-driven anomaly detection to further improve the heuristic analysis.
Thank you for listening. I am happy to take your questions."
