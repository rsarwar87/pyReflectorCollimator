module standoffs(x0, x1, h = -7){
difference()
    {
        translate([x0/2,x1/2,h]) cylinder(h = 4, r1 = 2.5, r2 = 2.5, center = true);
        translate([x0/2,x1/2,h]) cylinder(h = 4, r1 = 1., r2 = 1.5, center = true);
    }
}

module standoffs_cutout(x0, x1, h = -5, r=1.5){

    
        translate([x0/2,x1/2,h]) cylinder(h = 20, r1 =r, r2 = r, center = true);
    
}

difference(){
union(){
 
import("collimator-nocross-2.0.stl");

translate([0,0,-35]) cylinder(h = 70, r1 = 32, r2 = 32, center = true);
}
translate([0,0,-55]) cylinder(h = 70, r1 = 32, r2 = 32, center = true);
translate([0,0,-40]) cylinder(h = 70, r1 = 27.5, r2 = 27.5, center = true);
translate([0,0,-00]) cylinder(h = 70, r1 = 11, r2 = 11, center = true);
translate([0,0,35]) cylinder(h = 50, r1 = 35, r2 = 35, center = true);
standoffs_cutout(28,28,0, 1.35);
standoffs_cutout(28,-28,0, 1.35);
standoffs_cutout(-28,28,0, 1.35);
standoffs_cutout(-28,-28,0, 1.35);
}
//translate([0,0,-30]) cube(size = [28,28,28], center = true);
difference(){
translate([0,0,5]) cylinder(h = 10, r1 = 26, r2 = 26, center = true);
translate([0,0,5]) cylinder(h = 10, r1 = 24, r2 = 24, center = true);
}

standoffs(28,28);
standoffs(28,-28);
standoffs(-28,28);
standoffs(-28,-28);
