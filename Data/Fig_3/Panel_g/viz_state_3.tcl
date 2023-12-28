package require topotools
display rendermode GLSL
display depthcue off
display projection orthographic 
axes location off

color Display {Background} white

set viewplist {}
set fixedlist {}

mol new prot_l306.psf type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol addfile sampled_traj.dcd type dcd first 2 last 2 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation VDW 0.500000 12.000000
mol color ColorID 27
mol selection {resname 9VD}
mol material Opaque
mol addrep top
mol representation Bonds 0.100000 12.000000
mol color ColorID 8
mol selection {resname 9VD}
mol material AOChalky
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 0.16964} {0 1 0 -0.382014} {0 0 1 0.0581859} {0 0 0 1}} {{-0.842302 0.334646 -0.422536 0} {0.484405 0.813775 -0.321127 0} {0.236385 -0.475165 -0.847549 0} {0 0 0 1}} {{0.0388713 0 0 0} {0 0.0388713 0 0} {0 0 0.0388713 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
# done with molecule 0

mol new state_3.pdb
mol delrep 0 top
mol representation NewCartoon 0.300000 10.000000 4.100000 0
mol color ColorID 8
mol selection {all}
mol material AOEdgy
mol addrep top
mol representation NewCartoon 0.350000 10.000000 4.100000 0
mol color ColorID 1
mol selection {resid 98 to 116}
mol material Opaque
mol addrep top
mol representation NewCartoon 0.350000 10.000000 4.100000 0
mol color ColorID 0
mol selection {resid 181 to 191}
mol material Opaque
mol addrep top
mol representation VDW 1.000000 12.000000
mol color ColorID 3
mol selection {resid 98 116 and name CA}
mol material Opaque
mol addrep top
set sel [atomselect top "resid 98 116 and name CA"]
set idx [$sel get index]
topo addbond [lindex $idx 0] [lindex $idx 1]
mol representation Bonds 0.300000 12.000000
mol color ColorID 3
mol selection {resid 98 116 and name CA}
mol material Opaque
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 0.16964} {0 1 0 -0.382014} {0 0 1 0.0581859} {0 0 0 1}} {{-0.842302 0.334646 -0.422536 0} {0.484405 0.813775 -0.321127 0} {0.236385 -0.475165 -0.847549 0} {0 0 0 1}} {{0.0388713 0 0 0} {0 0.0388713 0 0} {0 0 0.0388713 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
set topmol [molinfo top]
# done with molecule 1

foreach v $viewplist {
  molinfo $v set {center_matrix rotate_matrix scale_matrix global_matrix} $viewpoints($v)
}
foreach v $fixedlist {
  molinfo $v set fixed 1
}
unset viewplist
unset fixedlist
mol top $topmol
unset topmol

