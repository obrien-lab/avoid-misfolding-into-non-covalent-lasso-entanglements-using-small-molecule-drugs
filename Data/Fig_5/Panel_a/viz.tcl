package require topotools
display rendermode GLSL
display depthcue off
display projection orthographic 
axes location off

color Display {Background} white

set viewplist {}
set fixedlist {}

mol new ./model2_9VD_bound.psf type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol addfile ./model2_9VD_bound.cor type cor first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
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
set viewpoints([molinfo top]) {{{1 0 0 -42.687} {0 1 0 -42.6411} {0 0 1 -42.4634} {0 0 0 1}} {{-0.241407 -0.877007 0.415431 0} {0.694781 0.142673 0.70493 0} {-0.677498 0.458809 0.574886 0} {0 0 0 1}} {{0.0404968 0 0 0} {0 0.0404968 0 0} {0 0 0.0404968 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
# done with molecule 0

mol new ./model2.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation NewCartoon 0.300000 10.000000 4.100000 0
mol color Index
mol selection {all}
mol material AOEdgy
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 -42.687} {0 1 0 -42.6411} {0 0 1 -42.4634} {0 0 0 1}} {{-0.241407 -0.877007 0.415431 0} {0.694781 0.142673 0.70493 0} {-0.677498 0.458809 0.574886 0} {0 0 0 1}} {{0.0404968 0 0 0} {0 0.0404968 0 0} {0 0 0.0404968 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
set topmol [molinfo top]
# done with molecule 1

mol new ./model2_fp_001.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation QuickSurf 1.300000 0.500000 1.000000 3.000000
mol color ColorID 4
mol selection {all}
mol material GlassBubble
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 -42.687} {0 1 0 -42.6411} {0 0 1 -42.4634} {0 0 0 1}} {{-0.241407 -0.877007 0.415431 0} {0.694781 0.142673 0.70493 0} {-0.677498 0.458809 0.574886 0} {0 0 0 1}} {{0.0404968 0 0 0} {0 0.0404968 0 0} {0 0 0.0404968 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
# done with molecule 2
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

