//Maya ASCII 2017 scene
//Name: IKFK_ARM.ma
//Last modified: Mon, Mar 12, 2018 11:51:48 PM
//Codeset: 1252
requires maya "2017";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201608291545-1001872";
fileInfo "osv" "Microsoft Windows 8 Home Premium Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "700A0832-4A8C-2A2D-C403-ABB1D3A75C1E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 5.7292732352220392 34.371452424278878 7.4247062632246905 ;
	setAttr ".r" -type "double3" -70.538352729612512 16.200000000000603 -1.6560322789280067e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "F130A92F-422B-CE7E-607C-FA814B6E29CD";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 35.691906508411549;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "C3889D57-465E-C2F1-3311-D088EE0F9FC5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "14F39DA6-4512-C49C-BD58-6E9C372FFFB1";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "7B9E3F40-4470-AA77-0E35-C59503B60703";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "2D1704B2-4CCE-70FB-B26D-3F865D17CAC8";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "58DA28CD-4179-09FC-7EBD-C5B2D701C29D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "B872700A-4691-97B8-1E80-20AE62679664";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode joint -n "joint1";
	rename -uid "A8E99E22-464E-57D8-5007-3D9CEB20EE87";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
createNode joint -n "joint2" -p "joint1";
	rename -uid "B39ABF41-4E3C-99CB-2383-73A4FB606D41";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
createNode joint -n "joint3" -p "joint2";
	rename -uid "877D09F2-44AE-664F-194D-9A9846BF5A0A";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
createNode pointConstraint -n "joint3_pointConstraint1" -p "joint3";
	rename -uid "1B8856AE-4F83-7D16-374D-3888D8B63A61";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint3_FKW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "joint3_IKW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".rst" -type "double3" 2 0 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr ".Utility" -type "string" "IKFK";
createNode orientConstraint -n "joint3_orientConstraint1" -p "joint3";
	rename -uid "3C8FB810-4EEB-F826-7FD2-B3A5E1DFED48";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint3_FKW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "joint3_IKW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr ".Utility" -type "string" "IKFK";
createNode pointConstraint -n "joint2_pointConstraint1" -p "joint2";
	rename -uid "0525575A-4864-4D85-58A4-F19818510436";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint2_FKW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "joint2_IKW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".rst" -type "double3" 2 0 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr ".Utility" -type "string" "IKFK";
createNode orientConstraint -n "joint2_orientConstraint1" -p "joint2";
	rename -uid "C446EF8E-4454-7DA2-D019-C29AD4965875";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint2_FKW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "joint2_IKW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".lr" -type "double3" 0 1.7689806827882651e-005 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr ".Utility" -type "string" "IKFK";
createNode pointConstraint -n "joint1_pointConstraint1" -p "joint1";
	rename -uid "43C69B22-4C83-8E18-79ED-BFBDC52B5367";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint1_FKW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "joint1_IKW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr ".rst" -type "double3" -2 0 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr ".Utility" -type "string" "IKFK";
createNode orientConstraint -n "joint1_orientConstraint1" -p "joint1";
	rename -uid "84154545-40AE-7DA1-3C86-8C8B495BE3D6";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint1_FKW0" -dv 1 -min 0 -at "double";
	addAttr -dcb 0 -ci true -k true -sn "w1" -ln "joint1_IKW1" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -s 2 ".tg";
	setAttr -k on ".w0";
	setAttr -k on ".w1";
	setAttr ".Utility" -type "string" "IKFK";
createNode joint -n "joint1_FK";
	rename -uid "1DB403E5-4C53-81E1-854B-4090D06F3579";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
	setAttr ".Utility" -type "string" "FK";
createNode joint -n "joint2_FK" -p "joint1_FK";
	rename -uid "A2C2158A-4A4D-9173-962D-F29302C45144";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
	setAttr ".Utility" -type "string" "FK";
createNode joint -n "joint3_FK" -p "joint2_FK";
	rename -uid "59B94844-42DE-1175-8AB0-87B61918032B";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
	setAttr ".Utility" -type "string" "FK";
createNode parentConstraint -n "joint3_FK_parentConstraint1" -p "joint3_FK";
	rename -uid "32D7953B-4DC6-5D15-BA43-AD8F039C9F32";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint3_CTRLW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 2 0 0 ;
	setAttr -k on ".w0";
createNode parentConstraint -n "joint2_FK_parentConstraint1" -p "joint2_FK";
	rename -uid "0057373C-491F-8608-91BE-3192B0C90DBD";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint2_CTRLW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 2 0 0 ;
	setAttr -k on ".w0";
