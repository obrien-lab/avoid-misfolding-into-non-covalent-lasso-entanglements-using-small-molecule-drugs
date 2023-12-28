package require topotools
display rendermode GLSL
display depthcue off
display projection orthographic 
axes location off

color Display {Background} white

set viewplist {}
set fixedlist {}

mol new protein_9VD_bound.psf type psf first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol addfile protein_9VD_bound.cor type cor first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
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
set viewpoints([molinfo top]) {{{1 0 0 -5.23595} {0 1 0 -35.0411} {0 0 1 -61.4602} {0 0 0 1}} {{0.531099 -0.829307 -0.173735 0} {0.167462 0.303736 -0.937923 0} {0.830595 0.469037 0.300192 0} {0 0 0 1}} {{0.0370036 0 0 0} {0 0.0370036 0 0} {0 0 0.0370036 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
# done with molecule 0

mol new 4c5c_model_clean.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation NewCartoon 0.300000 10.000000 4.100000 0
mol color ColorID 8
mol selection {all}
mol material AOEdgy
mol addrep top
mol representation NewCartoon 0.350000 10.000000 4.100000 0
mol color ColorID 1
mol selection {resid 98 to 146}
mol material Opaque
mol addrep top
mol representation NewCartoon 0.350000 10.000000 4.100000 0
mol color ColorID 0
mol selection {resid 174 to 184}
mol material Opaque
mol addrep top
mol representation VDW 1.000000 12.000000
mol color ColorID 3
mol selection {resid 98 146 and name CA}
mol material Opaque
mol addrep top
set sel [atomselect top "resid 98 146 and name CA"]
set idx [$sel get index]
topo addbond [lindex $idx 0] [lindex $idx 1]
mol representation Bonds 0.300000 12.000000
mol color ColorID 3
mol selection {resid 98 146 and name CA}
mol material Opaque
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 -5.23595} {0 1 0 -35.0411} {0 0 1 -61.4602} {0 0 0 1}} {{0.531099 -0.829307 -0.173735 0} {0.167462 0.303736 -0.937923 0} {0.830595 0.469037 0.300192 0} {0 0 0 1}} {{0.0370036 0 0 0} {0 0.0370036 0 0} {0 0 0.0370036 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
lappend viewplist [molinfo top]
set topmol [molinfo top]
# done with molecule 1

mol new 4c5c_model_clean_fp_004.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation QuickSurf 1.300000 0.500000 1.000000 3.000000
mol color ColorID 4
mol selection {all}
mol material GlassBubble
mol addrep top
set viewpoints([molinfo top]) {{{1 0 0 -5.23595} {0 1 0 -35.0411} {0 0 1 -61.4602} {0 0 0 1}} {{0.531099 -0.829307 -0.173735 0} {0.167462 0.303736 -0.937923 0} {0.830595 0.469037 0.300192 0} {0 0 0 1}} {{0.0370036 0 0 0} {0 0.0370036 0 0} {0 0 0.0370036 0} {0 0 0 1}} {{1 0 0 0} {0 1 0 0} {0 0 1 0} {0 0 0 1}}}
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

