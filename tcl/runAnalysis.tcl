puts " -------------Uniaxial Inelastic Section, Nonlinear Model -------------"
puts " -------------Uniform Earthquake Excitation -------------"
# SET UP ----------------------------------------------------------------------------
wipe;				# clear memory of all past model definitions
model BasicBuilder -ndm 3 -ndf 6;	# Define the model builder, ndm=#dimension, ndf=#dofs
set dataDir ../Out;			# set up name of data directory
file mkdir $dataDir; 			# create data directory
source LibUnits.tcl;			# define units
source DisplayPlane.tcl;		# procedure for displaying a plane in model
source DisplayModel3D.tcl;		# procedure for displaying 3D perspectives of model
source ../Inputs.tcl

if {$FrameType == "Concrete"} {
    source Ex8.genericFrame3D.build.RCsec.tcl
    source Ex8.genericFrame3D.analyze.Dynamic.EQ.Uniform.tcl
} elseif {$FrameType == "Steel"} {
    source Ex8.genericFrame3D.build.Wsec.tcl
    source Ex8.genericFrame3D.analyze.Dynamic.EQ.Uniform.tcl
}