createNode parentConstraint -n "joint1_FK_parentConstraint1" -p "joint1_FK";
	rename -uid "B6A3D4C3-414D-B5B7-FCB2-438AC85B5064";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "joint1_CTRLW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" -2 0 0 ;
	setAttr -k on ".w0";
createNode joint -n "joint1_IK";
	rename -uid "6168D018-4F80-4F64-CC2D-68BE135C2E88";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".t" -type "double3" -2 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
	setAttr ".Utility" -type "string" "IK";
createNode joint -n "joint2_IK" -p "joint1_IK";
	rename -uid "456EE654-4A5B-367E-0643-BCB121D606C6";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".t" -type "double3" 2 0 0 ;
	setAttr ".r" -type "double3" 0 3.537961365576531e-005 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" 0 90 0 ;
	setAttr ".radi" 0.55172413793103448;
	setAttr ".Utility" -type "string" "IK";
createNode joint -n "joint3_IK" -p "joint2_IK";
	rename -uid "7171F953-4649-F528-7395-5FB7A2284DE7";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".t" -type "double3" 2 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
	setAttr ".Utility" -type "string" "IK";
createNode ikEffector -n "effector1" -p "joint2_IK";
	rename -uid "E2B7B4FF-45AF-50FA-2A7D-2F8D7A5BA8EA";
	setAttr ".v" no;
	setAttr ".hd" yes;
createNode ikHandle -n "ikHandle1";
	rename -uid "757C0F9E-44BE-6D17-BE18-1B96D069F22E";
	setAttr ".roc" yes;
createNode parentConstraint -n "ikHandle1_parentConstraint1" -p "ikHandle1";
	rename -uid "4E552254-4717-FD45-84C1-678B5BB2BD60";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "ikHandle1_CTRLW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 1.9999999999996187 0 -1.2349814927532262e-006 ;
	setAttr -k on ".w0";
createNode poleVectorConstraint -n "ikHandle1_poleVectorConstraint1" -p "ikHandle1";
	rename -uid "F2591C4D-420B-1CBE-B5E7-1B97B54A32D8";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "locator1W0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".rst" -type "double3" 2 0 2 ;
	setAttr -k on ".w0";
createNode transform -n "ikHandle1_GRP";
	rename -uid "BBC096D3-4291-7942-F9B0-F58D7182FDB0";
	setAttr ".t" -type "double3" 1.9999999999996187 0 -1.2349814927532262e-006 ;
createNode transform -n "ikHandle1_CTRL" -p "ikHandle1_GRP";
	rename -uid "2B0D0A9E-4CA9-6A6C-8B28-CEB5ABC7BA5B";
createNode nurbsCurve -n "ikHandle1_CTRLShape" -p "ikHandle1_CTRL";
	rename -uid "1820A8B8-4591-5921-4C9C-A69A8CBEC424";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 0.54075830049999996 1 2 3 4 5 6 7 8 9 10 11 12 13 13.50934634 14 15 16
		 17 18 19 20 20.412581289999999 21 22 23 24 25 26 27 27.523213299999998 28
		33
		2.2204459145799863e-016 -6.0650123336106948e-008 1.3875130878537718
		4.1922434605742953e-018 -0.98111981391311132 0.98111981391311121
		-8.604519049576971e-017 -1.3875130878537723 -1.2130024667221387e-007
		-0.6937565025757737 -1.2016216432999987 -1.050490965667371e-007
		-1.201621560597774 -0.69375654392688579 -6.0650123336106935e-008
		-1.387513087853772 3.0808979542080102e-016 0
		-1.2016215605977738 -3.0325061401239889e-008 0.6937565439268859
		-0.69375650257577348 -5.2524548129323677e-008 1.2016216432999984
		2.2204459145799863e-016 -6.0650123336106948e-008 1.3875130878537718
		0.69375650257577393 -5.2524548437413449e-008 1.2016216432999984
		1.2016215605977743 -3.0325061934867059e-008 0.6937565439268859
		1.3875130878537725 -3.0808979542080102e-016 0
		1.201621560597774 -0.69375654392688635 -6.0650123336106935e-008
		0.6937565025757737 -1.2016216432999991 -1.050490965667371e-007
		-8.604519049576971e-017 -1.3875130878537723 -1.2130024667221387e-007
		4.1922434605742953e-018 -0.98111981391311132 -0.98111981391311121
		2.2204464532612714e-016 1.8195036014944739e-007 -1.3875130878537718
		0.69375650257577393 1.5757364469606082e-007 -1.2016216432999984
		1.2016215605977743 9.0975179807910103e-008 -0.6937565439268859
		1.3875130878537725 -3.0808979542080102e-016 0
		1.2016215605977745 0.69375654392688579 0
		0.69375650257577415 1.2016216432999987 0
		5.3013440034583228e-016 1.3875130878537723 0
		4.3989696638948832e-016 0.98111981391311132 -0.98111981391311121
		2.2204464532612714e-016 1.8195036014944739e-007 -1.3875130878537718
		-0.69375650257577348 1.5757364500415058e-007 -1.2016216432999984
		-1.2016215605977738 9.0975180341537287e-008 -0.6937565439268859
		-1.387513087853772 3.0808979542080102e-016 0
		-1.2016215605977736 0.69375654392688635 0
		-0.69375650257577326 1.2016216432999991 0
		5.3013440034583228e-016 1.3875130878537723 0
		4.3989698475307111e-016 0.98111989661533594 0.98111989661533583
		2.2204459145799863e-016 -6.0650123336106948e-008 1.3875130878537718
		;
