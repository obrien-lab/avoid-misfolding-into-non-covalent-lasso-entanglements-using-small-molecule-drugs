display rendermode GLSL
display depthcue off
display projection orthographic 
axes location off

color Display {Background} white

set viewplist {}
set fixedlist {}

mol new 9VD.psf type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol addfile 9VD.cor type cor first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation VDW 0.400000 12.000000
mol color ColorID 27
mol selection {resname 9VD}
mol material AOChalky
mol addrep top
mol representation Bonds 0.100000 12.000000
mol color ColorID 8
mol selection {resname 9VD}
mol material AOEdgy
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}} {{0.859573 -0.510791 0.0152127 0} {-0.184857 -0.33856 -0.922609 0} {0.476411 0.790235 -0.385439 0} {0 0 0 1}} {{0.190337 0 0 0} {0 0.190337 0 0} {0 0 0.190337 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
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

