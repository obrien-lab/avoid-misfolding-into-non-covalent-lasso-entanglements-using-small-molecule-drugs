set prefix "model1"
set num_sites 1

display rendermode GLSL
axes location off

color Display {Background} white

mol new $prefix.pdb type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
mol delrep 0 top
mol representation NewCartoon 0.300000 10.000000 4.100000 0
mol color Index
mol selection {protein}
mol material AOChalky
mol addrep top

# Load fp pdbs
for { set i 1}  {$i <= $num_sites} {incr i} {
    set filename [format "%s/%s_fp_%03d.pdb" $prefix $prefix $i]
    mol new $filename type pdb first 0 last -1 step 1 filebonds 1 autobonds 1 waitfor all
    mol delrep 0 top
    mol representation QuickSurf
    mol color ColorID 3
    mol selection {all}
    mol material AOChalky
    mol addrep top
    mol rename top [format "fp_%03d" $i]
    mol off top
}

mol top 0
display resetview