createNode transform -n "Pole";
	rename -uid "B152B408-4292-DAE0-ECEB-D599EB582A53";
	setAttr ".t" -type "double3" 0 0 2 ;
createNode locator -n "PoleShape" -p "Pole";
	rename -uid "07D26159-49EF-A868-1ABF-95AD6A7FF492";
	setAttr -k off ".v";
createNode transform -n "joint1_GRP";
	rename -uid "6C59B500-43C2-9787-FD99-42867B1B2877";
	setAttr ".t" -type "double3" -2 0 0 ;
createNode transform -n "joint1_CTRL" -p "joint1_GRP";
	rename -uid "5B3BDADC-43CE-5460-3291-4E8389648D81";
	addAttr -ci true -sn "Index" -ln "Index" -dt "string";
	addAttr -ci true -sn "Name" -ln "Name" -dt "string";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Joint" -ln "Joint" -dt "string";
	addAttr -ci true -sn "Type" -ln "Type" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".Name" -type "string" "joint2";
	setAttr ".Type" -type "string" "CTRL";
	setAttr ".Utility" -type "string" "FK";
createNode nurbsCurve -n "joint1_CTRLShape" -p "joint1_CTRL";
	rename -uid "F7CE4054-4051-6321-22B8-12AED4833DF9";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		0 0 -0.95999999999999996
		2.1316282072803005e-016 0.96000000000000019 0
		0 0 0.95999999999999996
		-2.1316282072803005e-016 -0.96000000000000019 0
		0 0 -0.95999999999999996
		;
createNode transform -n "joint2_GRP" -p "joint1_CTRL";
	rename -uid "8BA52DF0-42E6-7B83-5676-D09354EEFA5B";
	setAttr ".t" -type "double3" 2 0 0 ;
createNode transform -n "joint2_CTRL" -p "joint2_GRP";
	rename -uid "E495028A-4A91-455D-0497-0A9604E8242B";
	addAttr -ci true -sn "Index" -ln "Index" -dt "string";
	addAttr -ci true -sn "Name" -ln "Name" -dt "string";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Joint" -ln "Joint" -dt "string";
	addAttr -ci true -sn "Type" -ln "Type" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".Name" -type "string" "joint2";
	setAttr ".Type" -type "string" "CTRL";
	setAttr ".Utility" -type "string" "FK";
createNode nurbsCurve -n "joint2_CTRLShape" -p "joint2_CTRL";
	rename -uid "A494F44C-4D88-7766-24CB-B2B4789A3B09";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		0 0 -0.95999999999999996
		2.1316282072803005e-016 0.96000000000000019 0
		0 0 0.95999999999999996
		-2.1316282072803005e-016 -0.96000000000000019 0
		0 0 -0.95999999999999996
		;
createNode transform -n "joint3_GRP" -p "joint2_CTRL";
	rename -uid "A45CA9E1-4FAF-078F-0B82-37942C2207A4";
	setAttr ".t" -type "double3" 2 0 0 ;
createNode transform -n "joint3_CTRL" -p "joint3_GRP";
	rename -uid "431BDA43-4E83-9906-BCBA-8191469DA8A3";
	addAttr -ci true -sn "Index" -ln "Index" -dt "string";
	addAttr -ci true -sn "Name" -ln "Name" -dt "string";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Joint" -ln "Joint" -dt "string";
	addAttr -ci true -sn "Type" -ln "Type" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	addAttr -ci true -sn "Utility" -ln "Utility" -dt "string";
	setAttr ".Name" -type "string" "joint2";
	setAttr ".Type" -type "string" "CTRL";
	setAttr ".Utility" -type "string" "FK";
