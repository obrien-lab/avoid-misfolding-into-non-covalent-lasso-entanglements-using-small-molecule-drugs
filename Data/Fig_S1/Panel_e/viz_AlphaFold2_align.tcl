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
mol drawframes top 0 {1:5}

set viewpoints([molinfo top]) {{{1 0 0 0.321701} {0 1 0 0.670106} {0 0 1 -0.352721} {0 0 0 1}} {{-0.220693 -0.701609 0.677517 0} {0.941711 0.027546 0.335278 0} {-0.253898 0.712019 0.654638 0} {0 0 0 1}} {{0.0422272 0 0 0} {0 0.0422272 0 0} {0 0 0.0422272 0} {0 0 0 1}} {{1 0 0 0.03} {0 1 0 0.45} {0 0 1 0} {0 0 0 1}}}
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

