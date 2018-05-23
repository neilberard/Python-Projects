//Maya ASCII 2017 scene
//Name: Foot01.ma
//Last modified: Mon, Feb 26, 2018 09:41:45 PM
//Codeset: 1252
requires maya "2017";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "Foot01";
	rename -uid "33142804-48D3-9631-4F0D-6686CE3F4954";
	setAttr ".rp" -type "double3" 4.4408920985006262e-016 0 0 ;
	setAttr ".sp" -type "double3" 4.4408920985006262e-016 0 0 ;
createNode nurbsCurve -n "Foot01Shape" -p "Foot01";
	rename -uid "F96E934E-422F-8846-738F-67BACE05C1A5";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-3.5349340177160538 0 -5.3024010265740822
		-1.5710817856515815 0 5.3024010265740822
		-1.1783113392386864 0 6.4807123658127681
		-1.3322676295501878e-015 0 6.8734828122256628
		1.1783113392386837 0 6.480712365812769
		1.5710817856515789 0 5.3024010265740831
		3.5349340177160569 0 -5.3024010265740813
		1.3322676295501878e-015 0 -6.8734828122256628
		-3.5349340177160538 0 -5.3024010265740822
		-1.5710817856515815 0 5.3024010265740822
		-1.1783113392386864 0 6.4807123658127681
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
// End of Foot01.ma
