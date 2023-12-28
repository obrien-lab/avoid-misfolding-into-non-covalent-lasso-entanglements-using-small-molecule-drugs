package require topotools
display rendermode GLSL
display depthcue off
display projection orthographic 
axes location off

color Display {Background} white

set viewplist {}
set fixedlist {}

mol new ./models.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation NewCartoon 0.300000 10.000000 4.100000 0
mol color Index
mol selection {all}
mol material AOEdgy
mol addrep top
mol drawframes top 0 {6:10}

set viewpoints([molinfo top]) {{{1 0 0 0.302463} {0 1 0 0.115999} {0 0 1 -0.514022} {0 0 0 1}} {{-0.492766 0.351865 -0.795846 0} {0.686515 0.719184 -0.107098 0} {0.534677 -0.599135 -0.59595 0} {0 0 0 1}} {{0.0513593 0 0 0} {0 0.0513593 0 0} {0 0 0.0513593 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
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

