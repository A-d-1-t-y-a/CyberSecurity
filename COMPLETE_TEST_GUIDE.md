# 🎯 Complete Testing Guide - Unified Memory Forensics Framework

**Author:** Manoj Santhoju  
**Institution:** National College of Ireland  
**Program:** MSc Cybersecurity

## 🚀 Quick Start

### **Windows - Complete Test (Recommended)**
```cmd
test_complete_malware.bat
```

This single script will:
1. ✅ Clean up previous test artifacts
2. ✅ Run malware simulation
3. ✅ Create memory dump with malware artifacts
4. ✅ Run basic analysis
5. ✅ Run experimental analysis
6. ✅ Generate graphs
7. ✅ Show results
8. ✅ Optionally clean up

### **Manual Steps (If Needed)**

#### **Step 1: Run Malware Simulation**
```cmd
py test_malware_simulation.py
```

#### **Step 2: Create Memory Dump**
```cmd
py create_malware_memory_dump.py --filename memory_dump_with_malware.raw --os-type windows --size 50
```

#### **Step 3: Run Analysis**
```cmd
py -m unified_forensics experiment memory_dump_with_malware.raw --os-type windows --rates 1 --rates 10 --rates 20
```

#### **Step 4: Clean Up (When Done)**
```cmd
py test_malware_simulation.py --cleanup
del memory_dump_with_malware.raw
```

## 📋 Testing Without Malware

### **Test with Sample Memory Dumps**
```cmd
# Generate sample dumps
py quick_sample_generator.py

# Analyze without malware
py -m unified_forensics analyze memory_dump_samples\windows_sample.mem --os-type windows --format summary
```

## 🔧 Setup (First Time Only)

### **Windows**
```cmd
setup_windows.bat
```

### **Linux**
```bash
chmod +x setup_linux.sh
./setup_linux.sh
```

### **macOS**
```bash
chmod +x setup_macos.sh
./setup_macos.sh
```

## 📊 Understanding Results

### **Files Generated**
- `memory_dump_with_malware.raw` - Memory dump with malware artifacts
- `analysis_results/malware_test_complete.json` - Analysis results
- `performance_charts/detection_performance_windows_*.png` - Performance graphs
- `malware_test_environment/` - Test artifacts

### **Graphs Should Show**
- ✅ Detection rate curve (not straight line)
- ✅ Detected events count
- ✅ Meaningful variations by event rate

## 🧹 Cleanup

### **Remove Test Artifacts**
```cmd
py test_malware_simulation.py --cleanup
del memory_dump_with_malware.raw
```

### **Remove All Test Files**
```cmd
cleanup_unnecessary_files.bat
```

## 🆘 Troubleshooting

### **Error: File already exists**
**Solution:** The script now auto-cleans. If issues persist:
```cmd
rmdir /s /q malware_test_environment
py test_complete_malware.bat
```

### **Error: Memory dump not found**
**Solution:** Script auto-creates it. If issues persist:
```cmd
py create_malware_memory_dump.py
```

### **Graphs show straight lines**
**Solution:** 
1. Ensure malware simulation ran
2. Check analysis results in `analysis_results/`
3. Verify malware artifacts in dump

## 📝 Command Reference

### **Main Commands**
```cmd
# Complete test
test_complete_malware.bat

# Malware simulation only
py test_malware_simulation.py

# Create memory dump
py create_malware_memory_dump.py

# Analysis
py -m unified_forensics analyze <dump> --os-type windows --plugins malware

# Experimental analysis
py -m unified_forensics experiment <dump> --os-type windows --rates 1 --rates 10

# Cleanup
py test_malware_simulation.py --cleanup
```

## ✅ Verification Checklist

After running `test_complete_malware.bat`:

- [ ] No errors during execution
- [ ] Memory dump created (`memory_dump_with_malware.raw`)
- [ ] Analysis results saved (`analysis_results/malware_test_complete.json`)
- [ ] Graphs generated (`performance_charts/detection_performance_windows_*.png`)
- [ ] Graphs show variations (not straight lines)
- [ ] Test artifacts present (`malware_test_environment/`)

## 🎓 For Professor Presentation

1. **Show Setup:**
   ```cmd
   setup_windows.bat
   ```

2. **Run Complete Test:**
   ```cmd
   test_complete_malware.bat
   ```

3. **Show Results:**
   - Open `performance_charts/` folder
   - Show graphs with real detection data
   - Explain detection metrics

4. **Clean Up:**
   ```cmd
   py test_malware_simulation.py --cleanup
   ```

---

**Everything is ready! Just run `test_complete_malware.bat`** 🎯
