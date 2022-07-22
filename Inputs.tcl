# ------ frame configuration
set NStory 5;			# number of stories above ground level
set NBay 1;			# number of bays in X direction
set NBayZ 1;			# number of bays in Z direction

# define GEOMETRY -------------------------------------------------------------
# define structure-geometry paramters
set LCol [expr 50*$ft];		# column height (parallel to Y axis)
set LBeam [expr 20*$ft];		# beam length (parallel to X axis)
set LGird [expr 20*$ft];		# girder length (parallel to Z axis)
set GJ [expr 1*$ksi*$in4];  # Section torsion constant (added in OpenSees >3.2.2)

# Uniform Earthquake ground motion (uniform acceleration input at all support nodes)
set GMdir "../GMfiles";		# ground-motion file directory
set GMdirection 1;				# ground-motion direction
set GMfile "H-E12140" ;			# ground-motion filenames
set GMfact 1.5;				# ground-motion scaling factor