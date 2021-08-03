import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = "Fruit Basket",
    options = {"build_exe": {"packages":["pygame"],
                             "include_files": ["citron_blank.png", "player.py", "positions.py", "trajcitron.py", "trajframb.py", "trajmelon.py", "trajananas.py","trajbanane.py","trajfraise.py","trajkiwi.py",
                                               "framb_blank.png", "melon_blank.png", "ananas_blank.png",
                                               "banane_blank.png","fraise_blank.png","kiwi_blank.png", "bg.jpg", "basket_player.png", "bg_pause.jpg", "bg_end.jpg", "music.wav"]}},
    executables=executables
)
