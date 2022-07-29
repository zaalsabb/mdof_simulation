cd tcl
"../OpenSees/bin/OpenSees.exe" runAnalysis.tcl
cd ..
python process_disp.py Out/disp.out Out/nodes.txt Out/elements.txt Out/disps_final.txt