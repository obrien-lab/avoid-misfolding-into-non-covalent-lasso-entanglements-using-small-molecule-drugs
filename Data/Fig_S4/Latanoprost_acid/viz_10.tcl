set prefix "struct_10"
set outname "viz_10"

display rendermode GLSL
axes location off
display projection Orthographic
display depthcue on

color Display {Background} white

set pdb_name_list [glob "${prefix}_*.pdb"]

proc compare {a b} {
    set a0 [lindex [split [lindex [split $a "."] 0] "_"] 4]
    set b0 [lindex [split [lindex [split $b "."] 0] "_"] 4]
    if {$a0 < $b0} {
        return -1
    } else {
        return 1
    }
}

set pdb_name_list [lsort -command compare $pdb_name_list]

for { set i 0}  {$i < [llength $pdb_name_list]} {incr i} {
    if {$i == 0} {
        mol new [lindex $pdb_name_list $i] type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
    } else {
        mol addfile [lindex $pdb_name_list $i] type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
    }
}

mol delrep 0 top
mol representation NewCartoon 0.300000 10.000000 4.100000 0
mol color Index
mol selection {protein}
mol material AOEdgy
mol addrep top
mol drawframes top 0 {now}

mol representation Licorice 0.300000 12.000000 12.000000
mol color Name
mol selection {resname LIG}
mol material Opaque
mol addrep top
mol drawframes top 1 {0:4}

set viewplist {}
set fixedlist {}
set viewpoints([molinfo top]) {{{1 0 0 0.29553} {0 1 0 0.0943347} {0 0 1 0.374454} {0 0 0 1}} {{0.363024 0.83285 -0.417821 0} {-0.753186 -0.0017042 -0.657804 0} {-0.548564 0.553497 0.626674 0} {0 0 0 1}} {{0.0240978 0 0 0} {0 0.0240978 0 0} {0 0 0.0240978 0} {0 0 0 1}} {{1 0 0 0.09} {0 1 0 0.27} {0 0 1 0} {0 0 0 1}}}
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

render Tachyon $outname "$env(VMDDIR)/tachyon_LINUXAMD64 -aasamples 12 %s -format TARGA -trans_max_surfaces 1 -res 1200 1500 -o %s.tga"

file delete -force -- $outname

exec convert -trim ${outname}.tga ${outname}.png

file delete -force -- ${outname}.tga