createNode nurbsCurve -n "joint3_CTRLShape" -p "joint3_CTRL";
	rename -uid "0188C524-4475-589A-70E2-0B906A3CDFAF";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		0 0 -0.95999999999999996
		2.1316282072803005e-016 0.96000000000000019 0
		0 0 0.95999999999999996
		-2.1316282072803005e-016 -0.96000000000000019 0
		0 0 -0.95999999999999996
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "A488A98A-4BF8-CE9D-5E39-EF8D77A32D0E";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "37844813-4D2A-D881-7901-D1A43E1FB0B8";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "F97E7496-4CB6-DF97-9C59-84903A0BD806";
createNode displayLayerManager -n "layerManager";
	rename -uid "D003EBAF-445D-77CE-DD58-85B2B0FF4604";
createNode displayLayer -n "defaultLayer";
	rename -uid "1035DDA0-4DFD-5E01-1114-9DB22F8D4C17";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "FAC089A8-4A83-0292-E979-679193C496BE";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "62987643-4E7B-DFBE-7163-499FC083AE6E";
	setAttr ".g" yes;
createNode network -n "temp";
	rename -uid "84CAA70B-4BA6-CF95-091F-DCA5E6B4DF74";
	addAttr -s false -ci true -m -sn "IK" -ln "IK" -at "message";
	addAttr -s false -ci true -m -sn "FK" -ln "FK" -at "message";
	addAttr -s false -ci true -m -sn "IK_CTRL" -ln "IK_CTRL" -at "message";
	addAttr -s false -ci true -m -sn "FK_CTRL" -ln "FK_CTRL" -at "message";
	addAttr -s false -ci true -m -sn "OrientConstraint" -ln "OrientConstraint" -at "message";
	addAttr -s false -ci true -m -sn "PointConstraint" -ln "PointConstraint" -at "message";
	addAttr -ci true -sn "Region" -ln "Region" -dt "string";
	addAttr -ci true -sn "Type" -ln "Type" -dt "string";
	addAttr -ci true -sn "Side" -ln "Side" -dt "string";
	setAttr -s 3 ".IK";
	setAttr -s 3 ".FK";
	setAttr -s 3 ".OrientConstraint";
	setAttr -s 3 ".PointConstraint";
	setAttr ".Region" -type "string" "Arm";
	setAttr ".Type" -type "string" "IKFK";
	setAttr ".Side" -type "string" "Left";
