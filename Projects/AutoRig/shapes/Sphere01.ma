//Maya ASCII 2017 scene
//Name: Sphere01.ma
//Last modified: Mon, Feb 26, 2018 10:02:57 PM
//Codeset: 1252
requires maya "2017";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -n "Sphere01";
	rename -uid "CC1E8881-4E1B-2D9E-A076-58A1FC095783";
createNode nurbsCurve -n "Sphere01Shape" -p "Sphere01";
	rename -uid "3A82BD23-4190-5292-8495-989F535F2E8E";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 0.54075830049999996 1 2 3 4 5 6 7 8 9 10 11 12 13 13.50934634 14 15 16
		 17 18 19 20 20.412581289999999 21 22 23 24 25 26 27 27.523213299999998 28
		33
		-3.0325061668053468e-007 0 6.9375654392688588
		-4.9055990695655556 0 4.9055990695655556
		-6.9375654392688588 0 -6.0650123336106935e-007
		-6.0081082164999922 3.4687825128788674 -5.252454828336855e-007
		-3.4687827196344294 6.0081078029888682 -3.0325061668053468e-007
		0 6.9375654392688588 0
		-1.5162530834026734e-007 6.0081078029888682 3.4687827196344294
		-2.6262274141684275e-007 3.4687825128788674 6.0081082164999922
		-3.0325061668053468e-007 0 6.9375654392688588
		-2.6262274141684275e-007 -3.4687825128788674 6.0081082164999922
		-1.5162530834026734e-007 -6.0081078029888682 3.4687827196344294
		0 -6.9375654392688588 0
		-3.4687827196344294 -6.0081078029888682 -3.0325061668053468e-007
		-6.0081082164999922 -3.4687825128788674 -5.252454828336855e-007
		-6.9375654392688588 0 -6.0650123336106935e-007
		-4.9055990695655556 0 -4.9055990695655556
		9.0975180074723671e-007 0 -6.9375654392688588
		7.8786822425052825e-007 -3.4687825128788674 -6.0081082164999922
		4.5487590037361836e-007 -6.0081078029888682 -3.4687827196344294
		0 -6.9375654392688588 0
		3.4687827196344294 -6.0081078029888682 0
		6.0081082164999922 -3.4687825128788674 0
		6.9375654392688588 0 0
		4.9055990695655556 0 -4.9055990695655556
		9.0975180074723671e-007 0 -6.9375654392688588
		7.8786822425052825e-007 3.4687825128788674 -6.0081082164999922
		4.5487590037361836e-007 6.0081078029888682 -3.4687827196344294
		0 6.9375654392688588 0
		3.4687827196344294 6.0081078029888682 0
		6.0081082164999922 3.4687825128788674 0
		6.9375654392688588 0 0
		4.9055994830766787 0 4.9055994830766787
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
// End of Sphere01.ma
