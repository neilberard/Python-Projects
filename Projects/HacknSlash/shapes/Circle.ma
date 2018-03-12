//Maya ASCII 2017 scene
//Name: Circle.ma
//Last modified: Tue, Feb 27, 2018 08:55:07 PM
//Codeset: 1252
requires maya "2017";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "circle";
	rename -uid "2B4C77A3-4975-0443-6EB4-F8BE0B881CA5";
createNode nurbsCurve -n "circleShape" -p "circle";
	rename -uid "EA1735A9-40EB-4572-5564-9FA1BC648879";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		6.1905318366406785 3.7906074993808902e-016 -6.1905318366406688
		-9.9881047801851676e-016 5.3607285352576218e-016 -8.7547340816796648
		-6.1905318366406723 3.7906074993808926e-016 -6.1905318366406723
		-8.7547340816796648 1.5534050146788411e-031 -2.5369029107174119e-015
		-6.1905318366406741 -3.7906074993808916e-016 6.1905318366406705
		-2.6379722372365103e-015 -5.3607285352576228e-016 8.7547340816796666
		6.1905318366406688 -3.7906074993808931e-016 6.1905318366406732
		8.7547340816796648 -2.8792577536447858e-031 4.7021847534316626e-015
		6.1905318366406785 3.7906074993808902e-016 -6.1905318366406688
		-9.9881047801851676e-016 5.3607285352576218e-016 -8.7547340816796648
		-6.1905318366406723 3.7906074993808926e-016 -6.1905318366406723
		;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
	setAttr ".fs" 1;
	setAttr ".ef" 10;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
// End of Circle.ma