createNode ikRPsolver -n "ikRPsolver";
	rename -uid "D7C263CE-4B45-749B-2F71-54AD0428409D";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "5ED52A1C-4895-FDD0-D0B3-ACA5F3CA0D60";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1001\n                -height 713\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n"
		+ "            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1001\n            -height 713\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1001\\n    -height 713\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1001\\n    -height 713\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "2BE93D34-4367-DD17-6728-FDB1DCD8F868";
	setAttr ".b" -type "string" "playbackOptions -min 0 -max 60 -ast 0 -aet 120 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "3C85D137-4BF4-3724-A93E-09929AF0E3EE";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 441.49156789410574 -315.27951769985674 ;
	setAttr ".tgi[0].vh" -type "double2" 1234.2473832405344 80.32117838968459 ;
	setAttr -s 7 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 1043.53076171875;
	setAttr ".tgi[0].ni[0].y" -78.688240051269531;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1486.387939453125;
	setAttr ".tgi[0].ni[1].y" -78.688240051269531;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 898.36090087890625;
	setAttr ".tgi[0].ni[2].y" -80.684539794921875;
	setAttr ".tgi[0].ni[2].nvs" 18306;
	setAttr ".tgi[0].ni[3].x" 379.24505615234375;
	setAttr ".tgi[0].ni[3].y" -78.688240051269531;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 822.1021728515625;
	setAttr ".tgi[0].ni[4].y" -78.688240051269531;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 1264.9593505859375;
	setAttr ".tgi[0].ni[5].y" -78.688240051269531;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 561.33880615234375;
	setAttr ".tgi[0].ni[6].y" 9.8050394058227539;
	setAttr ".tgi[0].ni[6].nvs" 18306;
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
connectAttr "joint1_pointConstraint1.ctx" "joint1.tx";
connectAttr "joint1_pointConstraint1.cty" "joint1.ty";
connectAttr "joint1_pointConstraint1.ctz" "joint1.tz";
connectAttr "joint1_orientConstraint1.crx" "joint1.rx";
connectAttr "joint1_orientConstraint1.cry" "joint1.ry";
connectAttr "joint1_orientConstraint1.crz" "joint1.rz";
connectAttr "joint1.s" "joint2.is";
connectAttr "joint2_pointConstraint1.ctx" "joint2.tx";
connectAttr "joint2_pointConstraint1.cty" "joint2.ty";
connectAttr "joint2_pointConstraint1.ctz" "joint2.tz";
connectAttr "joint2_orientConstraint1.crx" "joint2.rx";
connectAttr "joint2_orientConstraint1.cry" "joint2.ry";
connectAttr "joint2_orientConstraint1.crz" "joint2.rz";
connectAttr "joint2.s" "joint3.is";
connectAttr "joint3_pointConstraint1.ctx" "joint3.tx";
connectAttr "joint3_pointConstraint1.cty" "joint3.ty";
connectAttr "joint3_pointConstraint1.ctz" "joint3.tz";
connectAttr "joint3_orientConstraint1.crx" "joint3.rx";
connectAttr "joint3_orientConstraint1.cry" "joint3.ry";
connectAttr "joint3_orientConstraint1.crz" "joint3.rz";
connectAttr "joint3.pim" "joint3_pointConstraint1.cpim";
connectAttr "joint3.rp" "joint3_pointConstraint1.crp";
connectAttr "joint3.rpt" "joint3_pointConstraint1.crt";
connectAttr "joint3_FK.t" "joint3_pointConstraint1.tg[0].tt";
connectAttr "joint3_FK.rp" "joint3_pointConstraint1.tg[0].trp";
connectAttr "joint3_FK.rpt" "joint3_pointConstraint1.tg[0].trt";
connectAttr "joint3_FK.pm" "joint3_pointConstraint1.tg[0].tpm";
connectAttr "joint3_pointConstraint1.w0" "joint3_pointConstraint1.tg[0].tw";
connectAttr "joint3_IK.t" "joint3_pointConstraint1.tg[1].tt";
connectAttr "joint3_IK.rp" "joint3_pointConstraint1.tg[1].trp";
connectAttr "joint3_IK.rpt" "joint3_pointConstraint1.tg[1].trt";
connectAttr "joint3_IK.pm" "joint3_pointConstraint1.tg[1].tpm";
connectAttr "joint3_pointConstraint1.w1" "joint3_pointConstraint1.tg[1].tw";
connectAttr "joint3.ro" "joint3_orientConstraint1.cro";
connectAttr "joint3.pim" "joint3_orientConstraint1.cpim";
connectAttr "joint3.jo" "joint3_orientConstraint1.cjo";
connectAttr "joint3.is" "joint3_orientConstraint1.is";
connectAttr "joint3_FK.r" "joint3_orientConstraint1.tg[0].tr";
connectAttr "joint3_FK.ro" "joint3_orientConstraint1.tg[0].tro";
connectAttr "joint3_FK.pm" "joint3_orientConstraint1.tg[0].tpm";
connectAttr "joint3_FK.jo" "joint3_orientConstraint1.tg[0].tjo";
connectAttr "joint3_orientConstraint1.w0" "joint3_orientConstraint1.tg[0].tw";
connectAttr "joint3_IK.r" "joint3_orientConstraint1.tg[1].tr";
connectAttr "joint3_IK.ro" "joint3_orientConstraint1.tg[1].tro";
connectAttr "joint3_IK.pm" "joint3_orientConstraint1.tg[1].tpm";
connectAttr "joint3_IK.jo" "joint3_orientConstraint1.tg[1].tjo";
connectAttr "joint3_orientConstraint1.w1" "joint3_orientConstraint1.tg[1].tw";
connectAttr "joint2.pim" "joint2_pointConstraint1.cpim";
connectAttr "joint2.rp" "joint2_pointConstraint1.crp";
connectAttr "joint2.rpt" "joint2_pointConstraint1.crt";
connectAttr "joint2_FK.t" "joint2_pointConstraint1.tg[0].tt";
connectAttr "joint2_FK.rp" "joint2_pointConstraint1.tg[0].trp";
connectAttr "joint2_FK.rpt" "joint2_pointConstraint1.tg[0].trt";
connectAttr "joint2_FK.pm" "joint2_pointConstraint1.tg[0].tpm";
connectAttr "joint2_pointConstraint1.w0" "joint2_pointConstraint1.tg[0].tw";
connectAttr "joint2_IK.t" "joint2_pointConstraint1.tg[1].tt";
connectAttr "joint2_IK.rp" "joint2_pointConstraint1.tg[1].trp";
connectAttr "joint2_IK.rpt" "joint2_pointConstraint1.tg[1].trt";
connectAttr "joint2_IK.pm" "joint2_pointConstraint1.tg[1].tpm";
connectAttr "joint2_pointConstraint1.w1" "joint2_pointConstraint1.tg[1].tw";
connectAttr "joint2.ro" "joint2_orientConstraint1.cro";
connectAttr "joint2.pim" "joint2_orientConstraint1.cpim";
connectAttr "joint2.jo" "joint2_orientConstraint1.cjo";
connectAttr "joint2.is" "joint2_orientConstraint1.is";
connectAttr "joint2_FK.r" "joint2_orientConstraint1.tg[0].tr";
connectAttr "joint2_FK.ro" "joint2_orientConstraint1.tg[0].tro";
connectAttr "joint2_FK.pm" "joint2_orientConstraint1.tg[0].tpm";
connectAttr "joint2_FK.jo" "joint2_orientConstraint1.tg[0].tjo";
connectAttr "joint2_orientConstraint1.w0" "joint2_orientConstraint1.tg[0].tw";
connectAttr "joint2_IK.r" "joint2_orientConstraint1.tg[1].tr";
connectAttr "joint2_IK.ro" "joint2_orientConstraint1.tg[1].tro";
connectAttr "joint2_IK.pm" "joint2_orientConstraint1.tg[1].tpm";
connectAttr "joint2_IK.jo" "joint2_orientConstraint1.tg[1].tjo";
connectAttr "joint2_orientConstraint1.w1" "joint2_orientConstraint1.tg[1].tw";
connectAttr "joint1.pim" "joint1_pointConstraint1.cpim";
connectAttr "joint1.rp" "joint1_pointConstraint1.crp";
connectAttr "joint1.rpt" "joint1_pointConstraint1.crt";
connectAttr "joint1_FK.t" "joint1_pointConstraint1.tg[0].tt";
connectAttr "joint1_FK.rp" "joint1_pointConstraint1.tg[0].trp";
connectAttr "joint1_FK.rpt" "joint1_pointConstraint1.tg[0].trt";
connectAttr "joint1_FK.pm" "joint1_pointConstraint1.tg[0].tpm";
connectAttr "joint1_pointConstraint1.w0" "joint1_pointConstraint1.tg[0].tw";
connectAttr "joint1_IK.t" "joint1_pointConstraint1.tg[1].tt";
connectAttr "joint1_IK.rp" "joint1_pointConstraint1.tg[1].trp";
connectAttr "joint1_IK.rpt" "joint1_pointConstraint1.tg[1].trt";
connectAttr "joint1_IK.pm" "joint1_pointConstraint1.tg[1].tpm";
connectAttr "joint1_pointConstraint1.w1" "joint1_pointConstraint1.tg[1].tw";
connectAttr "joint1.ro" "joint1_orientConstraint1.cro";
connectAttr "joint1.pim" "joint1_orientConstraint1.cpim";
connectAttr "joint1.jo" "joint1_orientConstraint1.cjo";
connectAttr "joint1.is" "joint1_orientConstraint1.is";
connectAttr "joint1_FK.r" "joint1_orientConstraint1.tg[0].tr";
connectAttr "joint1_FK.ro" "joint1_orientConstraint1.tg[0].tro";
connectAttr "joint1_FK.pm" "joint1_orientConstraint1.tg[0].tpm";
connectAttr "joint1_FK.jo" "joint1_orientConstraint1.tg[0].tjo";
connectAttr "joint1_orientConstraint1.w0" "joint1_orientConstraint1.tg[0].tw";
connectAttr "joint1_IK.r" "joint1_orientConstraint1.tg[1].tr";
connectAttr "joint1_IK.ro" "joint1_orientConstraint1.tg[1].tro";
connectAttr "joint1_IK.pm" "joint1_orientConstraint1.tg[1].tpm";
connectAttr "joint1_IK.jo" "joint1_orientConstraint1.tg[1].tjo";
connectAttr "joint1_orientConstraint1.w1" "joint1_orientConstraint1.tg[1].tw";
connectAttr "joint1_FK_parentConstraint1.ctx" "joint1_FK.tx";
connectAttr "joint1_FK_parentConstraint1.cty" "joint1_FK.ty";
connectAttr "joint1_FK_parentConstraint1.ctz" "joint1_FK.tz";
connectAttr "joint1_FK_parentConstraint1.crx" "joint1_FK.rx";
connectAttr "joint1_FK_parentConstraint1.cry" "joint1_FK.ry";
connectAttr "joint1_FK_parentConstraint1.crz" "joint1_FK.rz";
connectAttr "joint1_FK.s" "joint2_FK.is";
connectAttr "joint2_FK_parentConstraint1.ctx" "joint2_FK.tx";
connectAttr "joint2_FK_parentConstraint1.cty" "joint2_FK.ty";
connectAttr "joint2_FK_parentConstraint1.ctz" "joint2_FK.tz";
connectAttr "joint2_FK_parentConstraint1.crx" "joint2_FK.rx";
connectAttr "joint2_FK_parentConstraint1.cry" "joint2_FK.ry";
connectAttr "joint2_FK_parentConstraint1.crz" "joint2_FK.rz";
connectAttr "joint2_FK.s" "joint3_FK.is";
connectAttr "joint3_FK_parentConstraint1.ctx" "joint3_FK.tx";
connectAttr "joint3_FK_parentConstraint1.cty" "joint3_FK.ty";
connectAttr "joint3_FK_parentConstraint1.ctz" "joint3_FK.tz";
connectAttr "joint3_FK_parentConstraint1.crx" "joint3_FK.rx";
connectAttr "joint3_FK_parentConstraint1.cry" "joint3_FK.ry";
connectAttr "joint3_FK_parentConstraint1.crz" "joint3_FK.rz";
connectAttr "joint3_FK.ro" "joint3_FK_parentConstraint1.cro";
connectAttr "joint3_FK.pim" "joint3_FK_parentConstraint1.cpim";
connectAttr "joint3_FK.rp" "joint3_FK_parentConstraint1.crp";
connectAttr "joint3_FK.rpt" "joint3_FK_parentConstraint1.crt";
connectAttr "joint3_FK.jo" "joint3_FK_parentConstraint1.cjo";
connectAttr "joint3_CTRL.t" "joint3_FK_parentConstraint1.tg[0].tt";
connectAttr "joint3_CTRL.rp" "joint3_FK_parentConstraint1.tg[0].trp";
connectAttr "joint3_CTRL.rpt" "joint3_FK_parentConstraint1.tg[0].trt";
connectAttr "joint3_CTRL.r" "joint3_FK_parentConstraint1.tg[0].tr";
connectAttr "joint3_CTRL.ro" "joint3_FK_parentConstraint1.tg[0].tro";
connectAttr "joint3_CTRL.s" "joint3_FK_parentConstraint1.tg[0].ts";
connectAttr "joint3_CTRL.pm" "joint3_FK_parentConstraint1.tg[0].tpm";
connectAttr "joint3_FK_parentConstraint1.w0" "joint3_FK_parentConstraint1.tg[0].tw"
		;
