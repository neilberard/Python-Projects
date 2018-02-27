//Maya ASCII 2017 scene
//Name: Diamond3D.ma
//Last modified: Mon, Feb 26, 2018 10:04:43 PM
//Codeset: 1252
requires maya "2017";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "Diamond3d";
	rename -uid "CC1E8881-4E1B-2D9E-A076-58A1FC095783";
createNode nurbsCurve -n "Diamond3dShape" -p "Diamond3d";
	rename -uid "3A82BD23-4190-5292-8495-989F535F2E8E";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 12 0 no 3
		13 0 1 4 7 10 13 14 17 20 21 24 27 28
		13
		-3.0325061668053468e-007 0 6.9375654392688588
		-6.9375654392688588 0 -6.0650123336106935e-007
		0 6.9375654392688588 0
		-3.0325061668053468e-007 0 6.9375654392688588
		0 -6.9375654392688588 0
		-6.9375654392688588 0 -6.0650123336106935e-007
		9.0975180074723671e-007 0 -6.9375654392688588
		0 -6.9375654392688588 0
		6.9375654392688588 0 0
		9.0975180074723671e-007 0 -6.9375654392688588
		0 6.9375654392688588 0
		6.9375654392688588 0 0
		-3.0325061668053468e-007 0 6.9375654392688588
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
// End of Diamond3D.ma
