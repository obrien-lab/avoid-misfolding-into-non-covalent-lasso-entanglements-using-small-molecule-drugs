package require topotools
display rendermode GLSL
axes location off
display projection Orthographic
disply depthcue off

color Display {Background} white

mol new ./traj_2_l60.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation NewCartoon 0.600000 10.000000 3.000000 0
mol color ColorID 10
mol selection {segname A}
mol material AOEdgy
mol addrep top

mol representation QuickSurf 2.000000 1.000000 3.000000 1.000000
mol color ColorID 6
mol selection {not segname A AtR PtR LIG}
mol material Glass2
mol addrep top
mol representation QuickSurf 2.000000 1.000000 3.000000 1.000000
mol color ColorID 3
mol selection {segname AtR}
mol material Diffuse
mol addrep top
mol representation QuickSurf 2.000000 1.000000 3.000000 1.000000
mol color ColorID 3
mol selection {segname PtR}
mol material Diffuse
mol addrep top

mol representation VDW 0.500000 12.000000
mol color ColorID 27
mol selection {segname LIG}
mol material Opaque
mol addrep top
mol representation DynamicBonds 10.000000 0.100000 12.000000
mol color ColorID 6
mol selection {segname LIG}
mol material AOChalky
mol addrep top

set viewplist {}
set fixedlist {}
set viewpoints([molinfo top]) {{{1 0 0 -25.9619} {0 1 0 -9.60361} {0 0 1 -1.88204} {0 0 0 1}} {{0.579449 0.00158709 -0.815005 0} {0.130733 0.986868 0.0948694 0} {0.804455 -0.16152 0.571631 0} {0 0 0 1}} {{0.0169804 0 0 0} {0 0.0169804 0 0} {0 0 0.0169804 0} {0 0 0 1}} {{1 0 0 -0.98} {0 1 0 0.14} {0 0 1 -1.29} {0 0 0 1}}}
lappend viewplist [molinfo top]
set topmol [molinfo top]
# done with molecule 0
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