connectAttr "joint2_FK.ro" "joint2_FK_parentConstraint1.cro";
connectAttr "joint2_FK.pim" "joint2_FK_parentConstraint1.cpim";
connectAttr "joint2_FK.rp" "joint2_FK_parentConstraint1.crp";
connectAttr "joint2_FK.rpt" "joint2_FK_parentConstraint1.crt";
connectAttr "joint2_FK.jo" "joint2_FK_parentConstraint1.cjo";
connectAttr "joint2_CTRL.t" "joint2_FK_parentConstraint1.tg[0].tt";
connectAttr "joint2_CTRL.rp" "joint2_FK_parentConstraint1.tg[0].trp";
connectAttr "joint2_CTRL.rpt" "joint2_FK_parentConstraint1.tg[0].trt";
connectAttr "joint2_CTRL.r" "joint2_FK_parentConstraint1.tg[0].tr";
connectAttr "joint2_CTRL.ro" "joint2_FK_parentConstraint1.tg[0].tro";
connectAttr "joint2_CTRL.s" "joint2_FK_parentConstraint1.tg[0].ts";
connectAttr "joint2_CTRL.pm" "joint2_FK_parentConstraint1.tg[0].tpm";
connectAttr "joint2_FK_parentConstraint1.w0" "joint2_FK_parentConstraint1.tg[0].tw"
		;
