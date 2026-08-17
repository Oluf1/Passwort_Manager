password_manager/
│
├── app.py                 
├── managers/
│   ├── vault_manager.py
│   ├── theme_manager.py
│   ├── font_manager.py
│   └── config_manager.py
│
├── ui/
│   ├── ui_handler.py       # Frames, Themes, Helpfunctions
│   ├── main_menu.py        # load_start_ui()
│   ├── config_ui.py        # Load_config(), open_vault_config()
│   ├── vault_ui.py         # load_vaults(), open_vault(), new_vault()
│   ├── service_ui.py       # add_service(), open_service()
│   ├── mail_ui.py          # add_mail(), open_mail()
│   ├── widgets.py          # Label_combobox usw.
│   └── pagination.py       # render_pages()
│
├── crypto/
│   ├── encrypt.py
│   └── decrypt.py
│
└── data/
    ├── Load.py             # Load_service,Load_mail
    ├── save.py             
