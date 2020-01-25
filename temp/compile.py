import cx_Freeze

executables = [cx_freeze.Executable("tutgameTEST.py")]
includefiles = ['manChanged/newbodyCarllFIXR/R1.png','manChanged/newbodyCarllFIXR/R2.png','manChanged/newbodyCarllFIXR/R3.png','manChanged/newbodyCarllFIXR/R4.png','manChanged/newbodyCarllFIXR/R5.png','manChanged/newbodyCarllFIXR/R6.png','manChanged/newbodyCarllFIXR/R7.png','manChanged/newbodyCarllFIXR/R8.png','manChanged/newbodyCarllFIXR/R9.png',
'manChanged/newbodyCarllFIX/L1','manChanged/newbodyCarllFIX/L2','manChanged/newbodyCarllFIX/L3','manChanged/newbodyCarllFIX/L4','manChanged/newbodyCarllFIX/L5','manChanged/newbodyCarllFIX/L6','manChanged/newbodyCarllFIX/L7','manChanged/newbodyCarllFIX/L8','manChanged/newbodyCarllFIX/L9',
'bg/cloudlvlLighter.jpg','manChanged/newpauseplain.jpg','MAINFILES/aha.jpg','MAINFILES/standing.png','manChanged/newpausetitle.jpg','manChanged/jumpL/J1L.png','manChanged/jumpL/J2L.png','manChanged/jumpL/J3L.png','manChanged/jumpR/J1R.png','manChanged/jumpR/J2R.png','manChanged/jumpR/J3R.png',
'other_fx/bubble_exploBIG/g_exp1.png','other_fx/bubble_exploBIG/g_exp2.png','other_fx/bubble_exploBIG/g_exp3.png','other_fx/bubble_exploBIG/g_exp4.png','other_fx/bubble_exploBIG/g_exp5.png','other_fx/bubble_exploBIG/g_exp6.png','other_fx/bubble_exploBIG/g_exp7.png','other_fx/bubble_exploBIG/g_exp8.png','other_fx/bubble_exploBIG/g_exp9.png','other_fx/bubble_exploBIG/g_exp10.png',
'audio/shoot.wav','audio/deathSound.wav','audio/fireMissile.wav','audio/mgSound.wav','audio/jumpSound.wav','audio/hit.wav','audio/music.mp3',
'MAINFILES/R1E.png','MAINFILES/R2E.png','MAINFILES/R3E.png','MAINFILES/R4E.png','MAINFILES/R5E.png','MAINFILES/R6E.png','MAINFILES/R7E.png','MAINFILES/R8E.png','MAINFILES/R9E.png','MAINFILES/R10E.png','MAINFILES/R11E.png',
'MAINFILES/L1E.png','MAINFILES/L2E.png','MAINFILES/L3E.png','MAINFILES/L4E.png','MAINFILES/L5E.png','MAINFILES/L6E.png','MAINFILES/L7E.png','MAINFILES/L8E.png','MAINFILES/L9E.png','MAINFILES/L10E.png','MAINFILES/L11E.png']

cx.freeze.setup(
    name = "GAMETHING",
    options = {'build_exe': {"packages":["pygame"],
                             "included_files":includedfiles}},
    executables = executables
    )