connectAttr "joint1_FK.ro" "joint1_FK_parentConstraint1.cro";
connectAttr "joint1_FK.pim" "joint1_FK_parentConstraint1.cpim";
connectAttr "joint1_FK.rp" "joint1_FK_parentConstraint1.crp";
connectAttr "joint1_FK.rpt" "joint1_FK_parentConstraint1.crt";
connectAttr "joint1_FK.jo" "joint1_FK_parentConstraint1.cjo";
connectAttr "joint1_CTRL.t" "joint1_FK_parentConstraint1.tg[0].tt";
connectAttr "joint1_CTRL.rp" "joint1_FK_parentConstraint1.tg[0].trp";
connectAttr "joint1_CTRL.rpt" "joint1_FK_parentConstraint1.tg[0].trt";
connectAttr "joint1_CTRL.r" "joint1_FK_parentConstraint1.tg[0].tr";
connectAttr "joint1_CTRL.ro" "joint1_FK_parentConstraint1.tg[0].tro";
connectAttr "joint1_CTRL.s" "joint1_FK_parentConstraint1.tg[0].ts";
connectAttr "joint1_CTRL.pm" "joint1_FK_parentConstraint1.tg[0].tpm";
connectAttr "joint1_FK_parentConstraint1.w0" "joint1_FK_parentConstraint1.tg[0].tw"
		;
