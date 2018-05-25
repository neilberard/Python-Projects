//Maya ASCII 2017 scene
//Name: Arrows01.ma
//Last modified: Mon, Feb 26, 2018 08:43:17 PM
//Codeset: 1252
requires maya "2017";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "Arrows01";
	rename -uid "ECCFB682-4A2D-E277-F715-8EBA13951CBD";
createNode nurbsCurve -n "Arrows0Shape1" -p "Arrows01";
	rename -uid "1D910533-48B7-3797-8626-EC94CE4A20BE";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 36 0 no 3
		37 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
		 28 29 30 31 32 33 34 35 36
		37
		-2 0 4
		-4 0 2
		-4 0 1
		-6 0 1
		-6 0 2
		-8 0 0
		-6 0 -2
		-6 0 -1
		-4 0 -1
		-4 0 -2
		-2 0 -4
		-1 0 -4
		-1 0 -6
		-2 0 -6
		0 0 -8
		2 0 -6
		1 0 -6
		1 0 -4
		2 0 -4
		4 0 -2
		4 0 -1
		6 0 -1
		6 0 -2
		8 0 0
		6 0 2
		6 0 1
		4 0 1
		4 0 2
		2 0 4
		1 0 4
		1 0 6
		2 0 6
		0 0 8
		-2 0 6
		-1 0 6
		-1 0 4
		-2 0 4
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
// End of Arrows01.ma
