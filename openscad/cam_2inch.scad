module standoffs(x0, x1, h = -7){
difference()
    {
        translate([x0/2,x1/2,h]) cylinder(h = 4, r1 = 2.5, r2 = 2.5, center = true);
        translate([x0/2,x1/2,h]) cylinder(h = 4, r1 = 1.5, r2 = 1.5, center = true);
    }
}

module standoffs_cutout(x0, x1, h = -5){

    
        translate([x0/2,x1/2,h]) cylinder(h = 20, r1 = 1.5, r2 = 1.5, center = true);
    
}

difference(){
union(){
 
import("collimator-nocross-2.0.stl");

translate([0,0,-35]) cylinder(h = 70, r1 = 32, r2 = 32, center = true);
}
translate([0,0,-55]) cylinder(h = 70, r1 = 32, r2 = 32, center = true);
translate([0,0,-40]) cylinder(h = 70, r1 = 27.5, r2 = 27.5, center = true);
translate([0,0,-00]) cylinder(h = 70, r1 = 5, r2 = 5, center = true);
standoffs_cutout(28,28,0);
standoffs_cutout(28,-28,0);
standoffs_cutout(-28,28,0);
standoffs_cutout(-28,-28,0);
}
//translate([0,0,-30]) cube(size = [28,28,28], center = true);


standoffs(28,28);
standoffs(28,-28);
standoffs(-28,28);
standoffs(-28,-28);