connectAttr "joint1_IK.s" "joint2_IK.is";
connectAttr "joint2_IK.s" "joint3_IK.is";
connectAttr "joint3_IK.tx" "effector1.tx";
connectAttr "joint3_IK.ty" "effector1.ty";
connectAttr "joint3_IK.tz" "effector1.tz";
connectAttr "joint1_IK.msg" "ikHandle1.hsj";
connectAttr "effector1.hp" "ikHandle1.hee";
connectAttr "ikRPsolver.msg" "ikHandle1.hsv";
connectAttr "ikHandle1_parentConstraint1.ctx" "ikHandle1.tx";
connectAttr "ikHandle1_parentConstraint1.cty" "ikHandle1.ty";
connectAttr "ikHandle1_parentConstraint1.ctz" "ikHandle1.tz";
connectAttr "ikHandle1_parentConstraint1.crx" "ikHandle1.rx";
connectAttr "ikHandle1_parentConstraint1.cry" "ikHandle1.ry";
connectAttr "ikHandle1_parentConstraint1.crz" "ikHandle1.rz";
connectAttr "ikHandle1_poleVectorConstraint1.ctx" "ikHandle1.pvx";
connectAttr "ikHandle1_poleVectorConstraint1.cty" "ikHandle1.pvy";
connectAttr "ikHandle1_poleVectorConstraint1.ctz" "ikHandle1.pvz";
connectAttr "ikHandle1.ro" "ikHandle1_parentConstraint1.cro";
connectAttr "ikHandle1.pim" "ikHandle1_parentConstraint1.cpim";
connectAttr "ikHandle1.rp" "ikHandle1_parentConstraint1.crp";
connectAttr "ikHandle1.rpt" "ikHandle1_parentConstraint1.crt";
connectAttr "ikHandle1_CTRL.t" "ikHandle1_parentConstraint1.tg[0].tt";
connectAttr "ikHandle1_CTRL.rp" "ikHandle1_parentConstraint1.tg[0].trp";
connectAttr "ikHandle1_CTRL.rpt" "ikHandle1_parentConstraint1.tg[0].trt";
connectAttr "ikHandle1_CTRL.r" "ikHandle1_parentConstraint1.tg[0].tr";
connectAttr "ikHandle1_CTRL.ro" "ikHandle1_parentConstraint1.tg[0].tro";
connectAttr "ikHandle1_CTRL.s" "ikHandle1_parentConstraint1.tg[0].ts";
connectAttr "ikHandle1_CTRL.pm" "ikHandle1_parentConstraint1.tg[0].tpm";
connectAttr "ikHandle1_parentConstraint1.w0" "ikHandle1_parentConstraint1.tg[0].tw"
		;
connectAttr "ikHandle1.pim" "ikHandle1_poleVectorConstraint1.cpim";
connectAttr "joint1_IK.pm" "ikHandle1_poleVectorConstraint1.ps";
connectAttr "joint1_IK.t" "ikHandle1_poleVectorConstraint1.crp";
connectAttr "Pole.t" "ikHandle1_poleVectorConstraint1.tg[0].tt";
connectAttr "Pole.rp" "ikHandle1_poleVectorConstraint1.tg[0].trp";
connectAttr "Pole.rpt" "ikHandle1_poleVectorConstraint1.tg[0].trt";
connectAttr "Pole.pm" "ikHandle1_poleVectorConstraint1.tg[0].tpm";
connectAttr "ikHandle1_poleVectorConstraint1.w0" "ikHandle1_poleVectorConstraint1.tg[0].tw"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "joint1_FK.msg" "temp.FK[0]";
connectAttr "joint2_FK.msg" "temp.FK[1]";
connectAttr "joint3_FK.msg" "temp.FK[2]";
connectAttr "joint1_IK.msg" "temp.IK[0]";
connectAttr "joint2_IK.msg" "temp.IK[1]";
connectAttr "joint3_IK.msg" "temp.IK[2]";
connectAttr "joint1_pointConstraint1.msg" "temp.PointConstraint[0]";
connectAttr "joint2_pointConstraint1.msg" "temp.PointConstraint[1]";
connectAttr "joint3_pointConstraint1.msg" "temp.PointConstraint[2]";
connectAttr "joint1_pointConstraint1.msg" "temp.OrientConstraint[0]";
connectAttr "joint2_pointConstraint1.msg" "temp.OrientConstraint[1]";
connectAttr "joint3_pointConstraint1.msg" "temp.OrientConstraint[2]";
connectAttr "joint2_CTRL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "joint1_CTRL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn";
connectAttr "temp.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "joint3_CTRLShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "joint2_CTRLShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "joint1_CTRLShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "joint3_CTRL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "ikRPsolver.msg" ":ikSystem.sol" -na;
// End of IKFK_ARM.ma
